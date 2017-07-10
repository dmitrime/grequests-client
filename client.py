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

    def _doChecks(self, method, rate, wait, timeout):
        if method not in set(['GET', 'POST']):
            raise ValueError("Only GET and POST are supported")
        if rate < 1:
            raise ValueError("Rate must be positive")
        if wait < 0:
            raise ValueError("Wait time must be non-negative")
        if timeout <= 0:
            raise ValueError("Timeout must be positive")

    def send(self, method='GET', rate=10, wait=0.5, timeout=1):
        """ Send concurrent HTTP requests (GET or POST) to the urls, `rate` urls at a time,
            waiting `wait` seconds in between and with the same timeout for all urls.
        """
        self._doChecks(method, rate, wait, timeout)

        callmethod = self._get if method == 'GET' else self._post
        reqs = zip(self.urls, self.data, self.callbacks)
        for i in range(0, len(self.urls), rate):
            urls, params, funcs = zip(*reqs[i:i+rate])
            rs = (callmethod(u, ps, timeout) for u, ps in zip(urls, params))
            map(lambda (f, r): f(r), zip(funcs, grequests.map(rs, exception_handler=Client.exception_handler)))
            if i+rate < len(self.urls):
                time.sleep(wait)

    @staticmethod
    def exception_handler(request, exception):
        print("FAILED: %s" % exception.message)


if __name__ == '__main__':
    def callback(resp):
        if resp is not None:
            print(resp.status_code)

    lst = [
            ('http://localhost:8000', {'lang': 'python'}, callback),
            ('http://localhost:8000/{bar}', {'bar': 'foo'}, callback),
            ('http://localhost:8000/{foo}', {'foo': 'bar'}, callback),
            ('http://localhost:8000/{foo}/{bar}/ws', {'foo': 'bar', 'bar': 'foo', 'lang': 'python'}, callback)
    ]
    Client(*lst).send(method='GET', rate=2)
