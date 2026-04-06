# main.py
from flask import Flask
from flask_migrate import Migrate
from .extensions import db
from .crud_routes import main_routes
from .db_connection import DB_URL

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with Flask
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True)
