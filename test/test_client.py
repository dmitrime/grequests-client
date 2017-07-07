# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')

from client import Client

def test_url_sub_params():
    """ Params in the url are correctly substituted """

    template = 'http://www.foo.com/{bar}/{baz}/bam'
    params = {'bar': 'mybar', 'baz': 'ubaz', 'foo': 'onefoo'}
    assert Client((template, params)).urls[0] == 'http://www.foo.com/mybar/ubaz/bam?foo=onefoo'

def test_url_no_sub():
    """ Only get params are added (in sorted order) """

    template = 'http://www.foo.com'
    params = {'foo': 'bar', 'x': 'y'}
    assert Client((template, params)).urls[0] == 'http://www.foo.com?foo=bar&x=y'

def test_url_params_empty():
    """ No effect if params are empty """

    template = 'http://www.foo.com'
    params = {}
    assert Client((template, params)).urls[0] == 'http://www.foo.com'
