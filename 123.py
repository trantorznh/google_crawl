# -*- coding: utf8 -*-
import re
import os
import requests
import codecs
import sys
from StringIO import StringIO

# you may change this
f = codecs.open('namelist.txt', 'r', 'utf-8')
pageNum = 1
perpage = 20  # limit by google

search_word = map(lambda x: x.strip(), f.readlines())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
}

# re
picsUrlPattern = re.compile(r'imgurl=(.+?)&amp;imgrefurl')

fw = codecs.open('fordownload.txt', 'w', 'utf-8')
fw_page = codecs.open('page.txt', 'w', 'utf-8')
bid=3072
for name in search_word:
    picsNum = 1
    for j in range(pageNum):
        queryUrl = 'https://www.google.com.hk/search?safe=strict&tbm=isch&ijn=%s&start=%s&q=%s&tbs=itp:face' % (j, perpage * j, name)
        print queryUrl
        try:
            picsPage = requests.get(queryUrl).content
            fw1=open('123.txt','w')
            fw1.write(picsPage)
            fw1.close()
            sys.exit()
            print picsPage
            fw_page.write(StringIO(picsPage))
            print 'successfully get page %s of %s' % (j + 1, name)
        except:
            print 'fail in '+ queryUrl
            continue

        picsUrlList = picsUrlPattern.findall(picsPage)
        if len(picsUrlList)==0:
            print name
# continue
            #fw.close()
            #sys.exit()
        for pics in picsUrlList:
            newPath = os.path.join(name, '%s_google.jpg' % picsNum)
            fw.write(pics + '\t' + newPath + '\n')
            picsNum += 1

# fw.close()
