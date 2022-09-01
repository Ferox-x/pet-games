from os import environ


bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = 1000
workers = 1

env = {
    'DJANGO_SETTINGS_MODULE': 'app.settings'
}

reload = True
name = 'app'
