import zipfile
print "source Folder:"
source_folder=raw_input()
print "Destination Folder:"
destination_folder=raw_input()
zip_ref = zipfile.ZipFile(source_folder, 'r')
zip_ref.extractall(destination_folder)
zip_ref.close()
