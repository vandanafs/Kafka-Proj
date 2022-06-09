from kafka import KafkaConsumer
from json import loads
from sqlalchemy import create_engine, engine


if __name__ == '__main__':
    engine = create_engine('sqlite:///bank.db', echo = True)
    db = engine.connect()
    consumer = KafkaConsumer('delinquents', 
                bootstrap_servers = ['localhost:9092'],
                value_deserializer = lambda m: loads(m.decode('ascii')))
    for message in consumer:
        cust_id, x_action_date, xaction_type, current_balance = message.value.values()
        print('cust_id: {} is a delinquent'.format(cust_id))
        update_delinquents = "INSERT INTO \'healthy-ish balances\' (custid, createdate, xaction, balance) VALUES({}, {}, '{}', {})".format(cust_id, x_action_date, xaction_type, current_balance)
        db.execute(update_delinquents)