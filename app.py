from flask import Flask, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

class Inventory(db.Model):
    __tablename__='inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    barcode = db.Column(db.Integer)

    def serializer(self):
        return {"id":self.id, "name":self.name, "category":self.category, "price":self.price, "quantity":self.quantity, "barcode":self.barcode}

db.create_all()



@app.route('/inventory/item', methods=['GET', 'POST'])
def get_all():
    if request.method == 'GET':
        items = Inventory.query.all()
        res = [item.serializer() for item in items]
        return jsonify(res), 200

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        barcode = request.form['barcode']

        item = Inventory(name=name, category=category, price=price, quantity=quantity, barcode=barcode)

        db.session.add(item)
        db.session.commit()

        item = Inventory.query.get(item.id)
        res = jsonify(item.serializer())

        return res, 201


@app.route('/inventory/item/<int:barcode>', methods=['DELETE', 'PUT'])
def barcode(barcode):
    item = Inventory.query.filter_by(barcode=barcode).first()
    if request.method == 'DELETE':
        if item is not None:
            db.session.delete(item)
            db.session.commit()
            return [], 200
        else:
            print('Item not found')
            abort(404)

    if request.method == 'PUT':
        if item is not None:
            db.session.delete(item)
            db.session.commit()

            name = request.form['name']
            category = request.form['category']
            price = request.form['price']
            quantity = request.form['quantity']
            barcode = request.form['barcode']

            item = Inventory(name=name, category=category, price=price, quantity=quantity, barcode=barcode)

            db.session.add(item)
            db.session.commit()

            return jsonify(item.serializer()), 200
        else:
            return None, 404


# query parameters
@app.route('/inventory/item/query', methods=['GET'])
def get_by_category():
    category = request.args.get("category", type=str)
    items = Inventory.query.filter_by(category=category)
    if items:
        res = [item.serializer() for item in items]
        return jsonify(res), 200
    else:
        return []


if __name__=='__main__':
    app.run(debug=True)
