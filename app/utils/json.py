from datetime import date, datetime, time


def json_serial_date(obj):
    if obj is None:
        return None
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError("Type %s not of type date" % type(obj))
