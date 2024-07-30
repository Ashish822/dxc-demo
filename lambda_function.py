import boto3
import json
import os
import cfnresponse
import logging

logging.basicConfig(format='%(asctime)s::%(levelname)s::%(message)s', level=logging.DEBUG)

client = boto3.client('ssm')
s3 = boto3.resource("s3")



def lambda_handler(event, context):
    
    logging.info(f"{json.dumps(event)}")
    
    try:
        
        parameter_1 = client.get_parameter(
        Name=os.environ.get('PARAMETER1'),
        )

        parameter_2 = client.get_parameter(
        Name=os.environ.get('PARAMETER2'),
        )
    
        print(f"parameter_1:{parameter_1}")
        print(f"parameter_2:{parameter_2}")
    
        x = {parameter_1.get('Parameter').get('Name'): parameter_1.get('Parameter').get('Value'), parameter_2.get('Parameter').get('Name'): parameter_2.get('Parameter').get('Value')}
    
        bucket_name = "dxc-home-assignment"
        file_name = "hello.txt"
        s3_path = "dxc/" + file_name
        encoded_string = json.dumps(x).encode("utf-8")
        responseData=x
    
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    
        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")
    
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps({parameter_1.get('Parameter').get('Name'): parameter_1.get('Parameter').get('Value'), parameter_2.get('Parameter').get('Name'): parameter_2.get('Parameter').get('Value')})
        }
    
    except Exception as err:
        
        logging.exception(f"{err}")
