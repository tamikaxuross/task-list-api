from flask import Blueprint, request, jsonify, Response
from app.models.task import Task
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# Helper: safely get a task by ID or return a 404 JSON response
def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"message": "Invalid ID"}), 400

    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"message": f"No task with ID {task_id} found"}), 404

    return task

# CREATE: POST /tasks
@bp.post("")
def create_task():
    data = request.get_json()

    if "title" not in data or "description" not in data:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(data)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# READ ALL: GET /tasks
@bp.get("")
def get_all_tasks():
    sort_order = request.args.get("sort")
    title_filter = request.args.get("title")

    query = db.session.query(Task)

    if title_filter:
        query = query.filter(Task.title.ilike(f"%{title_filter}%"))

    if sort_order == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())

    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])


# READ ONE: GET /tasks/<task_id>
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = get_task_or_abort(task_id)
    if not isinstance(task, Task):
        return task  # return 404 or 400 response
    return jsonify({"task": task.to_dict()})

# UPDATE: PUT /tasks/<task_id>
@bp.put("/<task_id>")
def update_task(task_id):
    task = get_task_or_abort(task_id)
    if not isinstance(task, Task):
        return task

    data = request.get_json()
    if "title" not in data or "description" not in data:
        return jsonify({"details": "Invalid data"}), 400

    task.title = data["title"]
    task.description = data["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# DELETE: DELETE /tasks/<task_id>
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = get_task_or_abort(task_id)
    if not isinstance(task, Task):
        return task

    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
