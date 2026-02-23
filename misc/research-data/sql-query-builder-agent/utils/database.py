from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

def create_sample_db(db_uri: str):
    """Creates a sample SQLite database with Users, Products, and Orders tables."""
    engine = create_engine(db_uri)
    metadata = MetaData()

    # Define tables
    users = Table(
        'users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('email', String),
        Column('signup_date', DateTime)
    )

    products = Table(
        'products', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('category', String),
        Column('price', Float),
        Column('stock', Integer)
    )

    orders = Table(
        'orders', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('order_date', DateTime),
        Column('total_amount', Float),
        Column('status', String) # Pending, Shipped, Delivered
    )

    order_items = Table(
        'order_items', metadata,
        Column('id', Integer, primary_key=True),
        Column('order_id', Integer, ForeignKey('orders.id')),
        Column('product_id', Integer, ForeignKey('products.id')),
        Column('quantity', Integer),
        Column('unit_price', Float)
    )

    metadata.create_all(engine)

    # Insert sample data
    with Session(engine) as session:
        # Check if data already exists to avoid duplication if run multiple times
        if session.query(users).first():
            print("Database already contains data.")
            return

        print("Populating database with sample data...")

        # Create Users
        sample_users = []
        names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
        for i, name in enumerate(names):
            user = {
                'name': name,
                'email': f"{name.lower()}@example.com",
                'signup_date': datetime.now() - timedelta(days=random.randint(0, 365))
            }
            sample_users.append(user)

        # We need to execute inserts to get IDs back or just bulk insert
        session.execute(users.insert(), sample_users)
        session.commit()

        # Create Products
        categories = ["Electronics", "Books", "Clothing", "Home"]
        product_names = [
            ("Laptop", "Electronics", 1200.0),
            ("Smartphone", "Electronics", 800.0),
            ("Headphones", "Electronics", 150.0),
            ("Novel", "Books", 15.0),
            ("Science Textbook", "Books", 80.0),
            ("T-Shirt", "Clothing", 20.0),
            ("Jeans", "Clothing", 50.0),
            ("Coffee Maker", "Home", 40.0),
            ("Blender", "Home", 30.0),
            ("Desk Lamp", "Home", 25.0)
        ]

        sample_products = []
        for name, cat, price in product_names:
            prod = {
                'name': name,
                'category': cat,
                'price': price,
                'stock': random.randint(10, 100)
            }
            sample_products.append(prod)

        session.execute(products.insert(), sample_products)
        session.commit()

        # Create Orders
        user_ids = [r[0] for r in session.query(users.c.id).all()]
        product_ids = [r[0] for r in session.query(products.c.id).all()]
        product_prices = {r[0]: r[1] for r in session.query(products.c.id, products.c.price).all()}

        sample_orders = []
        sample_order_items = []

        statuses = ["Pending", "Shipped", "Delivered", "Cancelled"]

        for _ in range(50): # 50 orders
            user_id = random.choice(user_ids)
            order_date = datetime.now() - timedelta(days=random.randint(0, 60))

            # Create order items first to calculate total
            num_items = random.randint(1, 5)
            order_total = 0
            current_order_items = []

            # We need the order ID, so we insert the order first with 0 total, then update it?
            # Or just estimate. Let's do it properly: execute insert and get ID.
            # SQLAlchemy 1.4+ style

            # Simplification: generate data in memory then insert
            # But wait, foreign keys need IDs.
            # I'll just do it sequentially.
            pass

        # Re-doing orders loop with direct execution to handle IDs

        for _ in range(50):
            user_id = random.choice(user_ids)
            order_date = datetime.now() - timedelta(days=random.randint(0, 60))
            status = random.choice(statuses)

            # Insert Order
            result = session.execute(orders.insert().values(
                user_id=user_id,
                order_date=order_date,
                total_amount=0, # Update later
                status=status
            ))
            order_id = result.inserted_primary_key[0]

            num_items = random.randint(1, 5)
            order_total = 0

            for _ in range(num_items):
                prod_id = random.choice(product_ids)
                qty = random.randint(1, 3)
                price = product_prices[prod_id]
                item_total = price * qty
                order_total += item_total

                session.execute(order_items.insert().values(
                    order_id=order_id,
                    product_id=prod_id,
                    quantity=qty,
                    unit_price=price
                ))

            # Update order total
            session.execute(orders.update().where(orders.c.id == order_id).values(total_amount=order_total))

        session.commit()
        print("Database populated successfully.")

if __name__ == "__main__":
    create_sample_db("sqlite:///sample_data.db")
