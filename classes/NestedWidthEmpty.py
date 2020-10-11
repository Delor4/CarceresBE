from flask_restful import marshal
from flask_restful.fields import Nested, get_value


class NestedWithEmpty(Nested):
    """
    Allows returning an empty dictionary if marshaled value is None
    """

    def __init__(self, nested, allow_empty=False, **kwargs):
        self.allow_empty = allow_empty
        super(NestedWithEmpty, self).__init__(nested, **kwargs)

    def output(self, key, obj):
        value = get_value(key if self.attribute is None else self.attribute, obj)
        if value is None:
            if self.allow_null:
                return None
            elif self.allow_empty:
                return {}
        return marshal(value, self.nested)
