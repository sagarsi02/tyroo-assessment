# Tyroo Large CSV Processor

Processes large CSV files (1.5GB+) and stores all fields as text in PostgreSQL.

## Features

- Downloads large gzipped CSV files
- Processes data in memory-efficient chunks
- Stores all fields as text/varchar in PostgreSQL
- Comprehensive error handling and logging
- Environment variable configuration
- Progress tracking

## Prerequisites

- Python 3.8+
- PostgreSQL 13+

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Create a PostgreSQL database:

```bash
create database tyroo_data;
```

### 4. Configuration

Create a `.env` file in the project root:

```ini
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tyroo_data
```

### 5. Database Schema

Execute the schema file:

```bash
-- Database schema for Tyroo product data with all fields as text/varchar

CREATE TABLE products (
    platform_commission_rate TEXT,
    venture_category3_name_en TEXT,
    product_small_img TEXT,
    deeplink TEXT,
    availability TEXT,
    image_url_5 TEXT,
    number_of_reviews TEXT,
    is_free_shipping TEXT,
    promotion_price TEXT,
    venture_category2_name_en TEXT,
    current_price TEXT,
    product_medium_img TEXT,
    venture_category1_name_en TEXT,
    brand_name TEXT,
    image_url_4 TEXT,
    description TEXT,
    seller_url TEXT,
    product_commission_rate TEXT,
    product_name TEXT,
    sku_id TEXT,
    seller_rating TEXT,
    bonus_commission_rate TEXT,
    business_type TEXT,
    business_area TEXT,
    image_url_2 TEXT,
    discount_percentage TEXT,
    seller_name TEXT,
    product_url TEXT,
    product_id TEXT,
    venture_category_name_local TEXT,
    rating_avg_value TEXT,
    product_big_img TEXT,
    image_url_3 TEXT,
    price TEXT
);

-- Create indexes for better query performance
CREATE INDEX idx_products_product_id ON products(product_id);
CREATE INDEX idx_products_sku_id ON products(sku_id);
CREATE INDEX idx_products_brand ON products(brand_name);
CREATE INDEX idx_products_category1 ON products(venture_category1_name_en);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_seller ON products(seller_name);
```

## Running the Processor

```bash
python data_processor.py
```

The script will:
1. Download the CSV file (1.5GB+)
2. Process it in chunks (10,000 rows at a time)
3. Store all data as text in PostgreSQL
4. Log progress to console and `tyroo_processing.log`



## Configuration Options

Edit these constants in `data_processor.py` if needed:

| Constant | Default | Description |
|----------|---------|-------------|
| `CHUNK_SIZE` | 10000 | Rows processed at a time |
| `LOCAL_FILENAME` | tyroo_data.csv.gz | Local file name |
| `TABLE_NAME` | products | Database table name |

## Troubleshooting

### Memory Errors

Reduce chunk size in `data_processor.py`:

```python
CHUNK_SIZE = 5000  # Reduce from 10000
```

### Database Connection Issues

1. Verify `.env` file contains correct credentials
2. Check PostgreSQL service is running

### Slow Performance

1. Increase chunk size (if memory allows)
2. Add more indexes to the database schema
3. Run on a machine with faster storage


## Project Structure

```
tyroo-processor/
├── data_processor.py  # Main processing script
├── schema.sql         # Database schema
├── requirements.txt   # Python dependencies
├── .env               # Configuration (gitignored)
└── tyroo_processing.log  # Log file (generated)
```

## License

MIT License