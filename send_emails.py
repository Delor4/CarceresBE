#!/usr/bin/env python
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message

from db import session
from models.car import Car
from models.client import Client
from models.subscription import Subscription
from models.user import User
from models.place import Place
from models.zone import Zone
from models.payment import Payment

app = None


def send_email_notifications():
    global app
    with app.app_context():
        if not app.config["EMAILS_ENABLED"]:
            return
        mail = Mail(app)
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        reminder_period = now + timedelta(days=1)
        subscribers_to_notify = (
            session.query(Subscription)
            .filter(Subscription.notification_sended == False)
            .filter(Subscription.end > now)
            .filter(Subscription.end < reminder_period)
            .join(Car, Car.id == Subscription.car_id)
            .join(Client, Client.id == Car.client_id)
            .join(User, User.id == Client.user_id)
            .filter(User.email.isnot(None))
            .all()
        )
        if len(subscribers_to_notify) == 0:
            return
        with mail.connect() as conn:
            for note in subscribers_to_notify:
                user = (
                    session.query(User)
                    .join(Client, User.id == Client.user_id)
                    .join(Car, Client.id == Car.client_id)
                    .filter(Car.id == note.car_id)
                    .first()
                )
                print(
                    "Sending notification to `%s` (less than day to end of subscription %s)."
                    % (user.name, note.id)
                )
                message = (
                    "Witaj, %s.\n"
                    "Do końca opłaconego abonamentu parkingowego pozostało mniej niż 24 godziny.\n"
                    "Prosimy o przedłużenie rezerwacji lub zabranie pojazdu z parkingu.\n"
                    "\n\nWiadomość wysłana automatycznie. Prosimy nie odpowiadać na ten email."
                    % user.client.name
                )
                subject = "Przypomnienie o końcu abonamentu parkingowego"
                msg = Message(recipients=[user.email], body=message, subject=subject)

                conn.send(msg)
                note.notification_sended = True
                session.add(note)
                session.flush()
        session.commit()


def setup_scheduler(_app):
    global app
    app = _app
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email_notifications, trigger="interval", seconds=60)
    scheduler.start()


if __name__ == "__main__":
    send_email_notifications()
