##############################################################################
#
# Copyright (c) 2023 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Dummy fixture classes for SAML2 plugin test classes
"""


class DummySession(dict):

    def set(self, key, value):
        self[key] = value


class DummyUser:

    def __init__(self, name):
        self.name = name

    def getId(self):
        return self.name


class DummyResponse:

    def __init__(self):
        self.redirected = ''
        self.locked = False
        self.headers = {}
        self.status = None
        self.body = ''

    def redirect(self, target, status=302, lock=False):
        self.redirected = target
        self.locked = lock
        self.status = status

    def setHeader(self, name, value):
        self.headers[name] = value

    def setBody(self, body):
        self.body = body


class DummyRequest:

    def __init__(self):
        self.RESPONSE = self.response = DummyResponse()
        self.SESSION = DummySession()
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)


class DummyNameId:

    def __init__(self, name):
        self.name = name
        self.name_qualifier = 'name_qualifier_value'
        self.sp_name_qualifier = 'sp_name_qualifier_value'
        self.format = 'format_value'
        self.sp_provided_id = 'sp_provided_id_value'
        self.text = name

    def __str__(self):
        return f'<DummyNameId {self.text}>'


class DummyPySAML2Client:

    def __init__(self, parse_result=None):
        self.users = {}
        self.parse_result = parse_result

    def _store_name_id(self, name_id):
        self.users[str(name_id)] = True

    def is_logged_in(self, name_id):
        return bool(self.users.get(str(name_id)))

    def local_logout(self, name_id):
        del self.users[str(name_id)]

    def parse_authn_request_response(self, saml_response, binding):
        if self.parse_result == 'raise_error':
            raise Exception('PARSE FAILURE')
        return self.parse_result


class DummySAMLResponse:

    def __init__(self, subject=None, issuer='', identity={}):
        self._subject = subject
        self._issuer = issuer
        self._identity = identity

    def get_subject(self):
        return self._subject

    def issuer(self):
        return self._issuer

    def get_identity(self):
        return self._identity
