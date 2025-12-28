from database import get_db
from collections import defaultdict

class DataProcessor:
    def __init__(self):
        # Database is initialized, no need to load CSV files
        pass
    
    def get_summary(self):
        """Get overall summary statistics"""
        summary = {
            'totalRetailOrders': 0,
            'totalRetailSpending': 0,
            'totalDigitalOrders': 0,
            'totalDigitalSpending': 0,
            'totalOrders': 0,
            'totalSpending': 0,
            'dateRange': {'start': None, 'end': None},
            'averageOrderValue': 0
        }
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Retail orders (excluding cancelled)
            cursor.execute('''
                SELECT COUNT(*) as count, 
                       COALESCE(SUM(total_owed), 0) as spending,
                       MIN(order_date) as min_date,
                       MAX(order_date) as max_date
                FROM retail_orders
                WHERE order_status != 'Cancelled' 
                  AND total_owed IS NOT NULL 
                  AND total_owed > 0
            ''')
            row = cursor.fetchone()
            if row:
                summary['totalRetailOrders'] = row['count']
                summary['totalRetailSpending'] = float(row['spending'] or 0)
                if row['min_date']:
                    summary['dateRange']['start'] = row['min_date']
                if row['max_date']:
                    summary['dateRange']['end'] = row['max_date']
            
            # Digital orders
            cursor.execute('''
                SELECT COUNT(*) as count, 
                       COALESCE(SUM(our_price), 0) as spending
                FROM digital_items
                WHERE our_price IS NOT NULL AND our_price > 0
            ''')
            row = cursor.fetchone()
            if row:
                summary['totalDigitalOrders'] = row['count']
                summary['totalDigitalSpending'] = float(row['spending'] or 0)
        
        summary['totalOrders'] = summary['totalRetailOrders'] + summary['totalDigitalOrders']
        summary['totalSpending'] = summary['totalRetailSpending'] + summary['totalDigitalSpending']
        
        if summary['totalOrders'] > 0:
            summary['averageOrderValue'] = summary['totalSpending'] / summary['totalOrders']
        
        return summary
    
    def get_spending_over_time(self, period='monthly'):
        """Get spending aggregated by time period"""
        result = {'labels': [], 'values': [], 'orderCounts': []}
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            if period == 'monthly':
                # Retail orders
                cursor.execute('''
                    SELECT 
                        strftime('%Y-%m', order_date) as period,
                        SUM(total_owed) as spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM retail_orders
                    WHERE order_status != 'Cancelled'
                      AND total_owed IS NOT NULL
                      AND total_owed > 0
                      AND order_date IS NOT NULL
                    GROUP BY period
                    ORDER BY period
                ''')
                for row in cursor.fetchall():
                    result['labels'].append(row['period'])
                    result['values'].append(float(row['spending'] or 0))
                    result['orderCounts'].append(row['order_count'])
                
                # Digital orders
                cursor.execute('''
                    SELECT 
                        strftime('%Y-%m', order_date) as period,
                        SUM(our_price) as spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM digital_items
                    WHERE our_price IS NOT NULL
                      AND our_price > 0
                      AND order_date IS NOT NULL
                    GROUP BY period
                    ORDER BY period
                ''')
                # Merge with retail data
                digital_data = {row['period']: {'spending': float(row['spending'] or 0), 'count': row['order_count']} 
                               for row in cursor.fetchall()}
                
                for period_key, data in digital_data.items():
                    if period_key in result['labels']:
                        idx = result['labels'].index(period_key)
                        result['values'][idx] += data['spending']
                        result['orderCounts'][idx] += data['count']
                    else:
                        result['labels'].append(period_key)
                        result['values'].append(data['spending'])
                        result['orderCounts'].append(data['count'])
                
                # Sort by period
                sorted_data = sorted(zip(result['labels'], result['values'], result['orderCounts']))
                result['labels'] = [x[0] for x in sorted_data]
                result['values'] = [x[1] for x in sorted_data]
                result['orderCounts'] = [x[2] for x in sorted_data]
            
            elif period == 'yearly':
                # Retail orders
                cursor.execute('''
                    SELECT 
                        strftime('%Y', order_date) as period,
                        SUM(total_owed) as spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM retail_orders
                    WHERE order_status != 'Cancelled'
                      AND total_owed IS NOT NULL
                      AND total_owed > 0
                      AND order_date IS NOT NULL
                    GROUP BY period
                    ORDER BY period
                ''')
                for row in cursor.fetchall():
                    result['labels'].append(row['period'])
                    result['values'].append(float(row['spending'] or 0))
                    result['orderCounts'].append(row['order_count'])
                
                # Digital orders
                cursor.execute('''
                    SELECT 
                        strftime('%Y', order_date) as period,
                        SUM(our_price) as spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM digital_items
                    WHERE our_price IS NOT NULL
                      AND our_price > 0
                      AND order_date IS NOT NULL
                    GROUP BY period
                    ORDER BY period
                ''')
                digital_data = {row['period']: {'spending': float(row['spending'] or 0), 'count': row['order_count']} 
                               for row in cursor.fetchall()}
                
                for period_key, data in digital_data.items():
                    if period_key in result['labels']:
                        idx = result['labels'].index(period_key)
                        result['values'][idx] += data['spending']
                        result['orderCounts'][idx] += data['count']
                    else:
                        result['labels'].append(period_key)
                        result['values'].append(data['spending'])
                        result['orderCounts'].append(data['count'])
                
                sorted_data = sorted(zip(result['labels'], result['values'], result['orderCounts']))
                result['labels'] = [x[0] for x in sorted_data]
                result['values'] = [x[1] for x in sorted_data]
                result['orderCounts'] = [x[2] for x in sorted_data]
        
        return result
    
        """Get top products by quantity or spending"""
        products = []
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            if by == 'quantity':
                cursor.execute('''
                    SELECT 
                        product_name as name,
                        SUM(quantity) as total_quantity,
                        SUM(total_owed) as total_spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM retail_orders
                    WHERE order_status != 'Cancelled'
                      AND total_owed IS NOT NULL
                      AND total_owed > 0
                      AND product_name IS NOT NULL
                    GROUP BY product_name
                    ORDER BY total_quantity DESC
                    LIMIT ?
                ''', (limit,))
            else:  # by spending
                cursor.execute('''
                    SELECT 
                        product_name as name,
                        SUM(quantity) as total_quantity,
                        SUM(total_owed) as total_spending,
                        COUNT(DISTINCT order_id) as order_count
                    FROM retail_orders
                    WHERE order_status != 'Cancelled'
                      AND total_owed IS NOT NULL
                      AND total_owed > 0
                      AND product_name IS NOT NULL
                    GROUP BY product_name
                    ORDER BY total_spending DESC
                    LIMIT ?
                ''', (limit,))
            
            for row in cursor.fetchall():
                products.append({
                    'name': row['name'] or 'Unknown',
                    'quantity': row['total_quantity'] or 0,
                    'spending': float(row['total_spending'] or 0),
                    'orders': row['order_count'] or 0
                })
        
        return {'products': products}
    
    def get_return_stats(self):
        """Get return statistics"""
        stats = {
            'totalReturns': 0,
            'returnRate': 0,
            'returnsOverTime': {'labels': [], 'values': []}
        }
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Total returns
            cursor.execute('SELECT COUNT(*) as count FROM returns')
            row = cursor.fetchone()
            if row:
                stats['totalReturns'] = row['count']
            
            # Calculate return rate
            cursor.execute('''
                SELECT COUNT(DISTINCT order_id) as count
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
            ''')
            row = cursor.fetchone()
            total_orders = row['count'] if row else 0
            
            if total_orders > 0:
                stats['returnRate'] = (stats['totalReturns'] / total_orders) * 100
            
            # Returns over time
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m', return_creation_date) as period,
                    COUNT(*) as count
                FROM returns
                WHERE return_creation_date IS NOT NULL
                GROUP BY period
                ORDER BY period
            ''')
            
            for row in cursor.fetchall():
                stats['returnsOverTime']['labels'].append(row['period'])
                stats['returnsOverTime']['values'].append(row['count'])
        
        return stats
    
    def get_digital_vs_retail(self):
        """Compare digital vs retail orders"""
        comparison = {
            'retail': {'orders': 0, 'spending': 0},
            'digital': {'orders': 0, 'spending': 0}
        }
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Retail
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT order_id) as orders,
                    SUM(total_owed) as spending
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
            ''')
            row = cursor.fetchone()
            if row:
                comparison['retail']['orders'] = row['orders'] or 0
                comparison['retail']['spending'] = float(row['spending'] or 0)
            
            # Digital
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT order_id) as orders,
                    SUM(our_price) as spending
                FROM digital_items
                WHERE our_price IS NOT NULL
                  AND our_price > 0
            ''')
            row = cursor.fetchone()
            if row:
                comparison['digital']['orders'] = row['orders'] or 0
                comparison['digital']['spending'] = float(row['spending'] or 0)
        
        return comparison
    
    def get_digital_orders_by_category(self, category, min_price=None, max_price=None, start_date=None, end_date=None, page=1, limit=100, sort_by='order_date', sort_order='desc'):
        """Get digital orders filtered by category with price and date filters"""
        orders = []
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            where_conditions = [
                "our_price IS NOT NULL",
                "our_price > 0",
                "product_name IS NOT NULL"
            ]
            
            query_params = []
            
            if category == 'Prime Membership':
                where_conditions.append("LOWER(product_name) LIKE ?")
                query_params.append('%prime%')
            elif category == 'Paramount+':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%paramount%', '%paramount+%'])
            elif category == 'STACK TV':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%stacktv%', '%stack tv%'])
            elif category == 'Video Streaming':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?) AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ?")
                query_params.extend(['%video%', '%streaming%', '%prime%', '%paramount%'])
            elif category == 'Movies':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%movie%', '%film%'])
            elif category == 'Books & eBooks':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%book%', '%kindle%'])
            elif category == 'Music':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%music%', '%song%', '%album%'])
            elif category == 'Apps & Software':
                where_conditions.append("(LOWER(product_name) LIKE ? OR LOWER(product_name) LIKE ?)")
                query_params.extend(['%app%', '%software%'])
            elif category == 'Games':
                where_conditions.append("LOWER(product_name) LIKE ?")
                query_params.append('%game%')
            elif category == 'Other Subscriptions':
                where_conditions.append("(subscription_order_info IS NOT NULL AND subscription_order_info != 'Not Applicable' AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ?)")
                query_params.extend(['%prime%', '%paramount%', '%stacktv%', '%stack tv%'])
            elif category == 'Other Digital':
                where_conditions.append("LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND LOWER(product_name) NOT LIKE ? AND (subscription_order_info IS NULL OR subscription_order_info = 'Not Applicable')")
                query_params.extend(['%movie%', '%film%', '%book%', '%kindle%', '%music%', '%song%', '%album%', '%app%', '%software%', '%game%'])
            
            if min_price is not None:
                where_conditions.append("our_price >= ?")
                query_params.append(float(min_price))
            if max_price is not None:
                where_conditions.append("our_price <= ?")
                query_params.append(float(max_price))
            
            if start_date:
                where_conditions.append("order_date >= ?")
                query_params.append(start_date)
            if end_date:
                where_conditions.append("order_date <= ?")
                query_params.append(end_date)
            
            where_clause = " AND ".join(where_conditions)
            
            sort_column_map = {
                'order_date': 'order_date',
                'product_name': 'product_name',
                'our_price': 'our_price',
                'quantity': 'quantity_ordered',
                'order_id': 'order_id'
            }
            sort_column = sort_column_map.get(sort_by, 'order_date')
            sort_dir = 'DESC' if sort_order == 'desc' else 'ASC'
            
            cursor.execute(f'''
                SELECT COUNT(*) as count
                FROM digital_items
                WHERE {where_clause}
            ''', query_params)
            total = cursor.fetchone()['count']
            
            offset = (page - 1) * limit
            cursor.execute(f'''
                SELECT 
                    order_id, order_date, product_name, our_price as total, quantity_ordered as quantity,
                    subscription_order_info
                FROM digital_items
                WHERE {where_clause}
                ORDER BY {sort_column} {sort_dir}
                LIMIT ? OFFSET ?
            ''', query_params + [limit, offset])
            
            for row in cursor.fetchall():
                orders.append({
                    'orderId': row['order_id'] or '',
                    'date': row['order_date'] or '',
                    'productName': row['product_name'] or '',
                    'total': float(row['total'] or 0),
                    'quantity': row['quantity'] or 0,
                    'status': 'Completed',
                    'paymentMethod': 'Digital Purchase',
                    'subscriptionInfo': row['subscription_order_info'] or '',
                })
        
        return {
            'orders': orders,
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }

    def get_retail_breakdown(self):
        """Get retail-specific breakdowns"""
        breakdown = {
            'categories': [],
            'topProducts': [],
            'spendingOverTime': {'labels': [], 'values': []},
            'paymentMethods': []
        }
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Categories (reuse existing logic but filter for retail only)
            category_keywords = {
                'Electronics': ['battery', 'charger', 'headphone', 'earbud', 'cable', 'wireless', 'led', 'display', 'screen', 
                               'monitor', 'keyboard', 'mouse', 'router', 'wifi', 'ethernet', 'speaker', 'amplifier', 
                               'kindle', 'e-reader', 'chromebook', 'laptop', 'computer', 'hard drive', 'external drive',
                               'smart lock', 'smart home', 'security camera', 'nvr', 'camera system'],
                'Mobile Devices': ['iphone', 'ipad', 'smartphone', 'tablet', 'apple watch', 'smartwatch', 
                                  'smart watch', 'huawei watch', 'samsung phone', 'google pixel', 'oura ring'],
                'Photography': ['lens', 'canon ef', 'canon ef-', 'canon ef-m', 'sigma', 'photography', 
                               'dslr', 'mirrorless', 'camcorder', 'vixia', 'powershot', 'eos', 
                               'viewfinder', 'camera lens'],
                'Gaming': ['playstation', 'nintendo', 'xbox', 'switch', 'ps4', 'ps5', 'wii', 'game console', 
                          'gamepad', 'controller', 'video game', 'gaming'],
                'Clothing': ['shirt', 'jacket', 'hoodie', 'pants', 'dress', 'shoes', 'socks', 'clothing', 'apparel',
                            'slipper', 'boot', 'sunglasses', 'glasses', 'rain jacket', 'raincoat'],
                'Home & Kitchen': ['cabinet', 'organizer', 'storage', 'container', 'mattress', 'bedding', 
                                  'curtain', 'drape', 'coffee maker', 'coffee brewer', 'nespresso', 
                                  'moccamaster', 'blender', 'vitamix', 'pasta maker', 'smoker', 
                                  'air conditioner', 'vacuum', 'roomba', 'dyson', 'air purifier', 
                                  'hepa', 'popcorn machine', 'aerogarden', 'chicken coop door'],
                'Tools & Garden': ['lawn mower', 'lawn sweepr', 'string trimmer', 'chipper', 'shredder', 
                                  'fence', 'mesh', 'generator', 'tool', 'garden', 'yard', 'landscaping', 
                                  'arborist', 'utility cart', 'garden cart'],
                'Pet Supplies': ['dog food', 'cat food', 'pet food', 'chicken feed', 'layer pellets', 'layer pellet',
                                'mixed grains scratch', 'goat feed', 'goat snax', 'pet treat', 'bully stick', 
                                'dog chew', 'dog treat', 'animal feed', 'feed for', 'dog chews'],
                'Food & Groceries': ['pancake mix', 'food', 'grocery', 'ingredient', 'spice', 'seasoning'],
                'Fitness Equipment': ['elliptical', 'treadmill', 'walking pad', 'exercise', 'fitness', 'gym',
                                     'weights', 'yoga', 'workout', 'dumbbell'],
                'Beauty & Personal Care': ['makeup', 'cosmetic', 'beauty', 'skincare', 'shampoo', 'soap',
                                           'hair mask', 'hair growth', 'toothbrush', 'sonicare', 'oral-b',
                                           'laser hair', 'jewelry polisher'],
                'Sports & Outdoors': ['sport', 'outdoor', 'camping', 'hiking', 'tent', 'backpack', 'paddle',
                                     'sup', 'paddleboard', 'volleyball', 'badminton', 'trampoline'],
                'Toys & Games': ['toy', 'game', 'lego', 'puzzle', 'board game', 'building kit', 'playset'],
                'Health & Wellness': ['vitamin', 'supplement', 'health', 'wellness', 'fitness', 'electrolyte',
                                     'multivitamin', 'gummy vitamin', 'dna test', '23andme', 'protein'],
                'Baby & Kids': ['car seat', 'booster seat', 'booster', 'baby', 'infant', 'toddler', 'stroller', 'diaper'],
                'Automotive': ['truck', 'vehicle', 'automotive', 'auto tire', 'auto oil', 'car tire', 'car oil'],
                'Services': ['hire', 'service', 'arborist']
            }
            
            categories = defaultdict(float)
            cursor.execute('''
                SELECT product_name, SUM(total_owed) as spending
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
                  AND product_name IS NOT NULL
                GROUP BY product_name
            ''')
            
            category_order = [
                'Baby & Kids', 'Pet Supplies', 'Mobile Devices', 'Photography', 'Gaming', 
                'Fitness Equipment', 'Tools & Garden', 'Food & Groceries', 'Services', 'Automotive',
                'Electronics', 'Home & Kitchen', 'Clothing', 'Beauty & Personal Care',
                'Sports & Outdoors', 'Toys & Games', 'Health & Wellness', 'Books & Media'
            ]
            
            for row in cursor.fetchall():
                product_name = (row['product_name'] or '').lower()
                category_found = False
                
                for category in category_order:
                    if category in category_keywords:
                        keywords = category_keywords[category]
                        if any(keyword in product_name for keyword in keywords):
                            categories[category] += float(row['spending'] or 0)
                            category_found = True
                            break
                
                if not category_found:
                    for category, keywords in category_keywords.items():
                        if category not in category_order:
                            if any(keyword in product_name for keyword in keywords):
                                categories[category] += float(row['spending'] or 0)
                                category_found = True
                                break
                
                if not category_found:
                    categories['Other'] += float(row['spending'] or 0)
            
            breakdown['categories'] = [{'name': k, 'spending': v} for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)]
            
            # Top products
            cursor.execute('''
                SELECT 
                    product_name as name,
                    SUM(quantity) as total_quantity,
                    SUM(total_owed) as total_spending,
                    COUNT(DISTINCT order_id) as order_count
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
                  AND product_name IS NOT NULL
                GROUP BY product_name
                ORDER BY total_spending DESC
                LIMIT 15
            ''')
            
            for row in cursor.fetchall():
                breakdown['topProducts'].append({
                    'name': row['name'] or 'Unknown',
                    'quantity': row['total_quantity'] or 0,
                    'spending': float(row['total_spending'] or 0),
                    'orders': row['order_count'] or 0
                })
            
            # Spending over time (monthly)
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m', order_date) as period,
                    SUM(total_owed) as spending
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
                  AND order_date IS NOT NULL
                GROUP BY period
                ORDER BY period
            ''')
            
            for row in cursor.fetchall():
                breakdown['spendingOverTime']['labels'].append(row['period'])
                breakdown['spendingOverTime']['values'].append(float(row['spending'] or 0))
            
            # Payment methods
            cursor.execute('''
                SELECT 
                    payment_instrument_type as method,
                    SUM(total_owed) as spending
                FROM retail_orders
                WHERE order_status != 'Cancelled'
                  AND total_owed IS NOT NULL
                  AND total_owed > 0
                  AND payment_instrument_type IS NOT NULL
                GROUP BY payment_instrument_type
                ORDER BY spending DESC
            ''')
            
            for row in cursor.fetchall():
                breakdown['paymentMethods'].append({
                    'method': row['method'] or 'Unknown',
                    'spending': float(row['spending'] or 0)
                })
        
        return breakdown
    
    def get_digital_breakdown(self):
        """Get digital-specific breakdowns"""
        breakdown = {
            'categories': [],
            'topProducts': [],
            'spendingOverTime': {'labels': [], 'values': []},
            'subscriptions': []
        }
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Digital categories
            digital_categories = defaultdict(float)
            cursor.execute('''
                SELECT product_name, SUM(our_price) as spending, subscription_order_info
                FROM digital_items
                WHERE our_price IS NOT NULL
                  AND our_price > 0
                  AND product_name IS NOT NULL
                GROUP BY product_name, subscription_order_info
            ''')
            
            for row in cursor.fetchall():
                product_name = (row['product_name'] or '').lower()
                subscription_info = row['subscription_order_info'] or ''
                spending = float(row['spending'] or 0)
                
                # Categorize digital items
                if 'subscription' in subscription_info.lower() or 'subscription' in product_name:
                    if 'prime' in product_name:
                        digital_categories['Prime Membership'] += spending
                    elif 'paramount' in product_name or 'paramount+' in product_name:
                        digital_categories['Paramount+'] += spending
                    elif 'stacktv' in product_name or 'stack tv' in product_name:
                        digital_categories['STACK TV'] += spending
                    elif 'video' in product_name or 'streaming' in product_name:
                        digital_categories['Video Streaming'] += spending
                    else:
                        digital_categories['Other Subscriptions'] += spending
                elif 'movie' in product_name or 'film' in product_name:
                    digital_categories['Movies'] += spending
                elif 'book' in product_name or 'kindle' in product_name:
                    digital_categories['Books & eBooks'] += spending
                elif 'music' in product_name or 'song' in product_name or 'album' in product_name:
                    digital_categories['Music'] += spending
                elif 'app' in product_name or 'software' in product_name:
                    digital_categories['Apps & Software'] += spending
                elif 'game' in product_name:
                    digital_categories['Games'] += spending
                else:
                    digital_categories['Other Digital'] += spending
            
            breakdown['categories'] = [{'name': k, 'spending': v} for k, v in sorted(digital_categories.items(), key=lambda x: x[1], reverse=True)]
            
            # Top products
            cursor.execute('''
                SELECT 
                    product_name as name,
                    SUM(quantity_ordered) as total_quantity,
                    SUM(our_price) as total_spending,
                    COUNT(DISTINCT order_id) as order_count
                FROM digital_items
                WHERE our_price IS NOT NULL
                  AND our_price > 0
                  AND product_name IS NOT NULL
                GROUP BY product_name
                ORDER BY total_spending DESC
                LIMIT 15
            ''')
            
            for row in cursor.fetchall():
                breakdown['topProducts'].append({
                    'name': row['name'] or 'Unknown',
                    'quantity': row['total_quantity'] or 0,
                    'spending': float(row['total_spending'] or 0),
                    'orders': row['order_count'] or 0
                })
            
            # Spending over time (monthly)
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m', order_date) as period,
                    SUM(our_price) as spending
                FROM digital_items
                WHERE our_price IS NOT NULL
                  AND our_price > 0
                  AND order_date IS NOT NULL
                GROUP BY period
                ORDER BY period
            ''')
            
            for row in cursor.fetchall():
                breakdown['spendingOverTime']['labels'].append(row['period'])
                breakdown['spendingOverTime']['values'].append(float(row['spending'] or 0))
            
            # Subscriptions (items with subscription info)
            cursor.execute('''
                SELECT 
                    product_name,
                    subscription_order_info,
                    SUM(our_price) as spending,
                    COUNT(*) as count
                FROM digital_items
                WHERE our_price IS NOT NULL
                  AND our_price > 0
                  AND subscription_order_info IS NOT NULL
                  AND subscription_order_info != 'Not Applicable'
                GROUP BY product_name, subscription_order_info
                ORDER BY spending DESC
                LIMIT 20
            ''')
            
            for row in cursor.fetchall():
                breakdown['subscriptions'].append({
                    'name': row['product_name'] or 'Unknown',
                    'subscriptionId': row['subscription_order_info'],
                    'spending': float(row['spending'] or 0),
                    'count': row['count']
                })
        
        return breakdown
    
    def get_orders_by_category(self, category, min_price=None, max_price=None, start_date=None, end_date=None, page=1, limit=100, sort_by='order_date', sort_order='desc'):
        """Get orders filtered by category with price and date filters"""
        orders = []
        
        # Map category to keywords
        category_keywords = {
            'Electronics': ['battery', 'charger', 'headphone', 'earbud', 'cable', 'wireless', 'led', 'display', 'screen', 
                           'monitor', 'keyboard', 'mouse', 'router', 'wifi', 'ethernet', 'speaker', 'amplifier', 
                           'kindle', 'e-reader', 'chromebook', 'laptop', 'computer', 'hard drive', 'external drive',
                           'smart lock', 'smart home', 'security camera', 'nvr', 'camera system'],
            'Mobile Devices': ['iphone', 'ipad', 'smartphone', 'tablet', 'apple watch', 'smartwatch', 
                              'smart watch', 'huawei watch', 'samsung phone', 'google pixel', 'oura ring'],
            'Photography': ['lens', 'canon ef', 'canon ef-', 'canon ef-m', 'sigma', 'photography', 
                           'dslr', 'mirrorless', 'camcorder', 'vixia', 'powershot', 'eos', 
                           'viewfinder', 'camera lens'],
            'Gaming': ['playstation', 'nintendo', 'xbox', 'switch', 'ps4', 'ps5', 'wii', 'game console', 
                      'gamepad', 'controller', 'video game', 'gaming'],
            'Clothing': ['shirt', 'jacket', 'hoodie', 'pants', 'dress', 'shoes', 'socks', 'clothing', 'apparel',
                        'slipper', 'boot', 'sunglasses', 'glasses', 'rain jacket', 'raincoat'],
            'Home & Kitchen': ['cabinet', 'organizer', 'storage', 'container', 'mattress', 'bedding', 
                              'curtain', 'drape', 'coffee maker', 'coffee brewer', 'nespresso', 
                              'moccamaster', 'blender', 'vitamix', 'pasta maker', 'smoker', 
                              'air conditioner', 'vacuum', 'roomba', 'dyson', 'air purifier', 
                              'hepa', 'popcorn machine', 'aerogarden', 'chicken coop door'],
            'Tools & Garden': ['lawn mower', 'lawn sweepr', 'string trimmer', 'chipper', 'shredder', 
                              'fence', 'mesh', 'generator', 'tool', 'garden', 'yard', 'landscaping', 
                              'arborist', 'utility cart', 'garden cart'],
            'Pet Supplies': ['dog food', 'cat food', 'pet food', 'chicken feed', 'layer pellets', 'layer pellet',
                            'mixed grains scratch', 'goat feed', 'goat snax', 'pet treat', 'bully stick', 
                            'dog chew', 'dog treat', 'animal feed', 'feed for', 'dog chews'],
            'Food & Groceries': ['pancake mix', 'food', 'grocery', 'ingredient', 'spice', 'seasoning'],
            'Fitness Equipment': ['elliptical', 'treadmill', 'walking pad', 'exercise', 'fitness', 'gym',
                                 'weights', 'yoga', 'workout', 'dumbbell'],
            'Beauty & Personal Care': ['makeup', 'cosmetic', 'beauty', 'skincare', 'shampoo', 'soap',
                                       'hair mask', 'hair growth', 'toothbrush', 'sonicare', 'oral-b',
                                       'laser hair', 'jewelry polisher'],
            'Sports & Outdoors': ['sport', 'outdoor', 'camping', 'hiking', 'tent', 'backpack', 'paddle',
                                 'sup', 'paddleboard', 'volleyball', 'badminton', 'trampoline'],
            'Toys & Games': ['toy', 'game', 'lego', 'puzzle', 'board game', 'building kit', 'playset'],
            'Health & Wellness': ['vitamin', 'supplement', 'health', 'wellness', 'fitness', 'electrolyte',
                                 'multivitamin', 'gummy vitamin', 'dna test', '23andme', 'protein'],
            'Baby & Kids': ['car seat', 'booster seat', 'booster', 'baby', 'infant', 'toddler', 'stroller', 'diaper'],
            'Automotive': ['truck', 'vehicle', 'automotive', 'auto tire', 'auto oil', 'car tire', 'car oil'],
            'Services': ['hire', 'service', 'arborist']
        }
        
        keywords = category_keywords.get(category, [])
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Build WHERE clause
            where_conditions = [
                "order_status != 'Cancelled'",
                "total_owed IS NOT NULL",
                "total_owed > 0",
                "product_name IS NOT NULL"
            ]
            
            # Category filter - build LIKE conditions for keywords
            query_params = []
            if keywords:
                # Build parameterized query for keywords
                keyword_placeholders = " OR ".join([f"LOWER(product_name) LIKE ?" for _ in keywords])
                where_conditions.append(f"({keyword_placeholders})")
                query_params.extend([f"%{keyword}%" for keyword in keywords])
            elif category == 'Other':
                # For "Other", exclude all known categories
                all_keywords = []
                for cats in category_keywords.values():
                    all_keywords.extend(cats)
                keyword_placeholders = " AND ".join([f"LOWER(product_name) NOT LIKE ?" for _ in all_keywords])
                where_conditions.append(f"({keyword_placeholders})")
                query_params.extend([f"%{keyword}%" for keyword in all_keywords])
            
            # Price filters
            if min_price is not None:
                where_conditions.append("total_owed >= ?")
                query_params.append(float(min_price))
            if max_price is not None:
                where_conditions.append("total_owed <= ?")
                query_params.append(float(max_price))
            
            # Date filters
            if start_date:
                where_conditions.append("order_date >= ?")
                query_params.append(start_date)
            if end_date:
                where_conditions.append("order_date <= ?")
                query_params.append(end_date)
            
            where_clause = " AND ".join(where_conditions)
            
            # Sort column mapping
            sort_column_map = {
                'order_date': 'order_date',
                'product_name': 'product_name',
                'total_owed': 'total_owed',
                'quantity': 'quantity',
                'order_id': 'order_id'
            }
            sort_column = sort_column_map.get(sort_by, 'order_date')
            sort_dir = 'DESC' if sort_order == 'desc' else 'ASC'
            
            # Get total count
            cursor.execute(f'''
                SELECT COUNT(*) as count
                FROM retail_orders
                WHERE {where_clause}
            ''', query_params)
            total = cursor.fetchone()['count']
            
            # Get paginated orders
            offset = (page - 1) * limit
            # Note: sort_column and sort_dir are safe because they're validated against a whitelist
            cursor.execute(f'''
                SELECT 
                    order_id, order_date, product_name, total_owed, quantity,
                    order_status, payment_instrument_type, asin
                FROM retail_orders
                WHERE {where_clause}
                ORDER BY {sort_column} {sort_dir}
                LIMIT ? OFFSET ?
            ''', query_params + [limit, offset])
            
            for row in cursor.fetchall():
                orders.append({
                    'orderId': row['order_id'] or '',
                    'date': row['order_date'] or '',
                    'productName': row['product_name'] or '',
                    'total': float(row['total_owed'] or 0),
                    'quantity': row['quantity'] or 0,
                    'status': row['order_status'] or '',
                    'paymentMethod': row['payment_instrument_type'] or '',
                    'asin': row['asin'] or '',
                })
        
        return {
            'orders': orders,
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
