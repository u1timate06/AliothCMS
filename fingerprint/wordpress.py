#!/usr/bin/env python
# __Author__:cmustard

from util.plugins import PluginBase


class Wordpress(PluginBase):
    def plugin(self):
        self.cms_name = "Wordpress"
        self.author = "Andrew Horton"
        self.description = "Wordpress is an opensource blogging system commonly used as a cms"
        self.website = "http://www.wordpress.org"

        # detail
        matches = []

        return matches
