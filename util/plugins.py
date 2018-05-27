#!/usr/bin/env python
# __Author__:cmustard

import hashlib
import bs4
import urllib.request
import urllib.parse
import urllib.error
import gzip
import re
from random import choice


from util.userAgent import pcUserAgent
from util.comm import getLogger, printInfo, convertDict


class PluginBase:
    def __init__(self):
        self.code = 200
        self.url = None  # 目标URL
        self.cms_name = None  # cms规则名称
        self.author = None  # 插件作者
        self.description = None  # 插件描述
        self.website = None  # 插件参考网站

        # 规则部分
        self.version = None  # cms版本结果
        self.body = None  # 规则 body部分
        self.static_uri = None  # 需要验证的uri
        self.uri_md5 = None  # 对应uri的md5值
        self.headers = None  # 头部匹配
        self.title = None  # title匹配

        # sysytem
        self.encodeList = ("utf-8", "gb2312", "gbk", "big5")
        self.logger = getLogger()

    def start(self, url):
        self.url = url
        self._verify()
        # self.output()
        return self.matches_result

    def output(self):
        """
        该函数需要自己实现,返回一个output字典
        :return:
        """
        raise NotImplementedError

    def plugin(self):
        """
        该函数需要自己实现
        :return:
        """
        """
        title,body,version,header,static,head,text
        """
        # self.cms_name = "hexo"
        # self.author = "Your preferred name <email@address>"
        # self.description = "Generic CMS is an open-source Content Management System developed in PHP."
        # self.website = "http://example.com/"
        #
        # matches = [
        # 	# {"title": 'glamor","body":"<name>'},
        # 	# {"version": '&copy; 2018 glamor'},
        # 	# {"body": '<a href="http://hexo.io/" target="_blank">Hexo</a>'},
        # 	# {"header": "Server:nginx/1.12.1"},
        # 	# {"static": "/uri", "md5": "12313123123"},
        # 	# {"static": '/ura', "content": "<name>123"},
        # 	{"static": "/usi", "version": '&copy; (2017|2018|2000) glamor'},
        # 	{"head": "asdasd"},
        # 	{"text": "123"},  # body and head
        # ]
        # return matches

        raise NotImplementedError

    def _verify(self):
        self.matches_result = dict()
        self.matches_result["header"] = []
        self.matches = self.plugin()

        self.matches_result[self.cms_name] = []
        self._access()

        for cms_rule in self.matches:
            # 一条且的规则
            cms_rule_list = list(cms_rule.keys())
            for sign in cms_rule_list:
                if sign.strip() == "static":
                    self.static_uri = cms_rule[sign]
                    self._access()
                    if "md5" in cms_rule_list:
                        _md5 = self.md5(self.contents)
                        if _md5 == cms_rule["md5"]:
                            self.matches_result[self.cms_name].extend([self.static_uri, self.code])
                    if "version" in cms_rule_list:
                        result = self._find(cms_rule["version"], self.contents)
                        if len(result) > 0:
                            result.extend(("version", self.code))
                            self.matches_result[self.cms_name].append(tuple(result))
                    else:
                        self._comm(sign, cms_rule[sign])
                    break
                elif sign.strip() == "version":
                    result = self._find(cms_rule[sign], self.contents)
                    if len(result) > 0:
                        result.append(("version", self.code))
                        self.matches_result[self.cms_name].append(tuple(type(result)))
                elif sign.strip() == "header":
                    self._header(sign, cms_rule[sign])
                elif sign.strip() == "md5":
                    continue
                else:
                    self._comm(sign, cms_rule[sign])
        # add description
        self.matches_result["description"] = self.description
        # print(self.matches_result)

    def _comm(self, sign, rule):
        result = self._find(rule, self.raw_body)
        if result:
            self.matches_result[self.cms_name].append(True)
        else:
            self.matches_result[self.cms_name].append(False)

    def _header(self, sign, rule):
        """

        :param sign:
        :param rule:
        :return:
        """
        header_raw_dict = convertDict(str(self.raw_headers))
        header_dict = dict()
        # format
        for key in header_raw_dict.keys():
            header_dict[key.lower()] = header_raw_dict[key]

        if ":" in rule:
            header_name, header_info = rule.split(":")
            # print(header_name)
            header_lower_name = header_name.lower()
            if not header_lower_name in list(header_dict.keys()):
                return
            result = self._find(header_info, header_dict[header_name])
            if len(result) > 0:
                self.matches_result["header"].append("{}:{}".format(header_name,result))
        else:
            result = self._find(rule, self.raw_headers)
            if len(result) > 0:
                self.matches_result["header"].append(result)
            else:
                self.matches_result["header"].append(result)

    def _find(self, pattern, rawData):
        """

        :param pattern:
        :param rawData:
        :return:
        """
        pattern = re.compile(pattern)
        result = re.findall(pattern, rawData)
        return result

    def _access(self):
        self.urlparse = urllib.parse.urlparse(self.url)

        if self.urlparse.scheme != "http" and self.urlparse.scheme != "https":
            self.url = "{}://{}".format("http", self.url)
        temp_url = self.url
        if self.static_uri is not None:
            self.static_uri = urllib.request.quote(self.static_uri)
            self.url = "{}/{}".format(self.url, self.static_uri)
            self.static_uri = None
        try:
            req = urllib.request.Request(self.url)
            req.add_header("User-Agent", pcUserAgent[choice(list(pcUserAgent.keys()))])
            # req.add_header("cookie","none\r\n")
            req.add_header("Accept-Encoding", "gzip, deflate")
            req.add_header("Referer", self.url)
            raw_html_object = urllib.request.urlopen(req)
            raw_html_contents = raw_html_object.read()
            # get headers from server
            self.raw_headers = raw_html_object.headers
            self.code = raw_html_object.code
            self.contents = self.mygzip(raw_html_contents)
            # print(len(self.contents), self.code)
            self._htmlParser()
            self.url = temp_url
        except urllib.error.HTTPError as e:
            self.url = temp_url
            self.code = e.code
        except Exception as e:
            self.logger.warn(printInfo(__file__, "_htmlParser function: " + str(e)))

    def _htmlParser(self):
        """
        parse html
        :return:
        """
        try:
            bs_object = bs4.BeautifulSoup(self.contents, "html.parser")
            self.raw_body = str(bs_object.body)
            self.raw_title = bs_object.title.get_text()
            self.raw_head = str(bs_object.head)
        # print(type(self.raw_body))
        except Exception as e:
            self.logger.warn(printInfo(__file__, "_parser function: " + str(e)))
            self.raw_body = None
            self.raw_title = None
            self.raw_head = None

    def md5(self, data):
        m = hashlib.md5()
        try:
            m.update(data)
        except TypeError as e:
            m.update(data.encode("utf-8"))
        result = m.hexdigest()
        return result

    def mygzip(self, contents):
        if isinstance(contents, bytes):
            # print(isinstance(body,bytes))
            for code in self.encodeList:
                try:
                    # gzip decompress
                    try:
                        contents = gzip.decompress(contents).decode(code)
                        break
                    except OSError as e:
                        # self.logger.debug(printInfo(__file__, str(e)))
                        contents = contents.decode(code)
                        break

                except UnicodeDecodeError as e:
                    self.logger.debug(printInfo(__file__, str(e)))
                    continue

                except Exception as e:
                    self.logger.warning(printInfo(__file__, str(e)))
                    contents = ""
        return contents

    def test(self):
        pass
    # self.url = "www.glamor.site"


    # 	print(self.md5("qwewqr"))
    # 	# self.static_uri = "/2.txt"
    # 	self._access()
    # 	self._verify()
    # # self._header("sign","rule")


if __name__ == '__main__':
    t = PluginBase()
    url = "www.glamor.site"
    t.start(url)
