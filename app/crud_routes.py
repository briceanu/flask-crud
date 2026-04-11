# routes.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    jwt_required,
)

from .schemas import (
    TodoSchemaIn,
    TodoSchemaOut,
    TodoUpdateSchemaIn,
    TodoUpdateTitleSchemaIn,
    UserSignupSchemaIn,
    UserSchemaOut,
)
from .models import Todo, User
from sqlalchemy import delete, insert, select, update
from .logger import logger
from .extensions import db
from .authentication import black_list_token, is_token_blacklisted

# Create a blueprint
main_routes = Blueprint("main_routes", __name__)


@main_routes.get("/gigi")
def get_gigi():
    return "this is gigi"


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


# create a user account
@main_routes.route("/signup", methods=["POST"])
def signup_user():
    user_schema = UserSignupSchemaIn()
    try:
        user_data = user_schema.load(request.get_json())
        hashed_password = generate_password_hash(user_data["password"])
        user_data["password"] = hashed_password
        del user_data["confirm_password"]
        stmt = insert(User).values(**user_data)
        db.session.execute(stmt)
        db.session.commit()
        logger.info(f"User created with name {user_data['name']}")
        return jsonify(f"Account successfully created {user_data['name']}"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


# get all users ONLY FOR ADMIN
@main_routes.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    try:
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        decoded_token = decode_token(auth_header.split()[1])
        if decoded_token["scope"] != "admin":
            logger.warning(
                "Unauthorized access attempt by user with scope: "
                + decoded_token["scope"]
            )
            return jsonify({"error": "Unauthorized access"}), 403
        users = db.session.execute(select(User)).scalars().all()
        schema = UserSchemaOut(many=True)
        return jsonify(schema.dump(users)), 200

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


# sigin in user
@main_routes.route("/login", methods=["POST"])
def login():
    username = request.form.get("name", None)
    password = request.form.get("password", None)
    stmt = select(User).where(User.name == username)
    user_from_db = db.session.execute(stmt).scalar_one_or_none()
    if not user_from_db:
        return jsonify({"error": "Invalid username or password"}), 401
    if not check_password_hash(user_from_db.password, password):
        return jsonify({"error": "Invalid username or password"}), 401
    # You can use the additional_claims argument to either add
    # custom claims or override default claims in the JWT.
    additional_claims = {"scope": user_from_db.scope}
    access_token = create_access_token(
        identity=username,
        additional_claims=additional_claims,
        expires_delta=timedelta(minutes=1),
    )
    refresh_token = create_refresh_token(
        identity=username,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=8),
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@main_routes.route("/logout", methods=["POST"])
def logout_user():
    try:
        token = request.headers.get("Authorization")
        decoded_token = decode_token(token.split()[1])
        token_jti = decoded_token["jti"]
        token_exp = decoded_token["exp"]
        if decoded_token["type"] != "refresh":
            return jsonify({"error": "Only refresh tokens can be blacklisted"}), 400
        if not token_jti or not token_exp:
            return jsonify({"error": "Invalid token"}), 400

        if is_token_blacklisted(jti=token_jti) == 1:
            return jsonify(detail="Token already black listed."), 400

        ttl = int(token_exp) - int(datetime.now(timezone.utc).timestamp())
        black_list_token(token_jti, ttl)
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        return jsonify({"error": "Bad Request", "details": str(e)}), 400


@main_routes.route("/new-access-token", methods=["POST"])
def get_new_access_token():
    try:
        token = request.headers.get("Authorization")
        decoded_token = decode_token(token.split()[1])
        if decoded_token["type"] != "refresh":
            return jsonify({"error": "Refresh token required"}), 400
        if is_token_blacklisted(jti=decoded_token["jti"]) == 1:
            return jsonify({"error": "Token is blacklisted"}), 400
        stmt = select(User).where(User.name == decoded_token["sub"])
        user_from_db = db.session.execute(stmt).scalar_one_or_none()
        if not user_from_db:
            return jsonify({"error": "Invalid token"}), 400
        if user_from_db.scope != decoded_token["scope"]:
            logger.warning(
                f"Unauthorized access attempt by user with scope {user_from_db.scope}"
            )
            return jsonify({"error": "Invalid token"}), 400

        return create_access_token(
            identity=user_from_db.name, additional_claims={"scope": user_from_db.scope}
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        db.session.close()


@main_routes.post("/upload-image")
def upload_user_image():
    return "image uploadd"
