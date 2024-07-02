# Today we are going to code a program that allows us to generate some fake data for research.
# Using some libraries that I will list below:
# pandas, faker, sqlite3
# if you don't have one of these libraries, then run the command below on your terminal:
# pip install pandas faker

# Importing libraries:
import pandas as pd
from faker import Faker
import sqlite3
import random

# Variable with the name of the job:
name_job = 'ecommerce_gen'

# Let's add some log capture to our project!
# Log Start Job
print(f'Start of the job in:, {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}')
with open('../log/log.csv', 'a') as f:
    f.write(f'start_job, {name_job},{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

# Starting data generator faker
faker = Faker()

# Setting the number of registers that will be generated
num_customers = 400
num_products = 100
num_orders = 500
num_reviews = 123

# Generating the data:

# Customers Data:
customers = []
for _ in range(num_customers):
    customers.append({
        'customer_id': faker.uuid4(),
        'customer_name': faker.name(),
        'customer_address': faker.address(),
        'customer_email': faker.email(),
        'customer_registration_date': faker.date_this_decade()
    })

customers_df = pd.DataFrame(customers)

# Products Data:
products = []
for _ in range(num_products):
    products.append({
        'product_id': faker.uuid4(),
        'product_name': faker.word(),
        'product_category': faker.word(),
        'product_price': round(random.uniform(10.0, 500.0), 2),
        'product_stock': random.randint(0, 100)
    })

products_df = pd.DataFrame(products)

# Orders Data:
orders = []
for _ in range(num_orders):
    orders.append({
        'order_id': faker.uuid4(),
        'customer_id': random.choice(customers_df['customer_id']),
        'order_date': faker.date_this_year(),
        'total_amount': round(random.uniform(20.0, 1000.0), 2)
    })

orders_df = pd.DataFrame(orders)

# Reviews Data:
reviews = []
for _ in range(num_reviews):
    reviews.append({
        'review_id': faker.uuid4(),
        'customer_id': random.choice(customers_df['customer_id']),
        'product_id': random.choice(products_df['product_id']),
        'rating': random.randint(1, 5),
        'comment': faker.sentence()
    })

reviews_df = pd.DataFrame(reviews)

# Let's test!
# Everything fine!

# Let's insert the data that we generated into a SQLite DB:

# Creating connection:
conn = sqlite3.connect('../db/ecommerce.db')

# Creating the tables in the Database:
customers_df.to_sql('customers', conn, if_exists='replace', index=False)
products_df.to_sql('products', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)
reviews_df.to_sql('reviews', conn, if_exists='replace', index=False)

# Closing the connection:
conn.close()

# Log End Job
with open('../log/log.csv', 'a') as f:
    f.write(f'end_job, {name_job},{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

# Printing a summary of what we generate:
print(f'End of the job in:, {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'Generate {num_customers} Customers, {num_products} Products, {num_orders} Orders, and {num_reviews} Reviews')