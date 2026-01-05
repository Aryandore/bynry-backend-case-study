from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref='warehouses')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=10)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    quantity = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref='inventories')
    warehouse = db.relationship('Warehouse', backref='inventories')

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))

class ProductSupplier(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), primary_key=True)
