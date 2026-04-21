from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(
            {
                "error": "Bad Request",
                "fields": e.description
                if isinstance(e.description, dict)
                else str(e.description),
            }
        ), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(
            {
                "error": "Unauthorized",
                "message": str(e.description)
                if e.description
                else "Authentication required",
            }
        ), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify(
            {
                "error": "Forbidden",
                "message": str(e.description)
                if e.description
                else "You do not have permission to access this resource",
            }
        ), 403

    @app.errorhandler(409)
    def conflict_error(e):
        return jsonify({"error": "Conflict", "message": e.description}), 409

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": str(e.description)}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal server error"}), 500
