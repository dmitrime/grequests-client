# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')

from mock import patch
from pytest import fixture, raises
from client import Client

def test_url_sub_params(client):
    """ Params in the url are correctly substituted """
    (c, _output) = client
    assert c.urls[0] == _output[0]
    assert c.data[0] == _output[1]

@patch('grequests.get')
def test_get_req(get, client):
    (c, _) = client
    c.send(method='GET')
    get.assert_called()

@patch('grequests.post')
def test_post_req(post, client):
    (c, _) = client
    c.send(method='POST')
    post.assert_called()

def test_unknown_method(client):
    (c, _) = client
    with raises(ValueError):
        c.send(method='XXX')

@fixture
def client(client_data):
    return Client(client_data[0]), client_data[1]

@fixture(params = [
        (('http://www.foo.com/{bar}/{baz}/bam', {'bar': 'mybar', 'baz': 'ubaz', 'foo': 'onefoo'}, id), 
            ['http://www.foo.com/mybar/ubaz/bam', {'foo': 'onefoo'}]),

        (('http://www.foo.com', {'foo': 'bar', 'x': 'y'}, id),
            ['http://www.foo.com', {'foo': 'bar', 'x': 'y'}])
    ]
)
def client_data(request):
    return request.param
