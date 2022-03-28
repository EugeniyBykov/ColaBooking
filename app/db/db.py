from flask_sqlalchemy import SQLAlchemy

def init_db(app) :
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/cola.db'
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return SQLAlchemy(app)