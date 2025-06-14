from flask import Blueprint, request, jsonify, Response
from app.models.goal import Goal
from ..db import db
from app.models.task import Task

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    goal.tasks = [] 
    for task_id in task_ids:
        task = db.session.get(Task, task_id)
        if task:
            goal.tasks.append(task)

    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": task_ids
    }), 200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return jsonify(goal_dict), 200

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
    goals = db.session.scalars(db.select(Goal)).all()
    return jsonify([goal.to_dict() for goal in goals])

# GET one goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    return jsonify({"goal": goal.to_dict()})

# UPDATE a goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = db.session.get(Goal, goal_id)
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
    goal = db.session.get(Goal, goal_id)
    if not goal:
        return jsonify({"message": f"No goal with ID {goal_id} found"}), 404

    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

