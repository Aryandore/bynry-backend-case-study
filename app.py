from flask import Flask, request, jsonify
from models import db, Product, Inventory, Warehouse, Supplier, ProductSupplier

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Create Product Endpoint
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required_fields:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    if Product.query.filter_by(sku=data['sku']).first():
        return {"error": "SKU already exists"}, 409

    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price']
    )
    db.session.add(product)
    db.session.flush()

    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )
    db.session.add(inventory)
    db.session.commit()
    return {"message": "Product created", "product_id": product.id}, 201

# Low-stock Alerts Endpoint
@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []
    inventories = Inventory.query.join(Warehouse)\
        .filter(Warehouse.company_id == company_id).all()

    for inv in inventories:
        product = inv.product
        if inv.quantity >= product.low_stock_threshold:
            continue

        supplier = ProductSupplier.query.filter_by(product_id=product.id).first()
        supplier_info = None
        if supplier:
            s = Supplier.query.get(supplier.supplier_id)
            supplier_info = {"id": s.id, "name": s.name, "contact_email": s.contact_email}

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": inv.warehouse_id,
            "warehouse_name": inv.warehouse.name,
            "current_stock": inv.quantity,
            "threshold": product.low_stock_threshold,
            "supplier": supplier_info
        })

    return jsonify({"alerts": alerts, "total_alerts": len(alerts)})

if __name__ == '__main__':
    app.run(debug=True)
