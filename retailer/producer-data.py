import csv
from time import sleep
from json import dumps
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
        #return df_toys
        df_toys2 = df_toys.to_json()
        return json.dumps(df_toys2).encode("utf-8")



    def generateRandomXactions(self, n=1000):
        #self.producer.send('READDATA_PROJECT', b'Hello, World!')
        #self.producer.send('READDATA_PROJECT', key=b'message-two', value=b'This is Kafka-Python')
        data = self.emit()
        print('Test Data', data)

        self.producer.send(topic='READ_DATA', value=data)
        #data5 = json.dumps(data)
        self.producer.flush()
        self.producer.close()


if __name__ == "__main__":
    p = Producer()
    p.generateRandomXactions()

        
       

if __name__ == "__main__":
    p = Producer()
    p.generateRandomXactions()
