#!/usr/bin/env
import requests
import argparse
import xml.etree.ElementTree as ET

import logging
import httplib
#logging and httplib used by requests to debug, see comments in main section 

import os
import sys

jasper_server = os.environ.get('JASPER_SERVER')
jasper_user = os.environ.get('JASPER_USER')
jasper_password = os.environ.get('JASPER_PASSWORD')
jasper_folderpath = os.environ.get('JASPER_FOLDERPATH')
  
def report_download(repo_path, folder=None, jasper_url=None, auth=None, user=None, password=None):
  '''
  
  Downloads a report and some other files from JasperReportsServer.
  repo_path is full report path in the JRS Repository.
    For ex, to download from Public, test_report use /public/test_report
    checks for correct repo path syntax (unix-like) are not implemented here,
    so be careful to correctly form path string.
    Terminating '/' slashes are stripped, whitespaces are stripped via .strip()
  folder - folder to download report files, default - None (.)
  
  Remember that repo path is relative to logged in user. For superuser in PRO you will have to use
  /organizations/organization_1/ syntax, for jasperadmin - /organization_1, for user /reports and so on.
  
  jasper_url is http path to JRS. Default is http://localhost:8080/jasperserver-pro
  user, password - authorization for digest. Defaults are 'superuser', 'superuser'
  
  '''
  
  # double checking the optional data in case this function is called from another module.
  # You may also want to convert them to strings via str() 
  if not jasper_url:
    jasper_url = jasper_server
  if not user:
    user = jasper_user
  if not password:
    password = jasper_password
  if not folder:
    folder = jasper_folderpath
  else:
    # stripping trailing slashes
    folder = folder.rstrip('/')
    folder = folder.rstrip('\\')  

  auth = (user, password)    
  
  # allwoed file types for download
  file_types = ['jrxml', 'img', 'jar', 'font']
  
  # really basic stripping, use something else for production
  (parent_folder, report_name) = repo_path.rsplit('/', 1)
  
  # Dicttionary structure not requred, just reusing some lines from upoload cmd
  args ={
  'repo_path': repo_path.strip().rstrip('/'),
  'report_name': report_name,
  'parent_folder': parent_folder,
  'jasper_url': jasper_url.strip().rstrip('/'),
  'rest_resource': '/rest/resource',
  'auth': auth
  }
  
  # we cannot initialize some values from other values before they are initilized
  args['url'] = args['jasper_url'] + args['rest_resource'] + args['repo_path']
  
  # setting parameters to get actual file content  
  params = {'fileData': 'true'}
  
  # initilizing session
  s = requests.Session()   
  r = s.get(url=args['url'], auth=args['auth'])
  logging.info(r.status_code)
  r.raise_for_status()
  
  # creating tree from ResourceDescripotor
  tree = ET.fromstring(r.content)
  
  # checking for folder if it is not empty string and creating it
  if folder != "":
    if not os.path.exists(folder):
      os.makedirs(folder)
  
  # searching tree. Could be more efficient with Xpath
  # You may also implement testing for reportUnit wsType for speedsup   
  for i in tree.iter('resourceDescriptor'):
    if 'wsType' in i.attrib:
      if i.attrib['wsType'] in file_types:
        #files[i.attrib['name']] = [i.attrib['uriString'], i.attrib['wsType']]
        url = args['jasper_url'] + args['rest_resource'] + i.attrib['uriString']
        r = s.get(url=url, params=params)
        logging.info(r.status_code)
        r.raise_for_status()
        # writing to folder a filename with extension of wsType. i.e:
        # jrxml, jar, img, font. That has implication of all images having ".img" file extension, etc.
        filename = folder + "/" + i.attrib['name'] + "." + i.attrib['wsType'] 
        with open(filename, "wb") as f:
          f.write(r.content)  
  
  # wow, done!
   

if __name__ == '__main__':
  # initilize logging to error.log
  logging.basicConfig(filename='error.log',
                      level=logging.WARNING,
                      format='%(asctime)s %(message)s')
  # same with debug config:
  #=============================================================================
  # logging.basicConfig(filename='error.log',
  #                     level=logging.INFO,
  #                     format='%(asctime)s %(message)s')
  #=============================================================================
  
  # additional console handler per cookbook
  console = logging.StreamHandler()
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console.setFormatter(formatter)
  logging.getLogger().addHandler(console)
  
  #=============================================================================
  # logging per http://docs.python-requests.org/en/latest/api/
  # 
  # httplib.HTTPConnection.debuglevel = 1
  # 
  # you need to initialize logging, otherwise you will not see anything from requests
  # logging.getLogger().setLevel(logging.DEBUG)
  # requests_log = logging.getLogger("requests.packages.urllib3")
  # requests_log.setLevel(logging.DEBUG)
  # requests_log.propagate = True
  #=============================================================================
  
  # configuring argparse, Run jasperrest.py -h to see all options
  parser = argparse.ArgumentParser(description="Upload jrxml file as a report to JasperReports server")
  parser.add_argument("-r","--repo_path", help="Report repository path (with report name)", required=True)
  parser.add_argument("-f","--folder", help="Folder to download report")
  parser.add_argument("-l", "--jasper_url", default='http://localhost:8080/jasperserver-pro',
                      help="JasperReports Server URL, default http://localhost:8080/jasperserver-pro")
  parser.add_argument("-u", "--user", default='superuser',
                      help="JasperReports Server user, default superuser")
  parser.add_argument("-p", "--password", default='superuser',
                      help="JasperReports Server password, default superuser")
  
  args = parser.parse_args()
  
  # attempt our request
  try:
    report_download(**vars(args))
  except Exception as e:
    logging.error('Exception in report_upload(): %s' % e)
