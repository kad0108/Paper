#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append("../")
import jieba
from pymongo import *

import re

text = u"欣欣专注于帮助旅游企业实现在线化，面向旅游行业提供旅游信息化、互联网化整体解决方案。旗下主要运营旅游B2b平台“欣欣同业”（www.cncn.net）和旅游顾问平台“欣欣旅游”（www.cncn.com）。"

pattern = re.compile(r'www\..*?\.com');

print pattern.sub("", text)

