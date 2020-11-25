from flask_restful import fields


class FieldsDate(fields.Raw):
    def __init__(self, dt_format='rfc822', **kwargs):
        super(FieldsDate, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        return value.strftime(self.dt_format)
