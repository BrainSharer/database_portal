### Install instructions for django-plotly-dash
#### Libraries
1. pip install django_plotly_dash channels daphne redis django-redis channels-redis dpd-static-support
1. install redis on server
1. Modify settings.py
    1. add 'django_plotly_dash.apps.DjangoPlotlyDashConfig', to installed_apps
    1. add X_FRAME_OPTIONS = 'SAMEORIGIN'
    1. add CHANNEL_LAYERS
1. add path('django_plotly_dash/', include('django_plotly_dash.urls')), to urls.py
1. do manage.py migrate django_plotly_dash
1. install bootstrap
    1. pip install django-bootstrap4
    1. pip install dash_bootstrap_components
    1. add boostrap4 to installed apps in settings.py
    1. setup an alias to static in apache 
