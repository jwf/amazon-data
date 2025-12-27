"""Script to analyze products and improve categorization"""
from database import get_db

# Current category keywords (to identify what's missing)
category_keywords = {
    'Electronics': ['battery', 'charger', 'headphone', 'earbud', 'cable', 'wireless', 'led', 'display', 'screen'],
    'Clothing': ['shirt', 'jacket', 'hoodie', 'pants', 'dress', 'shoes', 'socks', 'clothing', 'apparel'],
    'Home & Kitchen': ['kitchen', 'cabinet', 'organizer', 'storage', 'container', 'home', 'household'],
    'Books & Media': ['book', 'dvd', 'cd', 'movie', 'music'],
    'Beauty & Personal Care': ['makeup', 'cosmetic', 'beauty', 'skincare', 'shampoo', 'soap'],
    'Sports & Outdoors': ['sport', 'outdoor', 'camping', 'hiking', 'tent', 'backpack'],
    'Toys & Games': ['toy', 'game', 'lego', 'puzzle', 'board game'],
    'Health & Wellness': ['vitamin', 'supplement', 'health', 'wellness', 'fitness', 'electrolyte']
}

def categorize_product(product_name, categories):
    """Categorize a product based on keywords"""
    if not product_name:
        return None
    
    product_lower = product_name.lower()
    
    for category, keywords in categories.items():
        if any(keyword in product_lower for keyword in keywords):
            return category
    return None

# Get sample products that aren't categorized
with get_db() as conn:
    cursor = conn.cursor()
    
    # Get products by spending
    cursor.execute('''
        SELECT 
            product_name, 
            SUM(total_owed) as spending,
            COUNT(*) as count
        FROM retail_orders
        WHERE order_status != 'Cancelled'
          AND total_owed IS NOT NULL
          AND total_owed > 0
          AND product_name IS NOT NULL
        GROUP BY product_name
        ORDER BY spending DESC
        LIMIT 100
    ''')
    
    print("Top 100 products by spending:\n")
    uncategorized = []
    
    for row in cursor.fetchall():
        product_name = row['product_name']
        spending = row['spending']
        count = row['count']
        
        category = categorize_product(product_name, category_keywords)
        
        if category:
            print(f"✓ [{category:20s}] ${spending:8.2f} ({count:3d}x) {product_name[:80]}")
        else:
            uncategorized.append((product_name, spending, count))
            print(f"✗ [{'Other':20s}] ${spending:8.2f} ({count:3d}x) {product_name[:80]}")
    
    print(f"\n\nUncategorized products (top 50 by spending):")
    print("=" * 100)
    for product_name, spending, count in uncategorized[:50]:
        print(f"${spending:8.2f} ({count:3d}x) {product_name}")
