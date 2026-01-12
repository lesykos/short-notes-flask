import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "sdfsf3435lkjh34j5h3iu4sdf2")
    ADMIN_NAME = os.environ.get("ADMIN_NAME")
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
