# Importing libraries
import json
import os
import boto3
import datetime
import time
import pandas as pd
import yfinance as yf

REGION = os.environ['REGION']
STREAMNAME = os.environ['STREAMNAME']

# us-east-1 is N. Virginia
# us-east-2 is Ohio
#kinesis = boto3.client('kinesis', "us-east-2")
kinesis = boto3.client('kinesis', REGION)

# Stocks
stocks_list = ['FB', 'SHOP', 'BYND', 'NFLX', 'PINS', 'SQ', 'TTD', 'OKTA', 'SNAP', 'DDOG']

def lambda_handler(event, context):
    json_data = {}
    for stock in stocks_list:
        data = yf.Ticker(stock).history(start="2022-05-02", end="2022-05-03", interval="5m")
        data.reset_index(inplace=True)

        for index, interval in data.iterrows():
            json_data['name'] = stock
            json_data['high'] = round(interval['High'], 2)
            json_data['low'] = round(interval['Low'], 2)
            json_data['ts'] = str(interval['Datetime'])
            json_data['hour'] = int(str(interval['Datetime'])[11:13])
            json_upload = json.dumps(json_data)+"\n"

            #kinesis.put_record(StreamName="kinesis-prj3", Data=json_upload, PartitionKey="partitionkey")
            kinesis.put_record(StreamName=STREAMNAME, Data=json_upload, PartitionKey="partitionkey")
            time.sleep(1)
