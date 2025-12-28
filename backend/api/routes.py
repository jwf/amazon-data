from flask import jsonify, request
from . import api_bp
import sys
import os
# Add parent directory to path to import data_processor
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
from data_processor import DataProcessor

processor = DataProcessor()

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@api_bp.route('/stats/summary', methods=['GET'])
def get_summary():
    """Get overall statistics summary"""
    return jsonify(processor.get_summary())

@api_bp.route('/stats/spending-over-time', methods=['GET'])
def get_spending_over_time():
    """Get spending over time (monthly/yearly)"""
    period = request.args.get('period', 'monthly')  # monthly or yearly
    return jsonify(processor.get_spending_over_time(period))

@api_bp.route('/stats/top-products', methods=['GET'])
def get_top_products():
    """Get top products by quantity or spending"""
    limit = int(request.args.get('limit', 20))
    by = request.args.get('by', 'quantity')  # quantity or spending
    return jsonify(processor.get_top_products(limit, by))

@api_bp.route('/stats/categories', methods=['GET'])
def get_categories():
    """Get spending by category (attempted from product names)"""
    return jsonify(processor.get_category_breakdown())

@api_bp.route('/stats/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get spending by payment method"""
    return jsonify(processor.get_payment_method_breakdown())

@api_bp.route('/stats/returns', methods=['GET'])
def get_returns():
    """Get return statistics"""
    return jsonify(processor.get_return_stats())

@api_bp.route('/stats/digital-vs-retail', methods=['GET'])
def get_digital_vs_retail():
    """Compare digital vs retail orders"""
    return jsonify(processor.get_digital_vs_retail())

@api_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get paginated order list"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    return jsonify(processor.get_orders(page, limit))

@api_bp.route('/stats/retail-breakdown', methods=['GET'])
def get_retail_breakdown():
    """Get retail-specific breakdowns"""
    return jsonify(processor.get_retail_breakdown())

@api_bp.route('/stats/digital-breakdown', methods=['GET'])
def get_digital_breakdown():
    """Get digital-specific breakdowns"""
    return jsonify(processor.get_digital_breakdown())

@api_bp.route('/orders/by-category', methods=['GET'])
def get_orders_by_category():
    """Get retail orders filtered by category with optional price and date filters"""
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    sort_by = request.args.get('sort_by', 'order_date')
    sort_order = request.args.get('sort_order', 'desc')
    
    return jsonify(processor.get_orders_by_category(
        category, min_price, max_price, start_date, end_date, page, limit, sort_by, sort_order
    ))

@api_bp.route('/digital-orders/by-category', methods=['GET'])
def get_digital_orders_by_category():
    """Get digital orders filtered by category with optional price and date filters"""
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    sort_by = request.args.get('sort_by', 'order_date')
    sort_order = request.args.get('sort_order', 'desc')
    
    return jsonify(processor.get_digital_orders_by_category(
        category, min_price, max_price, start_date, end_date, page, limit, sort_by, sort_order
    ))
