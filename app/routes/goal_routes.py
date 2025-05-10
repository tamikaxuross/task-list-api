from flask import Blueprint, request, jsonify, Response
from app.models.goal import Goal
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# CREATE a goal
@bp.post("")
def create_goal():
    data = request.get_json()

    if "title" not in data:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(data)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# GET all goals
@bp.get("")
def get_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

# GET one goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    return jsonify({"goal": goal.to_dict()})

# UPDATE a goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    data = request.get_json()
    if "title" not in data:
        return jsonify({"details": "Invalid data"}), 400

    goal.title = data["title"]
    db.session.commit()
    return jsonify({"goal": goal.to_dict()})

# DELETE a goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

