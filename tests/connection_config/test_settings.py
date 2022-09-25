from django.conf import LazySettings, Settings
from django.test import TestCase

settings = LazySettings()
settings.configure(Settings('tests.connection_config.settings'))


class SettingsTest(TestCase):
    def test_databases(self):
        result = settings.DATABASES
        self.assertEqual(result['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(result['default']['NAME'], ':memory:')
        # self.assertEqual(result['postgresql']['ENGINE'], 'django.db.backends.postgresql')
        # self.assertEqual(result['postgresql']['NAME'], 'd8r82722r2kuvn')
        # self.assertEqual(result['postgresql']['HOST'], '')
        # self.assertEqual(result['postgresql']['USER'], 'uf07k1i6d8ia0v')
        # self.assertEqual(result['postgresql']['PASSWORD'], '')
        # self.assertEqual(result['postgresql']['PORT'], 5435)
        self.assertEqual(result['mysql']['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(result['mysql']['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(result['mysql']['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(result['mysql']['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(result['mysql']['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(result['mysql']['PORT'], 3306)
        self.assertEqual(result['url_with_options']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(result['url_with_options']['NAME'], 'ess-cue-lite')
        self.assertTrue(result['url_with_options']['OPTIONS']['connect_timeout'], 1)
        self.assertEqual(result['with_url_key']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(result['with_url_key']['NAME'], 'ess-cue-lite')
        self.assertTrue(result['with_url_key']['ATOMIC_REQUESTS'])

    def test_caches(self):
        result = settings.CACHES
        self.assertEqual(result['default']['BACKEND'], 'django.core.cache.backends.locmem.LocMemCache')
        self.assertEqual(result['dummy']['BACKEND'], 'django.core.cache.backends.dummy.DummyCache')
        # self.assertEqual(result['memcached']['BACKEND'], 'django.core.cache.backends.memcached.MemcachedCache')
        # self.assertEqual(result['memcached']['LOCATION'], ['1.2.3.4:1567', '1.2.3.5:1568'])
        self.assertEqual(result['with_explicit_module_path']['BACKEND'], 'django.core.cache.backends.dummy.DummyCache'),
