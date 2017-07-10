# grequests client

HTTP fetching client that takes a list of `(URL, parameters and callback)` tuples and sends asynchronous requests to those URLs.
URLs may contain keys between `{` and `}` that will be replaced with values from the parameters dict.
The client supports GET and POST with simple throttling by sending requests at a given `rate` and waiting in between.
Uses [grequests](https://github.com/kennethreitz/grequests).

### Running

First install the requirements, import the client and use it as follows:

```python
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
```


### Testing

To run the tests do:

    py.test test
