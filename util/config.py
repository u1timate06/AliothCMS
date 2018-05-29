#!/usr/bin/env python
# __Author__:cmustard

import re

# 日志记录路径
LOGFILE = "./test.log"

# 是否开启debug
Debug = False

# 数据库配置信息
DATABASE_USER = "admin"
DATABASE_PASSD = "password"
DATABASE = "cms"
DATABASE_PORT = 27017


PLUGIN_CLASSNAME_REGEX = r"class\s+(.*?)\(PluginBase\)"
CLASSNAMEREGX = re.compile(PLUGIN_CLASSNAME_REGEX)
