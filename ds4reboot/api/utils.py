import traceback

from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response

from ds4reboot.secret_settings import DEBUG


# Map dict to dereferencable object
class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


def is_integer(decimal):
    return decimal % 1 == 0


def log_exception(e, tb=None):
    # TODO log
    if DEBUG:
        print(e)
    if tb:
        return Response({'exception': str(e), 'traceback': tb}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'exception': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def log_validation_errors(errors):
    if DEBUG:
        print(errors)
    return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
