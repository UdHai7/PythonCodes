#importing module  
import pypyodbc  
#creating connection Object which will contain SQL Server Connection  
connection = pypyodbc.connect('DRIVER={FreeTDS};SERVER=msdb2.ivy-support.com;PORT=1433;DATABASE=sd_castrol;UID=sd_castrol_sauser;PWD=sd_castrol_sauseradfasd;TDS_Version=7.2;')  
  
print("Connection Successfully Established")  
  
#closing connection  
connection.close() 

