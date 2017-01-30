# -*- coding: utf-8 -*-

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Development Team: Stanislav WEB
"""

import re
from urlparse import urlparse

from src.core import helper
from .exceptions import FilterError


class Filter:
    """Filter class"""

    URL_REGEX = "^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?:[-A-Za-z0-9]+\.)+([A-Za-z]|(?u)\w){2,6}$"

    @staticmethod
    def filter(args):
        """
        Filter options
        :param dict args:
        :return: dict
        """

        filtered = {}

        for key, value in args.iteritems():
            if 'scan' == key:
                filtered['scan'] = Filter.scan(value)
            elif 'host' == key:
                filtered['host'] = Filter.host(value)
                filtered['scheme'] = Filter.scheme(value)
                filtered['ssl'] = Filter.ssl(filtered['scheme'])
            else:
                if 'proxy' == key:
                    filtered[key] = Filter.proxy(value)
                else:
                    filtered[key] = value

        return filtered

    @staticmethod
    def scheme(host):
        """
        Get `host` scheme from input
        :param str host:
        :return: str
        """

        scheme = helper.parse_url(host).scheme
        if not scheme:
            scheme = 'http'
        return scheme + "://"

    @staticmethod
    def ssl(scheme):
        """
        If `ssl` in action
        :param str scheme:
        :return: bool
        """
        return 'https://' == scheme

    @staticmethod
    def host(host):
        """
        Input `host` param filter
        :param str host:
        :raise FilterError
        :return: str
        """

        if not re.search('http', host, re.IGNORECASE):
            if re.search('https', host, re.IGNORECASE):
                host = "https://" + host
            else:
                host = "http://" + host

        host = helper.parse_url(host).netloc

        regex = re.compile(r"" + Filter.URL_REGEX + "")

        if not regex.match(host):
            raise FilterError("\"{0}\" is invalid host in --host. Use ip, http(s) or just hostname".format(host))
        return host

    @staticmethod
    def proxy(proxyaddress):
        """
        Input `proxy` param filter
        :param str proxyaddress:
        :raise FilterError
        :return: str
        """

        proxy = urlparse(proxyaddress)

        if proxy.scheme not in ['http', 'https', 'socks4', 'socks5'] or None is proxy.port:
            raise FilterError("\"{0}\" is invalid proxy in --proxy. Use scheme:ip:port format".format(proxyaddress))
        return proxyaddress

    @staticmethod
    def scan(choise):
        """
        Input `scan` type filter
        :param str choise:
        :return: str
        """

        if choise not in ['directories', 'subdomains']:
            choise = 'directories'
        return choise
