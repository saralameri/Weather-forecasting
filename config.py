# config.py
import os 
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv(override=True)

    def get(self, key):
        return os.environ.get(key)
    
    def set(self, key, value):
        feedback = os.environ[key] = value
        return feedback
