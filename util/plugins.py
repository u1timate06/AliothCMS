#!/usr/bin/env python
# __Author__:cmustard



class PluginBase:
    def __init__(self):
        self.cms_name = None  # cms对应名称
        self.version = None   # cms版本结果
        self.body = None  # 返回的body
        self.uri = None  # 需要验证的uri
        self.uri_md5 = None  # 对应uri的md5值
        self.regx = None   # 正则匹配
        self.header = None  # 头部匹配
        self.title = None   # title匹配
        pass

    def verify(self):
        pass

    def output(self):
        pass

    def _html(self):
        pass

    def _headers(self):
        pass

