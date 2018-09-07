# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
# @Author : woodenrobot
from scrapy import cmdline
name = 'moviecount_youku'
name2 = 'movienews_tencent'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())