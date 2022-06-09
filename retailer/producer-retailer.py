import csv
from time import sleep
from json import dumps,loads
from kafka import KafkaProducer
import time
import random
import boto3
import pandas as pd
import s3fs
import json
import io

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        
    def emit(self):
        
        path1='s3://productscsv/toys_rating4.csv'
        df_toys=pd.read_csv(path1)
        df_toys1=df_toys.to_json()
        return json.dumps(df_toys1).encode("utf-8")
        
        s3 = boto3.resource('s3', aws_access_key_id='AKIAUH4JAJJ7CS5SEIVB', aws_secret_access_key='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')
        bucket = s3.Bucket('productscsv')
        file_name = 'toys_rating4.csv'
        obj = bucket.Object(key=file_name)
        response = obj.get()


        lines = response['Body'].read().decode('utf-8').splitlines(True)
        reader2 = csv.DictReader(lines)  # this works
                

        
        lines2 = response['Body'].read().decode('utf-8')
        spamreader = csv.reader(io.StringIO(lines2),delimiter=',', quotechar='|')
        reader3 = csv.reader(lines2.split('\r\n'))
        

        #new try
       

        #for row in reader3:
          #  print(row) # printing empty list
         
          #  self.producer.flush()

        #return reader2
        #return df_toys

 

    def generateRandomXactions(self, n=1000):
        self.producer.send('READDATA_PROJECT', b'Hello, World!')
        self.producer.send('READDATA_PROJECT', key=b'message-two', value=b'This is Kafka-Python')
        data = self.emit()
        print('Test', data)
        #self.producer.send('READDATA_PROJECT', value=data)
        
        for row in data:
           print('to see what data it is', row)  # if return is reader3
        #print("final",row)    # print headers
           self.producer.send('READDATA_PROJECT', row)  # objString.encode('utf-8') assertion error
           #self.producer.send('READDATA_PROJECT', b'row')   # assertion error
           #self.producer.flush()
           # sleep(1)

    def test(self):
        with open('/Users/vandana/downloads/test.csv','r') as file:
             read1 = csv.DictReader(file, delimiter = ',')
             for messages in read1:
               self.producer.send('R_Topic', messages)
               self.producer.flush()       

if __name__ == "__main__":
    p = Producer()
    p.generateRandomXactions()
   # p.test()
