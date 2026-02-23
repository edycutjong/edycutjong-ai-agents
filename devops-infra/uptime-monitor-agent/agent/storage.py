from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import DATABASE_URL
except ImportError:
    # Fallback for when running tests or if config is not found
    DATABASE_URL = "sqlite:///uptime.db"

Base = declarative_base()

class MonitorResult(Base):
    __tablename__ = 'monitor_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Float, nullable=True)  # in seconds
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String, nullable=True)
    ssl_expiry_days = Column(Integer, nullable=True)
    ai_diagnosis = Column(String, nullable=True)

# Create an SQLite engine
engine = create_engine(DATABASE_URL, echo=False)

# Create tables
Base.metadata.create_all(engine)

# Session factory
Session = sessionmaker(bind=engine)

def add_result(endpoint, status_code, response_time, error_message=None, ssl_expiry_days=None, ai_diagnosis=None):
    session = Session()
    try:
        result = MonitorResult(
            endpoint=endpoint,
            status_code=status_code,
            response_time=response_time,
            error_message=error_message,
            ssl_expiry_days=ssl_expiry_days,
            ai_diagnosis=ai_diagnosis
        )
        session.add(result)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding result: {e}")
    finally:
        session.close()

def get_latest_results(limit=10):
    session = Session()
    try:
        results = session.query(MonitorResult).order_by(MonitorResult.timestamp.desc()).limit(limit).all()
        return results
    finally:
        session.close()

def get_results_by_endpoint(endpoint, limit=50):
    session = Session()
    try:
        results = session.query(MonitorResult).filter_by(endpoint=endpoint).order_by(MonitorResult.timestamp.desc()).limit(limit).all()
        return results
    finally:
        session.close()
