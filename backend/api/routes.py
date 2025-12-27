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
