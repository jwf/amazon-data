import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'amazon_data.db')

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize database schema"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Retail Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS retail_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT,
                order_id TEXT,
                order_date TEXT,
                purchase_order_number TEXT,
                currency TEXT,
                unit_price REAL,
                unit_price_tax REAL,
                shipping_charge REAL,
                total_discounts REAL,
                total_owed REAL,
                shipment_item_subtotal REAL,
                shipment_item_subtotal_tax REAL,
                asin TEXT,
                product_condition TEXT,
                quantity INTEGER,
                payment_instrument_type TEXT,
                order_status TEXT,
                shipment_status TEXT,
                ship_date TEXT,
                shipping_option TEXT,
                shipping_address TEXT,
                billing_address TEXT,
                carrier_name_tracking TEXT,
                product_name TEXT,
                gift_message TEXT,
                gift_sender_name TEXT,
                gift_recipient_contact TEXT,
                item_serial_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Digital Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS digital_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT,
                product_name TEXT,
                order_id TEXT,
                digital_order_item_id TEXT,
                order_date TEXT,
                quantity_ordered INTEGER,
                our_price REAL,
                our_price_currency TEXT,
                fulfilled_date TEXT,
                is_fulfilled TEXT,
                seller_of_record TEXT,
                gift_item TEXT,
                subscription_order_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Returns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                return_authorization_id TEXT,
                tracking_id TEXT,
                return_creation_date TEXT,
                order_id TEXT,
                return_ship_option TEXT,
                carrier_package_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cart Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_added_to_cart TEXT,
                source TEXT,
                asin TEXT,
                product_name TEXT,
                cart_domain TEXT,
                cart_list TEXT,
                quantity INTEGER,
                one_click_buyable TEXT,
                to_be_gift_wrapped TEXT,
                prime_subscription TEXT,
                pantry TEXT,
                add_on TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_retail_orders_order_id ON retail_orders(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_retail_orders_order_date ON retail_orders(order_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_retail_orders_order_status ON retail_orders(order_status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_digital_items_order_id ON digital_items(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_digital_items_order_date ON digital_items(order_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_returns_order_id ON returns(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_returns_return_creation_date ON returns(return_creation_date)')
        
        conn.commit()

if __name__ == '__main__':
    init_database()
    print(f"Database initialized at {DATABASE_PATH}")
