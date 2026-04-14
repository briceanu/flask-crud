# main.py
from flask import Flask
from flask_migrate import Migrate
from .extensions import db
from .crud_routes import main_routes
from .db_connection import DB_URL
from flask_jwt_extended import JWTManager
from load_dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
# Initialize SQLAlchemy with Flask
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})
# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True)
