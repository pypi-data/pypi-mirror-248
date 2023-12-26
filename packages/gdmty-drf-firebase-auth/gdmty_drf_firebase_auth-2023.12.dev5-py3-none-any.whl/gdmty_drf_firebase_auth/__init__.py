""" Custom Django Rest Framework authentication backend for parsing Firebase uid tokens or email/password, and storing as local users.'

This package is a fork of django-firebase-auth
with some fixes and improvements.
This package also adds support for login
with email and password, and also adds support for
custom user models. And is fully integrated with gdmty-id.


"""
__title__ = 'gdmty_drf_firebase_auth'
__version__ = '2023.12-dev5'
__description__ = (
    'Custom Django Rest Framework authentication backend for '
    'parsing Firebase uid tokens and storing as local users.'
    'This package is a fork of django-firebase-auth '
    'with some fixes and improvements. '
    'This package also adds support for login '
    'with email and password, and also adds support for '
    'custom user models. And is fully integrated with idmty.'
)
__url__ = 'https://github.com/SIGAMty/gdmty-drf-firebase-auth'
__author__ = 'César Benjamín'
__author_email__ = 'mathereall@gmail.com'
__license__ = 'Apache 2.0'
VERSION = __version__
