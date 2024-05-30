import os
from dotenv import load_dotenv
import logging as log

load_dotenv()

LOG_LEVEL = os.environ["LOG_LEVEL"]
LLM_VERBOSE = os.environ["LLM_VERBOSE"]
LOG_FILE_PATH = os.environ["LOG_FILE_PATH"]
INDEX_NAME = os.environ["INDEX_NAME"]
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV=os.getenv('PINECONE_ENV')

log.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s : %(filename)s #%(lineno)d - %(message)s',
    handlers=[
        log.FileHandler(LOG_FILE_PATH),
        log.StreamHandler()
    ]
)