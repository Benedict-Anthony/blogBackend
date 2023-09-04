from datetime import timedelta


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    "DEFAULT_SCHEMA_CLASS": 'drf_spectacular.openapi.AutoSchema',

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=100),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=101),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False
}
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3000",
    "http://localhost",
]


SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'Blog API Docs',
    'VERSION': '1.0.0',

}
