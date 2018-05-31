#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: glamor
# @site: www.cmustard.com

from util.plugins import PluginBase

class Discuz(PluginBase):

    def plugin(self):
        """
        title,body,version,header,static,head,text"""
        self.cms_name = "Discuz"
        self.author = "cmustard"
        self.description = ""
        self.website = "www.discuz.net/forum.php"

        # detail
        matches = [
            {"header": r'Set-Cookie:_lastact.*_sid|_sid.*_lastact|_sid.*smile|smile.*_sid'},
            {"text":r'Powered by (?:Discuz!|<a href=\"http://www\\.discuz\\.net/\"|UCenter)'},
        ]

        return matches

if __name__ == '__main__':
    j = Discuz()
    url = "http://39.106.37.114:443/"
    j.start(url)