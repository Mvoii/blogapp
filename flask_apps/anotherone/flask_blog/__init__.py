from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_blog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # from flask_blog import routes
    from flask_blog.user.routes import users
    from flask_blog.main.routes import main
    from flask_blog.posts.routes import posts
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    with app.app_context():
        db.create_all()
        
    return app
