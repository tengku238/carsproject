from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse

# --- Flask setup ---
app = Flask(__name__)
api = Api(app)

# --- Database setup ---
db = SqliteDatabase('carsweb.db')


class BaseModel(Model):
    class Meta:
        database = db


class TBCarsWeb(BaseModel):
    carname = TextField(unique=True)
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()


# --- Utility: Create table if not exist ---
def create_tables():
    with db:
        db.create_tables([TBCarsWeb])


@app.route('/')
def home():
    return jsonify({"message": "🚗 Car Web Service Ready", "status": "ok"})


@app.route('/read')
def read_all():
    """Simple route for debugging"""
    rows = list(TBCarsWeb.select().dicts())
    return jsonify(rows)


# --- RESTful Resource ---
class CAR(Resource):

    # --- GET: tampilkan semua data ---
    def get(self):
        rows = list(TBCarsWeb.select().dicts())
        return jsonify(rows)

    # --- POST: tambah data ---
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('carname', required=True, help="Car name is required.")
        parser.add_argument('carbrand', required=True)
        parser.add_argument('carmodel', required=True)
        parser.add_argument('carprice', required=True)
        args = parser.parse_args()

        try:
            car = TBCarsWeb.create(
                carname=args['carname'],
                carbrand=args['carbrand'],
                carmodel=args['carmodel'],
                carprice=args['carprice']
            )
            return jsonify({
                "message": "✅ Car successfully added!",
                "car": {
                    "id": car.id,
                    "carname": car.carname,
                    "carbrand": car.carbrand,
                    "carmodel": car.carmodel,
                    "carprice": car.carprice
                }
            })
        except IntegrityError:
            return jsonify({"error": f"⚠️ Car '{args['carname']}' already exists."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- PUT: update data berdasarkan carname ---
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('carname', required=True, help="Car name is required to update data.")
        parser.add_argument('carbrand')
        parser.add_argument('carmodel')
        parser.add_argument('carprice')
        args = parser.parse_args()

        try:
            car = TBCarsWeb.get_or_none(TBCarsWeb.carname == args['carname'])
            if not car:
                return jsonify({"error": f"⚠️ Car '{args['carname']}' not found."}), 404

            if args['carbrand']:
                car.carbrand = args['carbrand']
            if args['carmodel']:
                car.carmodel = args['carmodel']
            if args['carprice']:
                car.carprice = args['carprice']
            car.save()

            return jsonify({
                "message": f"✅ Car '{args['carname']}' updated successfully!",
                "car": {
                    "id": car.id,
                    "carname": car.carname,
                    "carbrand": car.carbrand,
                    "carmodel": car.carmodel,
                    "carprice": car.carprice
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- DELETE: hapus berdasarkan carname ---
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('carname', required=True, help="Car name is required.")
        args = parser.parse_args()

        deleted = TBCarsWeb.delete().where(TBCarsWeb.carname == args['carname']).execute()

        if deleted:
            return jsonify({"message": f"🗑️ Car '{args['carname']}' deleted successfully!"})
        else:
            return jsonify({"error": f"⚠️ Car '{args['carname']}' not found."}), 404


# --- RESTful Resource untuk Search berdasarkan nama mobil ---
class CAR_SEARCH(Resource):
    def get(self, carname):
        car = TBCarsWeb.get_or_none(TBCarsWeb.carname == carname)
        if not car:
            return jsonify({"error": f"⚠️ Car '{carname}' not found."}), 404
        return jsonify({
            "id": car.id,
            "carname": car.carname,
            "carbrand": car.carbrand,
            "carmodel": car.carmodel,
            "carprice": car.carprice
        })


# --- Tambahkan Resource ke API ---
api.add_resource(CAR, '/cars/', endpoint="cars")
api.add_resource(CAR_SEARCH, '/cars/<string:carname>', endpoint="car_search")

# --- Main ---
if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', debug=True, port=5012)
