from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app, db_uri):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def create_all():
    """Create all db tables"""

    from rdb.models.user import User
    from rdb.models.environment import Environment
    from rdb.models.userEnvironmentAccess import UserEnvironmentAccess
    from rdb.models.image import Image
    from rdb.models.mlModel import MLModel

    db.create_all()
    db.session.commit()
