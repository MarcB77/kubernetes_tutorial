import datetime
import json
import uuid

import mlflow
import pandas as pd
import pytz
import utils.schemas as _schemas
import utils.services as _services
import sqlalchemy.orm as _orm
import uvicorn
from fastapi import Depends, FastAPI
import pickle

app = FastAPI()
_services.create_database()

logged_model = "./question_model"
loaded_model = mlflow.pyfunc.load_model(logged_model)

labels = json.load(open("./utils/labels.json"))

def predict_pipeline(data):
    """ Perform prediction on the loaded Xgboost model (sklearn pipeline).

    Args:
        data (dict): A dictionary inludinge the following keys: question1 (user input), question2 (user input) 
                    and the amount of words in the question (q1_words and q2_words).

    Returns:
        array: Prediction.
    """
    return loaded_model.predict(pd.DataFrame(data))

def amount_words_in_question(raw_input: dict, keys: list, new_keys: list):
    """ Create two new keys: q1_words and q2_words. 
        That indicated the amount of words for each question.

    Args:
        raw_input (dict): The user input data as a dictionary.
        keys (list): The questions that you want to use to calculate the amount of words.
        new_keys (list): Give the new features a name (q1_words and q2_words by default.)

    Returns:
        dict: An extended dictionary with the new features: q1_words and q2_words.
    """
    for index, key in enumerate(keys):
        raw_input[new_keys[index]] = [value.count(' ') + 1 for value in raw_input[key]]
    print(raw_input)
    return raw_input


@app.get("/raw_input/")
def read_rawinput(  
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = Depends(_services.get_db)
):
    """ View data from your table 'raw_input' from sqlite_database.db

    Args:
        skip (int, optional): Skip the first amount of rows. Defaults to 0.
        limit (int, optional): Amount of rows to view. Defaults to 10.
        db (_orm.Session, optional): Connects to your sqlite_database.db. Defaults to Depends(_services.get_db).

    Returns:
        Query: Returns your SQL query. 
    """
    return _services.get_rawinput(db=db, skip=skip, limit=limit)

@app.get("/predictions/")
def read_predict(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = Depends(_services.get_db)
):
    """ View data from your table 'Predictions' from sqlite_database.db

    Args:
        skip (int, optional): Skip the first amount of rows. Defaults to 0.
        limit (int, optional): Amount of rows to view. Defaults to 10.
        db (_orm.Session, optional): Connects to your sqlite_database.db. Defaults to Depends(_services.get_db).

    Returns:
        Query: Returns your SQL query. 
    """
    return _services.get_prediction(db=db, skip=skip, limit=limit)

@app.post("/predict/", response_model=_schemas.Predictions)
def create_predict(
    user: _schemas._CreatePrediction, db: _orm.Session = Depends(_services.get_db)
):
    """ A post request, make a similarity prediction on two questions.


    Args:
        user (_schemas._CreatePrediction): The user input format.
        db (_orm.Session, optional): Connects to your sqlite_database.db. Defaults to Depends(_services.get_db).

    Returns:
        dict: API response as a dictionary with UUID and prediction.
    """    

    """1. Raw input data handling"""
    UUID = str(uuid.uuid1())
    created_at = datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))

    user_input = user.dict()
    user_input = amount_words_in_question(user_input, keys=["question1", "question2"], new_keys=["q1_words", "q2_words"])
    #_services.insert_raw_snowflake(input_data=user_input, UUID=UUID, created_at=created_at)
    _services.insert_raw_mongodb(input_data=user_input, UUID=UUID, created_at=created_at)
    _services.create_rawinput(db=db, id=UUID, created_at=created_at, raw_input=user_input)

    """2. Prediction data handling"""
    prediction = predict_pipeline(user_input)
    predictions = [labels[str(single_prediction)] for single_prediction in prediction.tolist()]
    print("Raw Predictions: ", prediction, "\nPredictions:", predictions)
    
    _services.insert_predictions_mongodb(UUID=UUID, created_at=created_at, predictions=predictions)
    #_services.insert_predictions_snowflake(UUID=UUID, created_at=created_at, predictions=predictions)
    return _services.create_prediction(db=db, PredictionID=UUID, created_at=created_at, pred=predictions)

if __name__ == '__main__':
    uvicorn.run(app)