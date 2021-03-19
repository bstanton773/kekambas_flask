from . import bp as shop
from .models import Product
from flask import jsonify, request


@shop.route('/products')
def products():
    """
    [GET] /shop/products
    """
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@shop.route('/products/<int:id>')
def single_product(id):
    """
    [GET] /shop/products/<id>
    """
    p = Product.query.get_or_404(id)
    return jsonify(p.to_dict())

@shop.route('test', methods=['POST'])
def test():
    print(request.json)
    return jsonify(request.json)
