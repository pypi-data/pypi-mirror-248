from flask import url_for

from flask_apikit.exceptions import APIError
from flask_apikit.responses import Pagination
from flask_apikit.views import APIView
from tests import AppTestCase


class PaginationTestCase(AppTestCase):
    def test_pagination(self):
        """测试返回分页"""

        class Ret(APIView):
            def get(self):
                return Pagination().set_data([1, 2], 101)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('X-Pagination-Count'), '101')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '1')
        self.assertEqual(headers.get('X-Pagination-Page-Count'), '11')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_pagination_with_status(self):
        """测试返回分页+状态码"""

        class Ret(APIView):
            def get(self):
                return Pagination(status_code=511).set_data([1, 2], 100)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('X-Pagination-Count'), '100')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '1')
        self.assertEqual(headers.get('X-Pagination-Page-Count'), '10')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_pagination_other_headers(self):
        """测试返回分页包含其他headers"""

        class Ret(APIView):
            def get(self):
                return Pagination(headers={'AAA': 'a', 'bbb': 'B'}).set_data([1, 2], 99)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('X-Pagination-Count'), '99')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '1')
        self.assertEqual(headers.get('X-Pagination-Page-Count'), '10')
        self.assertEqual(headers.get('AAA'), 'a')
        self.assertEqual(headers.get('bbb'), 'B')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_pagination_class(self):
        """测试Pagination，设置头和data"""

        class Ret(APIView):
            def get(self):
                return Pagination().set_data([1, 2], 101)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 100})
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('X-Pagination-Count'), '101')
        self.assertEqual(headers.get('X-Pagination-Limit'), '100')
        self.assertEqual(headers.get('X-Pagination-Page'), '2')
        self.assertEqual(headers.get('X-Pagination-Page-Count'), '2')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_get_pagination(self):
        """测试从Query中获取的分页参数"""

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 100})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 100)
        self.assertEqual(data['skip'], 100)

    def test_get_pagination_custom_key(self):
        """测试从Query中获取分页参数的自定义query中的key"""
        self.app.config['APIKIT_PAGINATION_PAGE_KEY'] = 'xpage'
        self.app.config['APIKIT_PAGINATION_LIMIT_KEY'] = 'xlimit'

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))

        # page，limit已经无效了，返回默认值
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 3, 'limit': 3})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 0)
        # 必须请求xpage，xlimit才行
        data, headers, status_code = self.get(url_for('ret'), query_string={'xpage': 3, 'xlimit': 3})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 3)
        self.assertEqual(data['limit'], 3)
        self.assertEqual(data['skip'], 6)

    def test_get_pagination_min_page(self):
        """测试从Query中获取分页参数的页数限制"""

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))

        # 请求page小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 0, 'limit': 10})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 0)
        # 请求page小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': -1, 'limit': 10})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 0)

    def test_get_pagination_default_max_limit(self):
        """测试从Query中获取分页参数的默认最大限制"""

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 2000})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 100)
        self.assertEqual(data['skip'], 100)

    def test_get_pagination_custom_max_limit(self):
        """测试从Query中获取分页参数的自定义最大限制"""
        self.app.config['APIKIT_PAGINATION_MAX_LIMIT'] = 1000

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 2000})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 1000)
        self.assertEqual(data['skip'], 1000)

    def test_get_pagination_default_default_limit(self):
        """测试从Query中获取分页参数的默认默认限制"""

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))

        # 请求limit小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 0})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 10)
        # 请求limit小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': -1})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 10)
        # 请求没有limit
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 10)
        self.assertEqual(data['skip'], 10)

    def test_get_pagination_custom_default_limit(self):
        """测试从Query中获取分页参数的自定义默认限制"""
        self.app.config['APIKIT_PAGINATION_DEFAULT_LIMIT'] = 20

        class Ret(APIView):
            def get(self):
                p = Pagination()
                return {'skip': p.skip, 'limit': p.limit, 'page': p.page}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))

        # 请求limit小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': 0})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 20)
        self.assertEqual(data['skip'], 20)
        # 请求limit小1
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2, 'limit': -1})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 20)
        self.assertEqual(data['skip'], 20)
        # 请求没有limit
        data, headers, status_code = self.get(url_for('ret'), query_string={'page': 2})
        self.assertEqual(status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['limit'], 20)
        self.assertEqual(data['skip'], 20)
