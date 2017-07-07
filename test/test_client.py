# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')

from client import Client

def test_url_sub_params():
    """ Params in the url are correctly substituted """

    template = 'http://www.foo.com/{bar}/{baz}/bam'
    params = {'bar': 'mybar', 'baz': 'ubaz', 'foo': 'onefoo'}
    c = Client((template, params, id))
    assert c.urls[0] == 'http://www.foo.com/mybar/ubaz/bam'
    assert c.data[0] == {'foo': 'onefoo'}

def test_url_no_sub():
    """ Only get params are added (in sorted order) """

    template = 'http://www.foo.com'
    params = {'foo': 'bar', 'x': 'y'}
    c = Client((template, params, id))
    assert c.urls[0] == 'http://www.foo.com'
    assert c.data[0] == {'foo': 'bar', 'x': 'y'}
