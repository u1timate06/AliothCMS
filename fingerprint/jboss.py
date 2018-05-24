#!/usr/bin/env python
# __Author__:cmustard


from util.plugins import PluginBase

class JBoss(PluginBase):

    def plugin(self):
        self.cms_name = "JBoss"
        self.description = 'JBoss Application Server is the #1 most widely used Java application server on the market. A Java EE certified platform for developing and deploying enterprise Java applications, Web applications, and Portals, JBoss Application Server provides the full range of Java EE 5 features as well as extended enterprise services including clustering, caching, and persistence. - Homepaeg: http://www.jboss.org/jbossas/'
        self.author = ''

        matches = [
            {"title":'Welcome to JBoss AS'},
            {"text":'<a href="/admin-console/">Administration Console</a>'},
            {"text":'<a href="/web-console/">Jboss Web Consile</a>'},
            {"text":'<a href="/jmx-console/">JMX Console</a>'},
            {"header":r'x-powered-by:JBossWeb-[^\/^\s^,]+'},
            {"header":r'x-powered-by:JBoss(AS)?-([^\/^\s]+)'},
        ]

        return matches


if __name__ == '__main__':
    j = JBoss()
    url = "http://182.87.0.20:8081/portal/bsdt.seam"
    j.start(url)