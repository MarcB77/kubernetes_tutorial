import datetime
import uuid

import boto3
import pytz


sess = boto3.Session()
ddb = sess.resource('dynamodb', region_name='us-east-1')

def add_prediction(table, UUID: str, created_at: str, predictions: str):
    
    table.put_item(
        Item={
            'UUID': UUID,
            'created_at': created_at,
            'predictions': predictions
            }
        )
    
def add_raw_input(table, UUID: str, 
                  created_at: str, 
                  question1: str, 
                  question2: str, 
                  q1_words: int, 
                  q2_words: int
                  ):
    
    table.put_item(
        Item={
            'UUID': UUID,
            'created_at': created_at,
            'question1': question1,
            'question2': question2,
            'q1_words': q1_words,
            'q2_words': q2_words
        }
    )

created_at = datetime.datetime.now(tz = pytz.timezone('Europe/amsterdam'))
predictions = 'Similar'

print('Available Tables: ', list(ddb.tables.all()))
add_prediction(table = ddb.Table('Predictions'),
               UUID=str(uuid.uuid1()),
               created_at = str(created_at),
               predictions = predictions
               )

add_raw_input(table = ddb.Table('Raw_input'),
               UUID=str(uuid.uuid1()),
               created_at = str(created_at),
               question1='Hi how are you doing this morning',
               question2='Hi how are you doing today',
               q1_words=7,
               q2_words=6
               )