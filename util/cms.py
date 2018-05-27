#!/usr/bin/env python
# __Author__:cmustard

import importlib.abc
import re
import os
import sys
from multiprocessing import Pool,Process,queues
from util.comm import getLogger


PLUGIN_CLASSNAME_REGEX = "class\s+(.*?)\(PluginBase\)"
LOGGER = getLogger()

class CmsDector():
    def __init__(self):
        self.url = None
        self.pluginClass = None
        # self.cmsRes = queues.Queue(1000)
        self.cmsRes= None


    # 获取插件
    def get_cmsRes(self,plugin_path):
        with open(plugin_path,"r") as f:
            content = f.read()
        # 获取文件中的类名
        class_name = re.findall(PLUGIN_CLASSNAME_REGEX,content)[0]
        # 获取插件名称
        filename_ex = os.path.split(plugin_path)[1]
        # 去掉文件后缀名
        filename = filename_ex.split(".",-1)[0]
        # 格式化导入语句
        importString = "fingerprint.{}".format(filename)
        # 相对导入
        ip_module = importlib.import_module(importString)
        ip_module_cls = getattr(ip_module, class_name)
        # 获取类
        plugin_class = ip_module_cls()
        self.cmsRes = plugin_class.start(self.url)
        # self.cmsRes.put(self.cmsVul)
        print(self.cmsRes)




    def run(self,url,thread=10):
        pools = Pool(processes=thread)
        # 获取所有的插件名称
        self.url = url
        plugins_list = []
        plugins_list_temp = os.listdir("../fingerprint")
        for name in plugins_list_temp:
            if "__init__" in name:
                continue
            if name.endswith("py"):
                plugins_list.append("../fingerprint/"+name)
        # print(plugins_list)
        for plugin_path in plugins_list:
            # self.get_cmsRes(plugin_path)
            pools.apply_async(func=self.get_cmsRes,args=(plugin_path,))
        pools.close()
        pools.join()
        print("+---------scanner end---------+")


if __name__ == '__main__':
    c = CmsDector()
    c.run(url= "http://182.87.0.20:8081/portal/bsdt.seam")
    # get_plugin("123")




