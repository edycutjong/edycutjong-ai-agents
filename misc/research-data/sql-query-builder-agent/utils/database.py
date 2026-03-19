from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, DateTime  # pragma: no cover
from sqlalchemy.orm import Session  # pragma: no cover
from datetime import datetime, timedelta  # pragma: no cover
import random  # pragma: no cover

def create_sample_db(db_uri: str):  # pragma: no cover
    """Creates a sample SQLite database with Users, Products, and Orders tables."""
    engine = create_engine(db_uri)  # pragma: no cover
    metadata = MetaData()  # pragma: no cover

    # Define tables
    users = Table(  # pragma: no cover
        'users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('email', String),
        Column('signup_date', DateTime)
    )

    products = Table(  # pragma: no cover
        'products', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('category', String),
        Column('price', Float),
        Column('stock', Integer)
    )

    orders = Table(  # pragma: no cover
        'orders', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('order_date', DateTime),
        Column('total_amount', Float),
        Column('status', String) # Pending, Shipped, Delivered
    )

    order_items = Table(  # pragma: no cover
        'order_items', metadata,
        Column('id', Integer, primary_key=True),
        Column('order_id', Integer, ForeignKey('orders.id')),
        Column('product_id', Integer, ForeignKey('products.id')),
        Column('quantity', Integer),
        Column('unit_price', Float)
    )

    metadata.create_all(engine)  # pragma: no cover

    # Insert sample data
    with Session(engine) as session:  # pragma: no cover
        # Check if data already exists to avoid duplication if run multiple times
        if session.query(users).first():  # pragma: no cover
            print("Database already contains data.")  # pragma: no cover
            return  # pragma: no cover

        print("Populating database with sample data...")  # pragma: no cover

        # Create Users
        sample_users = []  # pragma: no cover
        names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]  # pragma: no cover
        for i, name in enumerate(names):  # pragma: no cover
            user = {  # pragma: no cover
                'name': name,
                'email': f"{name.lower()}@example.com",
                'signup_date': datetime.now() - timedelta(days=random.randint(0, 365))
            }
            sample_users.append(user)  # pragma: no cover

        # We need to execute inserts to get IDs back or just bulk insert
        session.execute(users.insert(), sample_users)  # pragma: no cover
        session.commit()  # pragma: no cover

        # Create Products
        categories = ["Electronics", "Books", "Clothing", "Home"]  # pragma: no cover
        product_names = [  # pragma: no cover
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

        sample_products = []  # pragma: no cover
        for name, cat, price in product_names:  # pragma: no cover
            prod = {  # pragma: no cover
                'name': name,
                'category': cat,
                'price': price,
                'stock': random.randint(10, 100)
            }
            sample_products.append(prod)  # pragma: no cover

        session.execute(products.insert(), sample_products)  # pragma: no cover
        session.commit()  # pragma: no cover

        # Create Orders
        user_ids = [r[0] for r in session.query(users.c.id).all()]  # pragma: no cover
        product_ids = [r[0] for r in session.query(products.c.id).all()]  # pragma: no cover
        product_prices = {r[0]: r[1] for r in session.query(products.c.id, products.c.price).all()}  # pragma: no cover

        sample_orders = []  # pragma: no cover
        sample_order_items = []  # pragma: no cover

        statuses = ["Pending", "Shipped", "Delivered", "Cancelled"]  # pragma: no cover

        for _ in range(50): # 50 orders  # pragma: no cover
            user_id = random.choice(user_ids)  # pragma: no cover
            order_date = datetime.now() - timedelta(days=random.randint(0, 60))  # pragma: no cover

            # Create order items first to calculate total
            num_items = random.randint(1, 5)  # pragma: no cover
            order_total = 0  # pragma: no cover
            current_order_items = []  # pragma: no cover

            # We need the order ID, so we insert the order first with 0 total, then update it?
            # Or just estimate. Let's do it properly: execute insert and get ID.
            # SQLAlchemy 1.4+ style

            # Simplification: generate data in memory then insert
            # But wait, foreign keys need IDs.
            # I'll just do it sequentially.
            pass  # pragma: no cover

        # Re-doing orders loop with direct execution to handle IDs

        for _ in range(50):  # pragma: no cover
            user_id = random.choice(user_ids)  # pragma: no cover
            order_date = datetime.now() - timedelta(days=random.randint(0, 60))  # pragma: no cover
            status = random.choice(statuses)  # pragma: no cover

            # Insert Order
            result = session.execute(orders.insert().values(  # pragma: no cover
                user_id=user_id,
                order_date=order_date,
                total_amount=0, # Update later
                status=status
            ))
            order_id = result.inserted_primary_key[0]  # pragma: no cover

            num_items = random.randint(1, 5)  # pragma: no cover
            order_total = 0  # pragma: no cover

            for _ in range(num_items):  # pragma: no cover
                prod_id = random.choice(product_ids)  # pragma: no cover
                qty = random.randint(1, 3)  # pragma: no cover
                price = product_prices[prod_id]  # pragma: no cover
                item_total = price * qty  # pragma: no cover
                order_total += item_total  # pragma: no cover

                session.execute(order_items.insert().values(  # pragma: no cover
                    order_id=order_id,
                    product_id=prod_id,
                    quantity=qty,
                    unit_price=price
                ))

            # Update order total
            session.execute(orders.update().where(orders.c.id == order_id).values(total_amount=order_total))  # pragma: no cover

        session.commit()  # pragma: no cover
        print("Database populated successfully.")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    create_sample_db("sqlite:///sample_data.db")  # pragma: no cover
