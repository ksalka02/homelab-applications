import boto3


client = boto3.client('ssm', region_name='us-east-1')

password = client.get_parameter(
    Name='/api/postgres/password',
    WithDecryption=True
)

pwd = password["Parameter"]["Value"]
host = 'players-api-instance.cqsufl8fdwgq.us-east-1.rds.amazonaws.com'
# print(pwd)

url = f'postgresql+psycopg2://postgres:{pwd}@{host}:5432/players'
# postgresql = {'pguser': 'postgres',
#               'pgpassword': pwd,
#               'pghost': 'players-api-instance.cqsufl8fdwgq.us-east-1.rds.amazonaws.com',
#               'pgport': 5432,
#               'pgdb': 'players'
#               }
