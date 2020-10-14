#!/usr/bin/env python

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from classes.config import flask_app
    import base

    DB_URI = flask_app.config['SQLALCHEMY_DATABASE_URI']

    import models.user
    import models.client
    import models.car
    import models.zone
    import models.place
    import models.subscription

    engine = create_engine(DB_URI)
    base.Base.metadata.create_all(engine, checkfirst=True)
