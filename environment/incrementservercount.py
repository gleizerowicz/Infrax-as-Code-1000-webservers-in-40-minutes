from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('app')

azMetadataUrl = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
availabilityZone = requests.get( azMetadataUrl ).content
region = availabilityZone[:-1]
# region = 'us-east-1'
field = "%sserverCount" % region.replace('-','')
expression = "set %s = %s + :val" % ( field, field )
	
response = table.update_item(
    Key={
        'scope': 'all'
    },
    UpdateExpression=expression,
    ExpressionAttributeValues={
        ':val': decimal.Decimal(1)
    },
    ReturnValues="UPDATED_NEW"
)

print("UpdateItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))