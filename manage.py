from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from classes.config import config

import models.user
import models.client
import models.car
import models.zone
import models.place
import models.subscription

app = Flask(__name__)
app.config.from_mapping(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
