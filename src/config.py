import os
from dotenv import load_dotenv
load_dotenv()
POSTGRES = {
    'host': os.getenv('POSTGRES_HOST','localhost'),
    'port': int(os.getenv('POSTGRES_PORT','5432')),
    'database': os.getenv('POSTGRES_DB','retail_analytics'),
    'user': os.getenv('POSTGRES_USER','retail'),
    'password': os.getenv('POSTGRES_PASSWORD','retailpass')
}
KAFKA = os.getenv('KAFKA_BOOTSTRAP_SERVERS','localhost:9092')
