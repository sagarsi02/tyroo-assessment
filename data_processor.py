#!/usr/bin/env python3
"""
Tyroo Large CSV Processor - Stores all fields as text/varchar
"""

import os
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from datetime import datetime
from dotenv import load_dotenv

# Initialize environment
load_dotenv()

# Constants
CSV_URL = "https://tyroo-engineering-assesments.s3.us-west-2.amazonaws.com/Tyroo-dummy-data.csv.gz"
LOCAL_FILENAME = "tyroo_data.csv.gz"
CHUNK_SIZE = 10000  # Rows per chunk
LOG_FILE = "tyroo_processing.log"
TABLE_NAME = "products"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TyrooDataProcessor:
    def __init__(self):
        """Initialize with DB config from environment"""
        self.db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'tyroo_data')
        }
        self.engine = None

    def _validate_config(self):
        """Check required environment variables"""
        if not self.db_config['user'] or not self.db_config['password']:
            raise ValueError("DB_USER and DB_PASSWORD must be set in .env file")

    def _create_db_engine(self):
        """Create SQLAlchemy engine for PostgreSQL"""
        try:
            self._validate_config()
            db_url = URL.create(
                drivername="postgresql",
                username=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database']
            )
            self.engine = create_engine(db_url)
            logger.info(f"Connected to database: {self.db_config['database']}")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    def download_file(self):
        """Download the CSV file with progress tracking"""
        try:
            if os.path.exists(LOCAL_FILENAME):
                logger.info(f"File already exists: {LOCAL_FILENAME}")
                return True

            logger.info(f"Downloading from {CSV_URL}")
            response = requests.get(CSV_URL, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(LOCAL_FILENAME, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    downloaded += f.write(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        logger.info(f"Downloaded {progress:.1f}%")

            logger.info(f"Download complete: {LOCAL_FILENAME}")
            return True

        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            if os.path.exists(LOCAL_FILENAME):
                os.remove(LOCAL_FILENAME)
            raise

    def _clean_chunk(self, chunk):
        """Convert all values to strings and clean NaN values"""
        return chunk.fillna('').astype(str)

    def process_file(self):
        """Process the CSV file in chunks"""
        if not os.path.exists(LOCAL_FILENAME):
            raise FileNotFoundError(f"File not found: {LOCAL_FILENAME}")

        try:
            self._create_db_engine()
            total_rows = 0
            start_time = datetime.now()

            # Process file in chunks
            for i, chunk in enumerate(pd.read_csv(
                LOCAL_FILENAME,
                compression='gzip',
                chunksize=CHUNK_SIZE,
                low_memory=False
            )):
                try:
                    cleaned_chunk = self._clean_chunk(chunk)
                    cleaned_chunk.to_sql(
                        TABLE_NAME,
                        self.engine,
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    total_rows += len(cleaned_chunk)
                    
                    # Log progress every 5 chunks
                    if i % 5 == 0:
                        elapsed = (datetime.now() - start_time).total_seconds()
                        speed = total_rows / elapsed if elapsed > 0 else 0
                        logger.info(
                            f"Processed {total_rows:,} rows "
                            f"({speed:,.0f} rows/sec)"
                        )
                except Exception as e:
                    logger.error(f"Error processing chunk {i}: {str(e)}")
                    continue

            logger.info(f"Processing complete. Total rows: {total_rows:,}")
            logger.info(f"Elapsed time: {datetime.now() - start_time}")

        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise

    def run(self):
        """Execute the full processing pipeline"""
        try:
            logger.info("Starting Tyroo Data Processing")
            self.download_file()
            self.process_file()
            logger.info("Processing completed successfully")
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        processor = TyrooDataProcessor()
        processor.run()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        exit(1)