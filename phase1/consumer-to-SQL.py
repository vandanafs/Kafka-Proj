import getpass
import os
from kafka import KafkaConsumer, TopicPartition
from json import loads
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#name = os.getenv('vandana')
#pswd = os.getenv('Data@223')
#my_sql= 'mysql+mysqlconnector://' + name + ":" + pswd + '@localhost/bank'
#engine=create_engine(my_sql)

#Session.configure()
#Base = declarative_base(bind=engine)

#using sqlalchey
#engine=create_engine("sqlite:///bank_al.db")
#session=sessionmaker(bind=engine)()
#Base = declarative_base()

db_name = 'zipbank'
user = getpass.getuser()
pass1 = getpass.getpass(stream=None)
db_engine=create_engine(f'mysql+pymysql://{user}:{pass1}@localhost')

with db_engine.connect() as connect:
    connect.execute(f'Create DATABASE IF NOT EXISTS {db_name}')
    connect.execute(f'use {db_name}')
    connect.execute(f'CREATE TABLE IF NOT EXISTS transactions'
                    f'(id INTEGER PRIMARY KEY AUTO_INCREMENT, '
                    f'custid INTEGER, type VARCHAR(250) NOT Null, '
                    f'date INTEGER, '
                    f'amt INTEGER)')

engine=create_engine(f'mysql+pymysql://{user}:{pass1}@localhost/{db_name}')
Base = declarative_base(bind=engine)


class XactionConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer('bank-customer-events',
            bootstrap_servers=['localhost:9092'],
            # auto_offset_reset='earliest',
            value_deserializer=lambda m: loads(m.decode('ascii')))
        ## These are two python dictionarys
        # Ledger is the one where all the transaction get posted
        self.ledger = {}
        # custBalances is the one where the current blance of each customer
        # account is kept.
        self.custBalances = {}
        # THE PROBLEM is every time we re-run the Consumer, ALL our customer
        # data gets lost!
        # add a way to connect to your database here.

        #Go back to the readme.



    def handleMessages(self):
        for message in self.consumer:
            message = message.value
            print('{} received'.format(message))
            self.ledger[message['custid']] = message
            # add message to the transaction table in your SQL usinf SQLalchemy
            with engine.connect() as connection:
               # connection.execute('insert into transactions ({0}, {1}, {2}, {3})'.format(message['custid'], message['type'], message['date'], message['amt']))
                connection.execute("insert into transactions(custid,type,date,amt) values (%s,%s,%s,%s)",(message['custid'],message['type'],message['date'],message['amt']))

            #with engine.connect() as connection:
               # connection.execute("insert into transaction(custid,type,date,amt) values (%s,%s,%s,%s)",(message['custid'],message['type'],message['date'],message['amt']))
                 #message_to_sqltable = Transaction(custid=message['custid'], type = message['type'], date=message['date'], amt=message['amt'])
            if message['custid'] not in self.custBalances:
                self.custBalances[message['custid']] = 0
            if message['type'] == 'dep':
                self.custBalances[message['custid']] += message['amt']
            else:
                self.custBalances[message['custid']] -= message['amt']
            print(self.custBalances)
           # Session = sessionmaker()
           # session = Session()
            #session.add(message_to_sqltable)
            #session.commit()




      

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    c = XactionConsumer()
    c.handleMessages()