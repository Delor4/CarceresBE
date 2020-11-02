#!/usr/bin/env python
"""
Create new database tables for models
"""
from sqlalchemy.orm import sessionmaker

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

    # Make default user if needed
    session = sessionmaker(bind=engine)()
    if session.query(models.user.User).count() == 0:
        user = models.user.User(name='admin',
                           user_type=1,
                           # pass: 'carceres'
                           password_hash="$6$rounds=656000$qvRag7CybnVI6t78$CZMIiqioeKKrrHOHt9nfHyVnqs2JK69gYPbjFMHt"
                                         ".lGvGw8BKliAlJCzc0WR1aGLlNM9bclSz5klaaUAbPUZh1",
                           )
        session.add(user)
        session.commit()
