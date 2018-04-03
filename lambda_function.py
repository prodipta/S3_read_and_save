import email
import boto3

s3 = boto3.client('s3')
s3r = boto3.resource('s3')
temp_dir = "/tmp/"
output_prefix = "output/"

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # ignore if it is not in mail directory, avoid recursive calls
    if "mail/" not in key:
        print("not an incoming mail")
        return None
    
    try:
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=bucket, Key=key)
        obj = s3r.Bucket(bucket).Object(key)
        msg = email.message_from_bytes(obj.get()["Body"].read())
        
        # quit if there is no attachments
        attachments = msg.get_payload()
        if len(attachments) < 2:
            print("we've got no attachment")
            return None
        
        # delete the first item, it will be the mail itself
        del attachments[0]
        
        # run over each attachments
        for attachment in attachments:
            # get the file name
            content_type = attachment.get('Content-Disposition')
            file_name = content_type.split("=")[1].replace('\"', '')
            print("attachment is {}".format(file_name))
            # download to temp dir with the same filename
            with open(temp_dir + file_name, 'wb') as writefile:
                writefile.write(attachment.get_payload(decode=True))
            
            # now upload to the right prefix + mail
            with open(temp_dir + file_name, 'rb')as data:
                s3.upload_fileobj(data, bucket, output_prefix+file_name)
            
        
    except Exception as e:
        # something went wrong - probably permissioning
        print(e)
    
    # we are done here
    return { 
        'bucket' : bucket,
        'key': key
    }
    
