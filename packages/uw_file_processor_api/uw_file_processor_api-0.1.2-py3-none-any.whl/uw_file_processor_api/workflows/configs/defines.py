import os

# mongo configs
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'file-processor-api')

# graph api configs
GRAPH_API_URL = os.getenv('GRAPH_API_URL', 'http://localhost:5000')


BUCKET_PATH_RAW = 'raw'
BUCKET_PATH_PARSED = 'processed'
BUCKET_PATH_FILTERS = 'filters'
BUCKET_PATH_FOR_TRAINING = 'for_training'
BUCKET_PATH_MODELS = 'models'
BUCKET_PATH_PREDICTIONS = 'predictions'

PARQUET_CONTENT_TYPE = 'application/octet-stream'
PARQUET_EXTENSION = 'parquet'

METADATA_CONTENT_TYPE = 'content-type'
