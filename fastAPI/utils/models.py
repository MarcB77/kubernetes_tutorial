import utils.database as _database
import sqlalchemy as _sql


class Predictions(_database.Base):
    """ This class defines the 'Predictions' Table.
        Including three columns: 
        id: A UUID from a host ID, sequence number, and the current time. 
        created_at: A datetime with timezone: Europe/Amsterdam
        predictions: Prediction, whether the two questions are 'Similar' or 'Not similar'

    Args:
        _database (base): sqlalchemy table
    """
    __tablename__ = "predictions"
    id = _sql.Column(_sql.String, primary_key=True, index=True)
    created_at = _sql.Column(_sql.TIMESTAMP, unique=True, index=True)
    predictions = _sql.Column(_sql.String, unique=False, index=True)

class RawInput(_database.Base):
    """ This class defines the 'Predictions' Table.
        Including three columns: 
        id: A UUID from a host ID, sequence number, and the current time. 
        created_at: A datetime with timezone: Europe/Amsterdam, when the request was received.
        question1: Question one from the user input
        question2: Question two from the user input
        q1_words: Amount of words of Question 1
        q2_words: Amount of words of Question 2

    Args:
        _database (base): sqlalchemy table
    """
    __tablename__ = "raw_input"
    id = _sql.Column(_sql.String, primary_key=True, index=True)
    created_at = _sql.Column(_sql.TIMESTAMP, unique=True, index=True)
    question1 = _sql.Column(_sql.String, unique=False, index=True)
    question2 = _sql.Column(_sql.String, unique=False, index=True)
    q1_words = _sql.Column(_sql.Integer, unique=False, index=True)
    q2_words = _sql.Column(_sql.Integer, unique=False, index=True)