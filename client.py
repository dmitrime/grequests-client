# -*- coding: utf-8 -*-
import re
import time
import grequests

class Client:
    def __init__(self, *urlParamsList, **kwargs):
        """ Construct the object by parsing all parameters """
        self.urls = []
        self.data = []
        self.callbacks = []
        for urlTemplate, params, func in urlParamsList:
            url, remainingParams = self._substituteParams(urlTemplate, params)
            self.urls.append(url)
            self.data.append(remainingParams)
            self.callbacks.append(func)
    
    def _substituteParams(self, urlTemplate, params):
        """ Substitute the parts in url template between { and } with values found in `params` dict.
            Return the rest of the `params` for later use.
        """
        toReplace = {p: p for p in re.findall(r"\{(.+?)\}", urlTemplate)}
        toAppend = {k: params[k] for k in (set(params.keys()) - set(toReplace.keys()))}
        url = urlTemplate
        for (k, v) in toReplace.items():
            url = re.sub("{%s}" % k, params[v], url)
        return url, toAppend

    def _get(self, url, params, timeout):
        """ Wrapper for grequests.get """
        return grequests.get(url, params=params, timeout=timeout)

    def _post(self, url, params, timeout):
        """ Wrapper for grequests.post """
        return grequests.post(url, data=params, timeout=timeout)

    def send(self, method='GET', rate=10, wait=0.5, timeout=1):
        """ Send concurrent HTTP requests (GET or POST) to the urls, `rate` urls at a time,
            waiting `wait` seconds in between and with the same timeout for all urls.
        """
        if method not in set(['GET', 'POST']):
            raise ValueError("Only GET and POST are supported")
        method = self._get if method == 'GET' else self._post
        reqs = zip(self.urls, self.data, self.callbacks)
        for i in range(0, len(self.urls), rate):
            urls, params, funcs = zip(*reqs[i:i+rate])
            rs = (method(u, ps, timeout=timeout) for u, ps in zip(urls, params))
            map(lambda (f, r): f(r), zip(funcs, grequests.map(rs)))
            time.sleep(wait)


if __name__ == '__main__':
    u = 'http://localhost:8000'
    ps = {'q': 'python'}
    def callback(resp):
        msg = resp.status_code if resp is not None else "None"
        print(msg)

    lst = [(u, ps, callback)]*5
    Client(*lst).send(method="GET", rate=2)
