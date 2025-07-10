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