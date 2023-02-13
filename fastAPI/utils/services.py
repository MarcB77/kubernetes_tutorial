import datetime

import utils.database as _database
import utils.models as _models
import pandas as pd
import sqlalchemy.orm as _orm
from snowflake.connector.pandas_tools import write_pandas


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""------------------------------------------"""
def get_prediction(db: _orm.Session, skip: int = 0, limit: int = 100):
    """ View data from your table 'Predictions' from sqlite_database.db 

    Args:
        db (_orm.Session): Connects to your sqlite_database.db
        skip (int, optional): Skip the first amount of rows. Defaults to 0.
        limit (int, optional): Amount of rows to view. Defaults to 100.

    Returns:
        Query: Returns your SQL query. 
    """
    return db.query(_models.Predictions).offset(skip).limit(limit).all()

def create_prediction(db: _orm.Session, PredictionID: str, created_at: datetime.datetime, pred):
    """ Insert predictions data to your local sqlite Database 'Predictions' table.

    Args:
        db (_orm.Session): Connects to your sqlite_database.db
        PredictionID (str): A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime.datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
        pred (list): Prediction, whether the two questions are 'Similar' or 'Not similar'

    Returns:
        sqlite table: Predictions table.
    """
    print("UUID: {} CREATED_AT: {}\n".format(PredictionID, created_at))
    db_prediction_data = _models.Predictions(id=PredictionID, created_at=created_at , predictions=str(pred))
    db.add(db_prediction_data)
    db.commit()
    db.refresh(db_prediction_data)
    return db_prediction_data

def get_rawinput(db: _orm.Session, skip: int = 0, limit: int = 100):
    """ View data from your table 'raw_input' from sqlite_database.db 

    Args:
        db (_orm.Session): Connects to your sqlite_database.db
        skip (int, optional): Skip the first amount of rows. Defaults to 0.
        limit (int, optional): Amount of rows to view. Defaults to 100.

    Returns:
        Query: Returns your SQL query. 
    """
    return db.query(_models.RawInput).offset(skip).limit(limit).all()

def create_rawinput(db: _orm.Session, id: str, created_at: datetime.datetime, raw_input: dict):
    """ Insert raw user input data to your local sqlite Database 'Raw_input' table.

    Args:
        db (_orm.Session): Connects to your sqlite_database.db
        id (str):  A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime.datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
        raw_input (dict): The raw input data from the user.
    """    

    db_raw = _models.RawInput(
        id = id,  
        created_at = created_at,
        question1 = str(raw_input["question1"]), 
        question2 = str(raw_input["question2"]),
        q1_words = str(raw_input["q1_words"]), 
        q2_words = str(raw_input["q2_words"])
    )
    db.add(db_raw)
    db.commit()
    db.refresh(db_raw)

"""------------ MONGO DB ------------"""
def insert_raw_mongodb(input_data, UUID, created_at):
    """ Insert data to your MongoDB 'Raw_input' table.

    Args:
        input_data (dict): The raw input data from the user.
        UUID (str): A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
    """
    mongo_input = input_data
    mongo_input["id"] = UUID
    mongo_input["created_at"] = created_at
    _database.raw_input_mongoDB.insert_one(mongo_input)  # --> MONGO_DB
    
def insert_predictions_mongodb(UUID, created_at, predictions):
    """ Insert data to your MongoDB 'Predictions' table.

    Args:
        UUID (str):  A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
        predictions (list): Prediction, whether the two questions are 'Similar' or 'Not similar'.
    """
    _database.predictions_mongoDB.insert_one({"id": UUID, "created_at": created_at, "predictions": predictions})

"""------------ Snowflake DB ------------"""
def insert_raw_snowflake(input_data, UUID, created_at):
    """ Insert data to your snowflake 'Raw_input' table.

    Args:
        input_data (dict): The raw input data from the user.
        UUID (str): A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
    """
    snowflake_input = input_data
    snowflake_input["id"] = UUID
    snowflake_input["created_at"] = created_at
    snowflake_input = {key.upper(): [val] for key, val in snowflake_input.items()}
    write_pandas(_database.snowflake_connector, pd.DataFrame.from_dict(snowflake_input), schema="QUESTIONS_CLASSIFIER", table_name="RAW_INPUT")
    
def insert_predictions_snowflake(UUID, created_at, predictions):
    """ Insert data to your snowflake 'Predictions' table.

    Args:
        UUID (str):  A UUID from a host ID, sequence number, and the current time. 
        created_at (datetime): A datetime with timezone: Europe/Amsterdam, when the request was received.
        predictions (list): Prediction, whether the two questions are 'Similar' or 'Not similar'.
    """
    snowflake_predictions = {"ID": [UUID], "CREATED_AT": [created_at], "PREDICTIONS": [predictions]}
    write_pandas(_database.snowflake_connector, pd.DataFrame.from_dict(snowflake_predictions), schema="QUESTIONS_CLASSIFIER", table_name="PREDICTIONS")