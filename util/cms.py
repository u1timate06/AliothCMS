#!/usr/bin/env python
# __Author__:cmustard

import importlib
import re
import os
import sys
from multiprocessing import Pool,Process
from fingerprint.jboss import JBoss

PLUGIN_CLASSNAME_REGEX = "class\s+(.*?)\(PluginBase\)"

# 获取插件
def get_plugin():
    plugin_path = r"../fingerprint/jboss.py"
    with open(plugin_path,"r") as f:
        content = f.read()
    class_name = re.findall(PLUGIN_CLASSNAME_REGEX,content)[0]
    print(class_name)
    filename = os.path.split(plugin_path)[1]
    filename = filename.split(".",-1)[0]
    importString = "fingerprint.{}".format(filename)
    ip_module = importlib.import_module('.', importString)
    ip_module_cls = getattr(ip_module, class_name)
    # 获取类
    j = ip_module_cls()
    url = "http://182.87.0.20:8081/portal/bsdt.seam"
    j.start(url)
    print(dir(ip_module_cls))
    pass


def _eval():
    pass

def main():
    get_plugin()

if __name__ == '__main__':
    main()





