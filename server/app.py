#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return ""


@app.route("/campers", methods=["GET"])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers])


@app.route("/campers/<int:id>", methods=["GET"])
def get_camper(id):
    camper = Camper.query.get(id)
    if camper:
        camper_data = camper.to_dict()
        camper_data["signups"] = [
            signup.to_dict(rules=("-camper", "activity")) for signup in camper.signups
        ]
        return jsonify(camper_data)
    else:
        return jsonify({"error": "Camper not found"}), 404


@app.route("/campers", methods=["POST"])
def create_camper():
    data = request.get_json()
    try:
        camper = Camper(name=data["name"], age=data["age"])
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400


@app.route("/campers/<int:id>", methods=["PATCH"])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json()
    try:
        if "name" in data:
            camper.name = data["name"]
        if "age" in data:
            camper.age = data["age"]
        db.session.commit()
        return jsonify(camper.to_dict(rules=("-signups",))), 202
    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route("/activities", methods=["GET"])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict(rules=("-signups",)) for activity in activities])


@app.route("/activities/<int:id>", methods=["DELETE"])
def delete_activity(id):
    activity = Activity.query.get(id)
    if activity:
        try:
            db.session.delete(activity)
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Activity not found"}), 404


@app.route("/signups", methods=["POST"])
def create_signup():
    data = request.get_json()
    try:
        camper = Camper.query.get(data.get("camper_id"))
        activity = Activity.query.get(data.get("activity_id"))
        if not camper or not activity:
            return jsonify({"errors": ["Camper or Activity not found"]}), 400

        signup = Signup(
            camper_id=camper.id, activity_id=activity.id, time=data.get("time")
        )
        db.session.add(signup)
        db.session.commit()

        response_data = signup.to_dict()
        response_data["activity"] = signup.activity.to_dict(rules=("-signups",))
        response_data["camper"] = signup.camper.to_dict(rules=("-signups",))
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
