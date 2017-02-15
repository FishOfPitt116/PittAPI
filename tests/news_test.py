'''
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import unittest

import timeout_decorator

from PittAPI import news
from . import PittServerError


class NewsTest(unittest.TestCase):

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_default(self):
        self.assertIsInstance(news.get_news(), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_main(self):
        self.assertIsInstance(news.get_news("main_news"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_cssd(self):
        self.assertIsInstance(news.get_news("cssd"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_chronicle(self):
        self.assertIsInstance(news.get_news("news_chronicle"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_alerts(self):
        self.assertIsInstance(news.get_news("news_alerts"), list)

    @timeout_decorator.timeout(30, timeout_exception=PittServerError)
    def test_get_news_length(self):
        self.assertEqual(len(news.get_news()), 10)
        self.assertTrue(len(news.get_news(max_news_items=20)) <= 20)
        self.assertTrue(len(news.get_news(max_news_items=25)) <= 25)
        self.assertTrue(len(news.get_news(max_news_items=25)) <= 29)
        self.assertTrue(len(news.get_news(max_news_items=30)) <= 30)
        self.assertTrue(len(news.get_news(max_news_items=40)) <= 40)
