import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer,String,DateTime
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ ='images'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    extension = Column(String)
    filepath = Column(String)
    uploader = Column(String,default='admin')
    created_on = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.filename

class Predictions(Base):
    __tablename__ ='predictions'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    pred_class = Column(String)
    created_on = Column(DateTime, default=datetime.now)

    def __str__(self):
        return f"{self.path} | {self.pred_class}"

if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)