# routes.py
from flask import Blueprint, request, jsonify
from .schemas import (
    TodoSchemaIn,
    TodoSchemaOut,
    TodoUpdateSchemaIn,
    TodoUpdateTitleSchemaIn,
)
from .models import Todo
from sqlalchemy import delete, insert, select, update
from .logger import logger
from .extensions import db

# Create a blueprint
main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/create", methods=["POST"])
def create_todo():
    try:
        todo_schema = TodoSchemaIn()
        todo_data = todo_schema.load(request.get_json())
        stmt = insert(Todo).values(**todo_data)
        db.session.execute(stmt)
        db.session.commit()
        logger.info(f"Todo created with id {todo_data['id']}")
        return jsonify(f"your task has been created. Task id {todo_data['id']}"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    finally:
        db.session.close()


@main_routes.route("/todos", methods=["GET"])
def get_todos():
    try:
        todos = db.session.execute(select(Todo)).scalars().all()
        schema = TodoSchemaOut(many=True)
        return jsonify(schema.dump(todos)), 200

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


@main_routes.route("/todo/<uuid:id>", methods=["GET"])
def get_todo(id):
    try:
        stmt = select(Todo).where(Todo.id == id)
        todo = db.session.execute(stmt).scalar_one_or_none()
        if not todo:
            logger.error(f"Todo with id {id} not found")
            return jsonify({"error": f"Todo with id {id} not found"}), 404
        schema = TodoSchemaOut(exclude=["email", "age"])
        logger.info(todo)
        return jsonify(schema.dump(todo)), 200
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


@main_routes.route("/todo/<uuid:id>", methods=["DELETE"])
def remove_one_todo(id):
    try:
        stmt = delete(Todo).where(Todo.id == id).returning(Todo.id)
        todo = db.session.execute(stmt).scalar_one_or_none()
        if not todo:
            logger.error(f"Todo with id {id} not found")
            return jsonify({"error": f"Todo with id {id} not found"}), 404
        db.session.commit()
        return jsonify({"Success": f"Todo with id {id} removed"}), 200
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


@main_routes.route("/todo/update/<uuid:id>", methods=["PUT"])
def update_todo(id):
    try:
        todo_schema = TodoUpdateSchemaIn()
        todo_data = todo_schema.load(request.get_json())
        stmt = update(Todo).where(Todo.id == id).values(**todo_data).returning(Todo.id)
        todo = db.session.execute(stmt).scalar_one_or_none()
        if not todo:
            logger.error(f"Todo with id {id} not found")
            return jsonify({"error": f"Todo with id {id} not found"}), 404
        db.session.commit()
        logger.info(f"Todo with id {id} updated")
        return jsonify(f"Todo with id {id} updated"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


@main_routes.route("/todo/update/<uuid:id>", methods=["PATCH"])
def update_todo_title(id):
    try:
        todo_schema = TodoUpdateTitleSchemaIn()
        todo_data = todo_schema.load(request.get_json())
        stmt = update(Todo).where(Todo.id == id).values(**todo_data).returning(Todo.id)
        todo = db.session.execute(stmt).scalar_one_or_none()
        if not todo:
            logger.error(f"Todo with id {id} not found")
            return jsonify({"error": f"Todo with id {id} not found"}), 404
        db.session.commit()
        logger.info(f"Todo with id {id} updated")
        return jsonify(f"Todo with id {id} updated"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()
