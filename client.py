# -*- coding: utf-8 -*-
import re
import grequests

class Client:
    def __init__(self, urlTemplate, params, rate=10):
        self.rate = rate
        self.url = self.substituteParams(urlTemplate, params)
    
    def substituteParams(self, urlTemplate, params):
        toReplace = {p: p for p in re.findall(r"\{(.+?)\}", urlTemplate)}
        print(set(params.keys()))
        print(set(toReplace.keys()))
        toAppend = {k: params[k] for k in (set(params.keys()) - set(toReplace.keys()))}
        url = urlTemplate
        for (k, v) in toReplace.items():
            url = re.sub("{%s}" % k, params[v], url)
        getParams = "&".join(["%s=%s" % (k,v) for k,v in sorted(toAppend.items())])
        return url + "?" + getParams if getParams else url


if __name__ == '__main__':
    u = 'http://www.foo.com/{bar}/{baz}/bam'
    ps = {'bar': 'mybar', 'baz': 'ubaz', 'foo': 'onefoo'}

    print(Client(u, ps).url)
