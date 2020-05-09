from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from classes.abstract_construction_goods import AbstractConstructionGoods
from classes.state import State
import os
import json
import copy

with open('secret.json') as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"]
)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Door(AbstractConstructionGoods, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer_name = db.Column(db.String(32), unique=False)
    price_in_uah = db.Column(db.Integer, unique=False)
    color = db.Column(db.String(32), unique=False)
    weight_in_kilograms = db.Column(db.Integer, unique=False)
    length_in_centimeters = db.Column(db.Integer, unique=False)
    width_in_centimeters = db.Column(db.Integer, unique=False)
    state = db.Column(db.String(32), unique=False)
    wood_type = db.Column(db.String(32), unique=False)
    purpose = db.Column(db.String(32), unique=False)
    _connection_protocol = db.Column(db.String(32), unique=False)
    _data_transfer_amount = db.Column(db.Float, unique=False)

    def __init__(self, producer_name='Ukraine', price_in_uah=900, color='red', weight_in_kilograms=0,
                 length_in_centimeters=0, width_in_centimeters=0, state=State.NEW, wood_type='mahogany',
                 purpose='office', connection_protocol='telnet', data_transfer_amount=0.0):
        super().__init__(producer_name, price_in_uah, color, weight_in_kilograms,
                         length_in_centimeters, width_in_centimeters, state)
        self.wood_type = wood_type
        self.purpose = purpose
        self._connection_protocol = connection_protocol
        self._data_transfer_amount = data_transfer_amount


class DoorSchema(ma.Schema):
    class Meta:
        fields = ('producer_name', 'price_in_uah', 'color', 'weight_in_kilograms',
                  'length_in_centimeters', 'width_in_centimeters', 'state',
                  'wood_type', 'purpose', '_connection_protocol',
                  '_data_transfer_amount')


door_schema = DoorSchema()
doors_schema = DoorSchema(many=True)


@app.route("/door", methods=["POST"])
def create_door():
    door = Door(request.json['producer_name'],
                request.json['price_in_uah'],
                request.json['color'],
                request.json['weight_in_kilograms'],
                request.json['length_in_centimeters'],
                request.json['width_in_centimeters'],
                request.json['state'],
                request.json['wood_type'],
                request.json['purpose'],
                request.json['connection_protocol'],
                request.json['data_transfer_amount'])
    db.session.add(door)
    db.session.commit()
    return door_schema.jsonify(door)


@app.route("/door", methods=["GET"])
def get_doors():
    doors_list = Door.query.all()
    result = doors_schema.dump(doors_list)
    return jsonify({'doors': result})


@app.route("/door/<door_id>", methods=["GET"])
def get_door_by_id(door_id: int):
    door = Door.query.get(door_id)
    if not door:
        abort(404)
    else:
        return door_schema.jsonify(door)


@app.route("/door/<door_id>", methods=["PUT"])
def update_door(door_id: int):
    door = Door.query.get(door_id)
    if not door:
        abort(404)
    else:
        old_door = copy.deepcopy(door)
        door.producer_name = request.json['producer_name']
        door.price_in_uah = request.json['price_in_uah']
        door.color = request.json['color']
        door.weight_in_kilograms = request.json['weight_in_kilograms']
        door.length_in_centimeters = request.json['length_in_centimeters']
        door.width_in_centimeters = request.json['width_in_centimeters']
        door.state = request.json['state']
        door.wood_type = request.json['wood_type']
        door.purpose = request.json['purpose']
        door._connection_protocol = request.json_module['connection_protocol']
        door._data_transfer_amount = request.json['data_transfer_amount']
        db.session.commit()
        return door_schema.jsonify(old_door)


@app.route("/door/<door_id>", methods=["DELETE"])
def delete_door_by_id(door_id: int):
    door = Door.query.get(door_id)
    if not door:
        abort(404)
    else:
        db.session.delete(door)
        db.session.commit()
        return door_schema.jsonify(door)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='127.0.0.1')
