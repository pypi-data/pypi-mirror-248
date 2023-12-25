# -*- coding: utf-8 -*-
# @author: xiao bai
import requests

from zerorunner_consul import consul
from zerorunner_consul import http_client

__all__ = ['Consul']


class HTTPClient(http_client.HTTPClient):
    def __init__(self, *args, **kwargs):
        super(HTTPClient, self).__init__(*args, **kwargs)
        self.session = requests.session()

    @staticmethod
    def response(response):
        response.encoding = 'utf-8'
        return consul.Response(
            response.status_code,
            response.headers,
            response.text,
            response.content)

    def get(self, callback, path, params=None, headers=None):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.get(uri,
                             headers=headers,
                             verify=self.verify,
                             cert=self.cert,
                             timeout=self.timeout)))

    def put(self, callback, path, params=None, data='', headers=None):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.put(uri,
                             data=data,
                             headers=headers,
                             verify=self.verify,
                             cert=self.cert,
                             timeout=self.timeout)))

    def delete(self, callback, path, params=None, data='', headers=None):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.delete(uri,
                                data=data,
                                headers=headers,
                                verify=self.verify,
                                cert=self.cert,
                                timeout=self.timeout)))

    def post(self, callback, path, params=None, headers=None, data=''):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.post(uri,
                              data=data,
                              headers=headers,
                              verify=self.verify,
                              cert=self.cert,
                              timeout=self.timeout)))


class Consul(consul.Consul):
    @staticmethod
    def http_connect(host, port, scheme, verify=True, cert=None, timeout=None):
        return HTTPClient(host, port, scheme, verify, cert, timeout)
