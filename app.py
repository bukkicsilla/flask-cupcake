"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Denali National PArk"

connect_db(app)

@app.route("/")
def home():
    return "CUPCAKES ARE DELICIOUS!"

@app.route("/api/cupcakes")
def list_cupcakes():
    """List of all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Show a single cupcake."""
    single_cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=single_cupcake.serialize())

@app.route("/api/cupcakes", methods=['POST'])
def create_cupcake():
    """Create a new cupcake and save in the database."""
    data = request.json
    new_cupcake = Cupcake(flavor=data.get("flavor", "plain"), size=data.get("size", "small"), rating=data.get("rating", "5"), image=data.get("image", "https://tinyurl.com/demo-cupcake"))
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.serialize()), 201

@app.route("/api/cupcakes/<int:id>", methods=['PATCH'])
def update_cupcake(id):
    """Update a single cupcake based on id."""
    cupcake_to_update = Cupcake.query.get_or_404(id)
    data = request.json
    #one way
    #db.session.query(Cupcake).filter_by(id=id).update(data)
    #another way
    cupcake_to_update.flavor = data.get("flavor", cupcake_to_update.flavor)
    cupcake_to_update.size = data.get("size", cupcake_to_update.size)
    cupcake_to_update.rating = data.get("rating", cupcake_to_update.rating)
    cupcake_to_update.image = data.get("image", cupcake_to_update.image)
    db.session.commit()
    return jsonify(cupcake=cupcake_to_update.serialize())

@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def delete_cupcake(id):
    """Delete a single cupcake."""
    cupcake_to_delete = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake_to_delete)
    db.session.commit()
    return jsonify(message="Deleted")
