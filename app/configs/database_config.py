"""database configuration"""

import os

# determine whether show log or not
BOOL_ECHO = False

# 数据库相关的配置信息,增加系统环境变量配置

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
