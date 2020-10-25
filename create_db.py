#!/usr/bin/env python
"""
Create new database tables for models
"""
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from classes.config import config
    import base

    import models.user
    import models.client
    import models.car
    import models.zone
    import models.place
    import models.subscription

    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    base.Base.metadata.create_all(engine, checkfirst=True)
