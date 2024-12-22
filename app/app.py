from flask import Flask

from ui.dash_view import create_dash_app
from ui.web import bp as web_bp


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.register_blueprint(web_bp)

    create_dash_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=9001)
