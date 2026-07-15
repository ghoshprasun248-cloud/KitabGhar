import os
from datetime import timedelta


class Config:
    # Application Secret Key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "kitabghar-secret-key-change-this-in-production"
    )


    # Flask Upload Configuration

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    BOOK_UPLOAD_FOLDER = os.path.join(
        UPLOAD_FOLDER,
        "books"
    )

    COVER_UPLOAD_FOLDER = os.path.join(
        UPLOAD_FOLDER,
        "covers"
    )


    # Allowed File Extensions

    ALLOWED_BOOK_EXTENSIONS = {
        "pdf",
        "epub",
        "mobi"
    }

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }


    # Maximum Upload Size
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024   # 100 MB


    # Session Configuration

    SESSION_COOKIE_NAME = "kitabghar_session"

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_SAMESITE = "Lax"

    PERMANENT_SESSION_LIFETIME = timedelta(
        days=7
    )


    # Pagination

    BOOKS_PER_PAGE = 12

    USERS_PER_PAGE = 20


    # Application Settings

    APP_NAME = "KitabGhar"

    VERSION = "1.0.0"

    DESCRIPTION = (
        "Online E-Book Management and Digital Reading Platform"
    )


    # Email Configuration

    MAIL_SERVER = os.environ.get(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME",
        ""
    )

    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD",
        ""
    )


    # Security Settings

    PASSWORD_MIN_LENGTH = 8

    MAX_LOGIN_ATTEMPTS = 5

    ACCOUNT_LOCK_TIME = 15   # minutes


    # CDN Configuration

    CDN_ENABLED = False

    CDN_URL = os.environ.get(
        "CDN_URL",
        ""
    )


    # Payment Gateway Configuration

    PAYMENT_ENABLED = False

    PAYMENT_PROVIDER = "demo"

    PAYMENT_SECRET_KEY = os.environ.get(
        "PAYMENT_SECRET_KEY",
        ""
    )


    # Logging

    LOG_FOLDER = os.path.join(
        BASE_DIR,
        "logs"
    )

    LOG_FILE = os.path.join(
        LOG_FOLDER,
        "kitabghar.log"
    )
    # Database Configuration

    MYSQL_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"

    MYSQL_USER = "p9PcJUvGS7rpgXv.root"

    MYSQL_PASSWORD = "PqW0u3a7ueGd7clw"

    MYSQL_DB = "kitabghar"

    MYSQL_PORT = 4000

class DevelopmentConfig(Config):

    DEBUG = True

    TESTING = False



class ProductionConfig(Config):

    DEBUG = False

    TESTING = False

    SESSION_COOKIE_SECURE = True



class TestingConfig(Config):

    DEBUG = True

    TESTING = True

    MYSQL_DATABASE = "kitabghar_test_db"



# Select Configuration

config = {

    "development": DevelopmentConfig,

    "production": ProductionConfig,

    "testing": TestingConfig,

    "default": DevelopmentConfig

}
MYSQL_SSL_MODE = "VERIFY_IDENTITY"
MYSQL_SSL_CA = "isrgrootx1.pem"