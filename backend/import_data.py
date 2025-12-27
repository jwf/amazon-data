import pandas as pd
import os
from database import get_db, init_database
from datetime import datetime

def clean_numeric(value):
    """Clean numeric values from CSV"""
    if pd.isna(value) or value == 'Not Available' or value == 'Not Applicable':
        return None
    if isinstance(value, str):
        # Remove quotes and convert to float
        value = value.replace("'", "").strip()
        try:
            return float(value)
        except (ValueError, AttributeError):
            return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def clean_text(value):
    """Clean text values from CSV"""
    if pd.isna(value) or value == 'Not Available' or value == 'Not Applicable':
        return None
    return str(value).strip() if value else None

def import_retail_orders(data_dir):
    """Import retail orders from CSV"""
    csv_path = os.path.join(data_dir, 'Retail.OrderHistory.1', 'Retail.OrderHistory.1.csv')
    if not os.path.exists(csv_path):
        print(f"Retail orders CSV not found: {csv_path}")
        return 0
    
    print(f"Loading retail orders from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} rows")
    
    with get_db() as conn:
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM retail_orders')
        
        imported = 0
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO retail_orders (
                        website, order_id, order_date, purchase_order_number, currency,
                        unit_price, unit_price_tax, shipping_charge, total_discounts, total_owed,
                        shipment_item_subtotal, shipment_item_subtotal_tax, asin, product_condition,
                        quantity, payment_instrument_type, order_status, shipment_status, ship_date,
                        shipping_option, shipping_address, billing_address, carrier_name_tracking,
                        product_name, gift_message, gift_sender_name, gift_recipient_contact,
                        item_serial_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    clean_text(row.get('Website')),
                    clean_text(row.get('Order ID')),
                    clean_text(row.get('Order Date')),
                    clean_text(row.get('Purchase Order Number')),
                    clean_text(row.get('Currency')),
                    clean_numeric(row.get('Unit Price')),
                    clean_numeric(row.get('Unit Price Tax')),
                    clean_numeric(row.get('Shipping Charge')),
                    clean_numeric(row.get('Total Discounts')),
                    clean_numeric(row.get('Total Owed')),
                    clean_numeric(row.get('Shipment Item Subtotal')),
                    clean_numeric(row.get('Shipment Item Subtotal Tax')),
                    clean_text(row.get('ASIN')),
                    clean_text(row.get('Product Condition')),
                    int(clean_numeric(row.get('Quantity')) or 0),
                    clean_text(row.get('Payment Instrument Type')),
                    clean_text(row.get('Order Status')),
                    clean_text(row.get('Shipment Status')),
                    clean_text(row.get('Ship Date')),
                    clean_text(row.get('Shipping Option')),
                    clean_text(row.get('Shipping Address')),
                    clean_text(row.get('Billing Address')),
                    clean_text(row.get('Carrier Name & Tracking Number')),
                    clean_text(row.get('Product Name')),
                    clean_text(row.get('Gift Message')),
                    clean_text(row.get('Gift Sender Name')),
                    clean_text(row.get('Gift Recipient Contact Details')),
                    clean_text(row.get('Item Serial Number')),
                ))
                imported += 1
                if imported % 1000 == 0:
                    conn.commit()
                    print(f"Imported {imported} retail orders...")
            except Exception as e:
                print(f"Error importing row: {e}")
                continue
        
        conn.commit()
        print(f"Successfully imported {imported} retail orders")
        return imported

def import_digital_items(data_dir):
    """Import digital items from CSV"""
    csv_path = os.path.join(data_dir, 'Digital-Ordering.1', 'Digital Items.csv')
    if not os.path.exists(csv_path):
        print(f"Digital items CSV not found: {csv_path}")
        return 0
    
    print(f"Loading digital items from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} rows")
    
    with get_db() as conn:
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM digital_items')
        
        imported = 0
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO digital_items (
                        asin, product_name, order_id, digital_order_item_id, order_date,
                        quantity_ordered, our_price, our_price_currency, fulfilled_date,
                        is_fulfilled, seller_of_record, gift_item, subscription_order_info
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    clean_text(row.get('ASIN')),
                    clean_text(row.get('ProductName')),
                    clean_text(row.get('OrderId')),
                    clean_text(row.get('DigitalOrderItemId')),
                    clean_text(row.get('OrderDate')),
                    int(clean_numeric(row.get('QuantityOrdered')) or 0),
                    clean_numeric(row.get('OurPrice')),
                    clean_text(row.get('OurPriceCurrencyCode')),
                    clean_text(row.get('FulfilledDate')),
                    clean_text(row.get('IsFulfilled')),
                    clean_text(row.get('SellerOfRecord')),
                    clean_text(row.get('GiftItem')),
                    clean_text(row.get('SubscriptionOrderInfoList')),
                ))
                imported += 1
                if imported % 1000 == 0:
                    conn.commit()
                    print(f"Imported {imported} digital items...")
            except Exception as e:
                print(f"Error importing row: {e}")
                continue
        
        conn.commit()
        print(f"Successfully imported {imported} digital items")
        return imported

def import_returns(data_dir):
    """Import returns from CSV"""
    csv_path = os.path.join(data_dir, 'Retail.CustomerReturns.1', 'Retail.CustomerReturns.1.csv')
    if not os.path.exists(csv_path):
        print(f"Returns CSV not found: {csv_path}")
        return 0
    
    print(f"Loading returns from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} rows")
    
    with get_db() as conn:
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM returns')
        
        imported = 0
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO returns (
                        return_authorization_id, tracking_id, return_creation_date,
                        order_id, return_ship_option, carrier_package_id
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    clean_text(row.get('Return Authorization Id')),
                    clean_text(row.get('Tracking Id')),
                    clean_text(row.get('Return Creation Date')),
                    clean_text(row.get('Order Id')),
                    clean_text(row.get('Return Ship Option')),
                    clean_text(row.get('Carrier Package Id')),
                ))
                imported += 1
            except Exception as e:
                print(f"Error importing row: {e}")
                continue
        
        conn.commit()
        print(f"Successfully imported {imported} returns")
        return imported

def import_cart_items(data_dir):
    """Import cart items from CSV"""
    csv_path = os.path.join(data_dir, 'Retail.CartItems.1', 'Retail.CartItems.1.csv')
    if not os.path.exists(csv_path):
        print(f"Cart items CSV not found: {csv_path}")
        return 0
    
    print(f"Loading cart items from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} rows")
    
    with get_db() as conn:
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM cart_items')
        
        imported = 0
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO cart_items (
                        date_added_to_cart, source, asin, product_name, cart_domain,
                        cart_list, quantity, one_click_buyable, to_be_gift_wrapped,
                        prime_subscription, pantry, add_on
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    clean_text(row.get('DateAddedToCart')),
                    clean_text(row.get('Source')),
                    clean_text(row.get('ASIN')),
                    clean_text(row.get('ProductName')),
                    clean_text(row.get('CartDomain')),
                    clean_text(row.get('CartList')),
                    int(clean_numeric(row.get('Quantity')) or 0),
                    clean_text(row.get('OneClickBuyable')),
                    clean_text(row.get('ToBeGiftWrapped')),
                    clean_text(row.get('PrimeSubscription')),
                    clean_text(row.get('Pantry')),
                    clean_text(row.get('AddOn')),
                ))
                imported += 1
            except Exception as e:
                print(f"Error importing row: {e}")
                continue
        
        conn.commit()
        print(f"Successfully imported {imported} cart items")
        return imported

def main():
    """Main import function"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    print("Initializing database...")
    init_database()
    
    print("\nStarting data import...")
    retail_count = import_retail_orders(data_dir)
    digital_count = import_digital_items(data_dir)
    returns_count = import_returns(data_dir)
    cart_count = import_cart_items(data_dir)
    
    print(f"\nImport complete!")
    print(f"  Retail orders: {retail_count}")
    print(f"  Digital items: {digital_count}")
    print(f"  Returns: {returns_count}")
    print(f"  Cart items: {cart_count}")

if __name__ == '__main__':
    main()
