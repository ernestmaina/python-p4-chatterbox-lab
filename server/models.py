from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, DateTime
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(DateTime, default=db.func.current_timestamp())  # Add the 'created_at' attribute here

# Additional columns and methods can be added as needed
