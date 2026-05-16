from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
import redis
import json
import pika
import os
import time

DATABASE_URL = "postgresql://user:pass@db:5432/webshop"
engine = create_engine(DATABASE_URL)
for attempt in range(5):
    try:
        with engine.connect() as connection:
            break
    except OperationalError:
        if attempt == 4:
            print("Could not connect to PostgreSQL. Exiting.")
            raise
        print("PostgreSQL is starting up, retrying in 3 seconds...")
        time.sleep(3)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            file_path = "/app/products.txt"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                products_to_add = []
                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue

                    if "\t" in line:
                        parts = line.split("\t")
                    else:
                        parts = line.rsplit(None, 1)

                    if len(parts) == 2:
                        name = parts[0].strip()
                        try:
                            price = float(parts[1].strip())
                            products_to_add.append(Product(name=name, price=price))
                        except ValueError:
                            continue

                if products_to_add:
                    db.add_all(products_to_add)
                    db.commit()
                    print(f"Database successfully seeded with {len(products_to_add)} products from file.")
            else:
                print("Seed file 'products.txt' not found. Skipping initialization.")
    except Exception as e:
        print(f"Seeding error: {e}")
    finally:
        db.close()

seed_db()

app = FastAPI()

cache = redis.Redis(host='cache', port=6379, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def home():
#     return {"message": "Backend with Database is running"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    cached_products = cache.get("all_products")

    if cached_products:
        print("Data is from Redis")
        return json.loads(cached_products)

    print("Data is from database, saving to Redis")
    products = db.query(Product).all()

    product_list = [{"id": p.id, "name": p.name, "price": p.price} for p in products]

    cache.setex("all_products", 60, json.dumps(product_list))

    return product_list

@app.post("/add-test-product")
def add_product(name: str, price: float, db: Session = Depends(get_db)):
    new_product = Product(name=name, price=price)
    db.add(new_product)
    db.commit()
    cache.delete("all_products")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='mq'))
        channel = connection.channel()
        channel.queue_declare(queue='inventory_updates')

        message = f"New product added: {name} with price {price}"
        channel.basic_publish(exchange='', routing_key='inventory_updates', body=message)
        connection.close()
        print(f" Sent message to RabbitMQ: {message}")
    except Exception as e:
        print(f"RabbitMQ error: {e}")

    return {"message": f"Product {name} added, cache cleared and notification sent"}

app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")