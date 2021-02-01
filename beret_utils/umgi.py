#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import urllib

from bereTools import tags


class HttpsAuth:
    def __init__(self, uri='https://ucs.umgi.digiplug.com/', user='onet_info', password='test'):
        self.user = user
        self.uri = uri
        self.password = password

    def url2txt(self, url, coding=False):
        """
        simple return text data from given url
        """

        if not '://' in url:
            url = ''.join([self.uri, url])
        #        try:
        if True:
            request = urllib.Request(url)
            base64string = base64.encodestring('%s:%s' % (self.user, self.password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            response = urllib.urlopen(request)
            if coding:
                return response.read().decode(coding)
            else:
                return response.read()


#        except:
#            return False


class UMGI:
    def __init__(self, uri='https://ucs.umgi.digiplug.com/', user='onet_info', password='test'):
        self.http = HttpsAuth(uri, user, password)
        self.products = {}
        for order in self.get_orders_xml():
            for product in self.get_products(order):
                self.products[product.isrc] = product

    def get_orders_xml(self):
        for url in tags('xmlfile', self.http.url2txt('GetOrders.aspx')):
            yield self.http.url2txt(url)

    def get_products(self, order):
        return map(lambda product: UMGIProduct(product, self.http), tags('product', order))


class UMGIProduct:
    def __init__(self, product_xml, http=None):
        self.http = http
        self._xml = product_xml
        self.assets = tags('asset', product_xml)
        self.urls = []
        self.isrc = tags('isrc', product_xml)[0]
        for asset in self.assets:
            if '<file_type>XML</file_type>' in asset:
                self.metadata_url = self.url4asset(asset)
            else:
                self.urls.append(self.url4asset(asset))
            if 'isrc' in asset:
                self.video = self.url4asset(asset)

    def url4asset(self, asset):
        return "Download.aspx?task_id=%s" % tags('task_id', asset)[0]

    def get_metadata(self):
        if self.http:
            return self.http.url2txt(self.metadata_url)

    def get_files(self):
        if self.http:
            for url in self.urls:
                yield self.http.url2txt(url)