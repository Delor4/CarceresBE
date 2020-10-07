from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import DB_URI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

import models.user

if __name__ == '__main__':
    manager.run()