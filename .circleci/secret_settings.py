DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'circleci',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
SECRET_APPS = []
SECRET_KEY = "ao#f$k))2#crl(qsfm796u!0mlicbrjh!$ucv9b8t6!sf&&a=l"
DEBUG = True

EMAIL_USE_SSL = True
EMAIL_HOST = "fake.fake.fake"
EMAIL_PORT = 465
EMAIL_HOST_USER = "fake@fake.fake"
EMAIL_HOST_PASSWORD = "fake.fake.fake"
DEFAULT_FROM_EMAIL = 'fake.fake.fake'

# Forward is a special API connection
EMAIL_FORWARD_HOST_USER = "fake@fake.fake"
EMAIL_FORWARD_HOST_PASSWORD = "fake.fake.fake"