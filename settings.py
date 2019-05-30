import os


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(12)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    #sqlalcehmy 配置
    SQLALCHEMY_COMMIT_ON_TEARDOW = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:asd123@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #post per_page
    POSTS_PER_PAGE = 10

    #管理员邮件
    BLUELOG_ADMIN = '1075573584@qq.com'

    #头像保存路劲
    AVATARS_SAVE_PATH = os.path.join(basedir,r'bluelog\uploads\avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "1075573584"
    MAIL_PASSWORD = "tshhozuxjalnbaeh"
    MAIL_DEFAULT_SENDER = 'Bluelog <1075573584@qq.com>'


    #tshhozuxjalnbaeh
    #zlqiryrknmyafjdf
class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


# 生成环境配置映射  十分巧妙
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig
}

if __name__ == '__main__':
    c = Config()
    print(c.basedir)
    print(c.AVATARS_SAVE_PATH)