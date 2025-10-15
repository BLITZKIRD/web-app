from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    # Basic config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Initialize database
    from .auth.models import init_db
    init_db()

    # Register blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.route('/')
    def home():
        return 'Home page. Go to /register or /login'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
