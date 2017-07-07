# -*- coding: utf-8 -*-
import re
import grequests

class Client:
    def __init__(self, *urlParamsList, **kwargs):
        if 'rate' in kwargs:
            self.rate = kwargs['rate']
        self.urls = []
        for urlTemplate, params in urlParamsList:
            self.urls.append(self.substituteParams(urlTemplate, params))
    
    def substituteParams(self, urlTemplate, params):
        toReplace = {p: p for p in re.findall(r"\{(.+?)\}", urlTemplate)}
        toAppend = {k: params[k] for k in (set(params.keys()) - set(toReplace.keys()))}
        url = urlTemplate
        for (k, v) in toReplace.items():
            url = re.sub("{%s}" % k, params[v], url)
        getParams = "&".join(["%s=%s" % (k,v) for k,v in sorted(toAppend.items())])
        return url + "?" + getParams if getParams else url


if __name__ == '__main__':
    u = 'http://www.foo.com/{bar}/{baz}/bam'
    ps = {'bar': 'mybar', 'baz': 'ubaz', 'foo': 'onefoo'}

    lst = [(u, ps), (u, ps)]
    print(Client(*lst).urls)
