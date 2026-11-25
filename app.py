
from flask import Flask
from database import init_db

# Import the feature Blueprints
from dashboard import dashboard_bp
from courses import courses_bp
from notes import notes_bp
from tasks import tasks_bp

# Create Flask application
app = Flask(__name__)

# Initialize database
with app.app_context():
    init_db()

# Connect all features to the main application
app.register_blueprint(dashboard_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
