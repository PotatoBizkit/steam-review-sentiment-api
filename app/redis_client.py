import os
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL=os.getenv("REDIS_URL")