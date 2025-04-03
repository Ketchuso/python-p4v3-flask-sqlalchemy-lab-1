# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/earthquakes/<int:id>', methods=["GET"])
def index(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

    body = {
        'id': earthquake.id,
        'location' : f'{earthquake.location}',
        'magnitude' : earthquake.magnitude,
        'year' : earthquake.year
    }
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=["GET"])
def size(magnitude):
    quake_list = []
    earthquakes = Earthquake.query.filter(Earthquake.magnitude > magnitude).all()
    if not earthquakes:  
        return jsonify({
            "count": 0,
            "quakes": []
        })

    quake_list = [quake.to_dict() for quake in earthquakes]
    
    return jsonify({
        "count": len(quake_list),
        "quakes": quake_list
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
