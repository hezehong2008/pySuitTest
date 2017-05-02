#!/usr/bin/env python
# -*- coding: UTF-8 -*


import urllib
url = urllib.parse.urlparse("https://yun.kujiale.com/dds/api/c/designdata/3FO4JX0MYXQF?t=1493701917949&diy-3d-20170427R2180B171=1")
_dict = {}
quote = urllib.parse.parse_qs(url.query, True)
if url.query:
    components = url.query.split("&")

    for item in components:
        param = item.split("=")[0]
        value = item.split("=")[1]
        _dict[param] = value
for item in quote:
    quote


class urlUtil(object):

    pass