from flask import Blueprint, request, jsonify
from app.models.product_model import Product
from app.views.product_view import render_product_list, render_product_detail
from app.utils.decorator import jwt_required, roles_required

producto_bp = Blueprint("product", __name__)

@producto_bp.route("/products", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_products():
    products = Product.query.all()
    return jsonify(render_product_list(products)), 200

@producto_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(render_product_detail(product)), 200

@producto_bp.route("/products", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    
    if(not name or not description or not price or stock is None):
        return jsonify({"error": "Faltan datos"}), 400
    
    product = Product(name=name, description=description, price=price, stock=stock)
    product.save()
    return jsonify(render_product_detail(product)), 201

@producto_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    
    product.update(name=name, description=description, price=price, stock=stock) 

    return jsonify(render_product_detail(product))  

@producto_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    product.delete()
    return "", 204