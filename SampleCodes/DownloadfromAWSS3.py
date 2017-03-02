import boto
from boto.s3.key import Key

keyId ="AKIAIHMYBGRBYYZ2TFEQ"
sKeyId="PxzjVpCKWRxNO2liDej9R6R9tAK07Zo8D5bcpcrK"
srcFileName="stg_dim_contract.csv"
destFileName="dim_lov.csv"
bucketName="ivyetl-dev"

conn = boto.connect_s3(keyId,sKeyId)
bucket = conn.get_bucket(bucketName)

#Get the Key object of the given key, in the bucket
k = Key(bucket,srcFileName)

#Get the contents of the key into a file 
k.get_contents_to_filename(destFileName)