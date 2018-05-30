#!/usr/bin/env python
# __Author__:cmustard

import importlib.util
import re
import os
import sys

from multiprocessing import Pool
from util.comm import getLogger, printInfo
from util.config import CLASSNAMEREGX, PLUGIN_CLASSNAME_REGEX

LOGGER = getLogger()
PLUGIN_ROOT = "../fingerprint/"


class CmsDector():
    def __init__(self):
        self.url = None
        self.pluginClass = None
        # self.cmsRes = queues.Queue(1000)
        self.cmsRes = None

    # 获取插件

    def _getCmsRes(self, path):
        """

        :param path:
        :return:
        """
        try:
            class_name = self.getClassName(CLASSNAMEREGX, self.getClassString(path))
            # 判断
            spec = importlib.util.spec_from_file_location(class_name, path)
            if spec is None:
                raise Exception("import module error!!!")
            moudle = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(moudle)
            sys.modules[class_name] = moudle
            obj = eval("moudle.{}".format(class_name))()

            self.cmsRes = obj.start(self.url)
            cms_name = obj.cms_name
            manData = self.caclProbaliy(cms_name)
            if manData is None:
                return
            print(manData)
        except Exception as e:
            LOGGER.error(printInfo(__file__, "function _getCmsRes error is {}".format(str(e))))

    def caclProbaliy(self,cms_name):
        if self.cmsRes is None:
            return
        cmsRes = self.cmsRes
        header = cmsRes['header']
        commom = cmsRes[cms_name]
        length = len(commom)
        flag = 0
        caclRes = None
        if length>0:
            for value in commom:
                if value:
                    flag +=1
            caclRes = "{}%".format(float(flag) / length * 100)
            if flag == 0:
                caclRes = None

        if len(header)>0:
            caclRes = "{}%".format(100)

        cmsRes[cms_name] = caclRes
        return cmsRes

    def getClassString(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
        else:
            return ""
        return content

    def getClassName(self, pattern, content):
        result = re.findall(CLASSNAMEREGX, content)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def run(self, url, thread=10, cmd=False):
        """
        api调用
        :param url:
        :param thread:
        :return:
        """
        if cmd:
            global PLUGIN_ROOT
            PLUGIN_ROOT = "fingerprint/"

        pools = Pool(processes=thread)
        # 获取所有的插件名称
        self.url = url
        plugins_list = []
        plugins_list_temp = os.listdir(PLUGIN_ROOT)
        for name in plugins_list_temp:
            if "__init__" in name:
                continue
            if name.endswith("py"):
                plugins_list.append(PLUGIN_ROOT + name)

        # print(plugins_list)

        for plugin_path in plugins_list:
            # self.get_cmsRes(plugin_path)
            pools.apply_async(func=self._getCmsRes, args=(plugin_path,))

        pools.close()
        pools.join()
        print("+---------scanner end---------+")


if __name__ == '__main__':
    c = CmsDector()
    path = r"C:\Users\glamor\Desktop\red-club\玉衡CMS指纹识别\AliothCMS\fingerprint\jboss.py"
    url = "http://182.87.0.20:8081/portal/bsdt.seam"
    c.run(url="http://182.87.0.20:8081/portal/bsdt.seam")
# c._getCmsRes(path)

# get_plugin("123")
