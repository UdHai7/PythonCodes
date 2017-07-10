#uploadtoAWSS3
import boto
import boto.s3
import sys
from boto.s3.key import Key
AWS_ACCESS_KEY_ID = 'AKIAIHMYBGRBYYZ2TFEQ'
AWS_SECRET_ACCESS_KEY = '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'
bucket_name = "ivyetl-dev"

conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

bucket = conn.get_bucket(bucketName)
    key = boto.s3.key.Key(bucket, 'out.csv')
    with open('out.csv') as f:
        key.send_file(f)



