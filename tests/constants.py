from pyctd.manager.database import DbManager
import unittest

class ConnectionMixin(unittest.TestCase):
    def setUp(self):
        super(ConnectionMixin, self).setUp()
        self.dir, self.path, self.connection = make_temp_connection()
        log.info('Test generated connection string %s', self.connection)

    def tearDown(self):
        super(ConnectionMixin, self).tearDown()
        tear_temp_connection(self.dir, self.path)

class TemporaryCacheMixin(ConnectionMixin):
    def setUp(self):
        super(TemporaryCacheMixin, self).setUp()
        self.manager = DbManager(connection=self.connection)