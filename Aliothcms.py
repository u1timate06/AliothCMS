#!/usr/bin/env python
# __Author__:cmustard


import optparse
import time

from util.cms import CmsDector

def main():
    # parser = optparse.OptionParser()
    # parser.add_option("--thread",dest="thread",default=10,help="special thread number")
    # parser.add_option("-u","--url",dest="url",help="target url")
    # options,args = parser.parse_args()
    # thread = options.thread
    # url = options.url
    # if url is None:
    #     exit(0)
    url = "http://182.87.0.20:8081/portal/bsdt.seam"
    thread = 10
    print(url,thread)

    cms = CmsDector()
    cms.run(url,thread,True)
    

if __name__ == '__main__':
    main()
