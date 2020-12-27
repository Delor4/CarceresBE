from flask_restful import Resource

from db import session
from models.car import Car
from models.client import Client
from models.place import Place
from models.user import User
from models.zone import Zone

users = [
    {
        "name": "stroz",
        "user_type": 2,
        # pass: 's'
        "password_hash": "$6$rounds=656000$whFc0DVCMM6peC4x$bvgxj5eShNGWkI2e8E.hTXe2TOfiSBCgaIWfJCrEOD17uI7XPzkiqcvf.BX2"
        "/yhWfEwCHRlTzT3gITShKwA8a/",
    },
    {
        "name": "klient",
        "user_type": 3,
        # pass: 'k'
        "password_hash": "$6$rounds=656000$36qujjj0IHhRm3s3$rP.NkdJslEaSDDZ0zrNyOQDnLpjZ.VK04YSQ7G7o1iuiIk2EQRvRWU"
        "/dfCY0Nd.bX4z5iuv8yiMCT1YkOW7UD0",
    },
]

clients = [
    {"name": "Jan", "surname": "Kowalski", "user_id": 3},
    {"name": "Antoni", "surname": "Nowak", "user_id": 1},
]

cars = [
    {"plate": "POL 0001", "client_id": 1},
    {"plate": "POL 0002", "client_id": 1},
    {"plate": "POL 0003", "client_id": 2},
]


def get_zone1():
    return {
        "name": "Strefa 1",
        "bkg_file": "mapa_parkingu_zone1.png",
        "places": [
            [10, 18, "Górne"],
            [14, 15, "Górne"],
            [18, 11, "Górne"],
            [22, 8, "Górne"],
            [26, 4, "Górne"],
            [2, 39, "Lewe"],
            [3, 44, "Lewe"],
            [4, 50, "Lewe"],
            [25, 34],
            [29, 33],
            [34, 32],
            [39, 31],
            [44, 30],
            [47, 5],
            [51, 10],
            [55, 14],
            [59, 18],
            [63, 22],
            [67, 26],
            [71, 30],
            [75, 35],
            [79, 39],
            [83, 43],
            [87, 47],
            [92, 52],
            [56, 47],
            [51, 48],
            [46, 49],
            [42, 50],
            [37, 51],
            [33, 52],
            [28, 54],
            [23, 55],
            [18, 56],
            [11, 69],
            [15, 68],
            [20, 67],
            [24, 66],
            [29, 65],
            [34, 64],
            [38, 63],
            [43, 62],
            [47, 61],
            [52, 60],
            [56, 59],
            [61, 58],
            [65, 57],
            [67, 78, "Dolne"],
            [62, 79, "Dolne"],
            [58, 80, "Dolne"],
            [54, 81, "Dolne"],
            [49, 82, "Dolne"],
            [44, 83, "Dolne"],
            [40, 84, "Dolne"],
            [35, 85, "Dolne"],
            [31, 86, "Dolne"],
            [26, 87, "Dolne"],
            [21, 88, "Dolne"],
        ],
    }


def get_zone2():
    return {
        "name": "Strefa 2",
        "bkg_file": "mapa_parkingu_zone2.png",
        "places": [
            [41, 11],
            [44, 15],
            [47, 19],
            [50, 23],
            [52, 27],
            [55, 31],
            [58, 35],
            [60, 39],
            [63, 43],
            [66, 47],
            [68, 51],
            [71, 55],
            [74, 59],
            [77, 63],
            [80, 67],
            [32, 16],
            [35, 20],
            [38, 24],
            [41, 28],
            [43, 32],
            [46, 36],
            [49, 40],
            [51, 44],
            [54, 48],
            [57, 52],
            [59, 56],
            [62, 60],
            [65, 64],
            [68, 69],
            [71, 73],
            [22, 40],
            [24, 44],
            [27, 48],
            [30, 52],
            [33, 56],
            [35, 60],
            [38, 64],
            [41, 68],
            [43, 72],
            [47, 76],
            [50, 80],
            [13, 46],
            [15, 50],
            [18, 54],
            [21, 58],
            [23, 62],
            [26, 66],
            [29, 70],
            [32, 74],
            [35, 78],
            [38, 82],
            [41, 86],
        ],
    }


class SeedResource(Resource):
    """
    Resources for 'seed' (/api/seed) endpoint.
    """

    def get(self):
        """
        Seed the database.
        """
        self.seed_zones()
        self.seed_users()
        self.seed_clients()
        self.seed_cars()

        session.commit()
        return {"message": "Database seeded."}, 200

    def seed_users(self):
        for u in users:
            user = User(
                name=u["name"],
                user_type=u["user_type"],
                password_hash=u["password_hash"],
            )
            session.add(user)

    def seed_zones(self):
        self._seed_zone(get_zone1())
        self._seed_zone(get_zone2())

    def _seed_zone(self, zone_data):
        zone = Zone(name=zone_data["name"], bkg_file=zone_data["bkg_file"])
        session.add(zone)

        for index, pos in enumerate(zone_data["places"]):
            place = Place(
                nr=index + 1,
                zone_id=zone.id,
                name=pos[2] if len(pos) > 2 else None,
                pos_x=pos[0],
                pos_y=pos[1],
            )
            zone.places.append(place)
            session.add(place)

    def seed_clients(self):
        for c in clients:
            client = Client(
                address=c.get("address", None),
                city=c.get("city", None),
                phone=c.get("phone", None),
                name=c["name"],
                surname=c["surname"],
                user_id=c["user_id"],
            )
            session.add(client)

    def seed_cars(self):
        for c in cars:
            car = Car(
                plate=c["plate"],
                client_id=c["client_id"],
            )
            session.add(car)
