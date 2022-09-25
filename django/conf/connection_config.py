from urllib import parse

from django.core.exceptions import ImproperlyConfigured
from django.utils import module_loading


def parse_connection_url(url):
    """
    A method to parse URLs into components that handles quirks
    with the stdlib urlparse, such as lower-cased hostnames.
    Also parses querystrings into typed components.
    """
    parsed = parse.urlparse(url)
    # parsed.hostname always returns a lower-cased hostname
    # this isn't correct if hostname is a file path, so use '_hostinfo'
    # to get the actual host
    hostname, port = parsed._hostinfo
    query = parse.parse_qs(parsed.query)
    params = {}

    for key, values in query.items():
        value = values[-1]
        if value.isdigit():
            value = int(value)
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False

        params[key] = value

    path = parsed.path[1:]
    if port:
        port = int(port)

    return {
        'username': parsed.username,
        'password': parsed.password,
        'hostname': hostname,
        'port': port,
        'path': path,
        'params': params,
    }


def _parse_connection_url(url, schemes):
    scheme, url = url.split('://', 1)
    backend_module_path = schemes.get(scheme, scheme)
    backend_class = module_loading.import_string(backend_module_path)
    return backend_class.connection_config_from_url(
        backend_module_path.replace(
            '.base.DatabaseWrapper', ''
        ),
        url,
    )


def _parse_connection_config(config, schemes, keys_invalid_with_url):
    if isinstance(config, str):
        return _parse_connection_url(config, schemes)
    url = config.pop("URL", None)
    if url:
        for k in keys_invalid_with_url:
            if k == "URL":
                raise ImproperlyConfigured("The %s key can't be used together with URL." % k)
        return {**config, **_parse_connection_url(url, schemes)}
    return config


def get_connection_configs(setting_name, setting_value):
    return {
        alias: _parse_connection_config(
            config,
            schemes=connection_config_settings[setting_name]["schemes"],
            keys_invalid_with_url=connection_config_settings[setting_name]["keys_invalid_with_url"],
        )
        for alias, config in setting_value.items()
    }


connection_config_settings = {
    "DATABASES": {
        "schemes": {
            "mysql": "django.db.backends.mysql.base.DatabaseWrapper",
            "oracle": "django.db.backends.oracle.base.DatabaseWrapper",
            "postgres": "django.db.backends.postgresql.base.DatabaseWrapper",
            "sqlite": "django.db.backends.sqlite3.base.DatabaseWrapper",
            "mysql+gis": "django.contrib.gis.db.backends.mysql.base.DatabaseWrapper",
            "oracle+gis": "django.contrib.gis.db.backends.oracle.base.DatabaseWrapper",
            "postgis": "django.contrib.gis.db.backends.postgis.base.DatabaseWrapper",
            "spatialite": "django.contrib.gis.db.backends.spatialite.base.DatabaseWrapper",
        },
        "keys_invalid_with_url": [
            "ENGINE",
            "OPTIONS",
            "NAME",
            "USER",
            "PASSWORD",
            "HOST",
            "PORT",
        ],
    },
    "CACHES": {
        "schemes": {
            "memory": "django.core.cache.backends.locmem.LocMemCache",
            "db": "django.core.cache.backends.db.DatabaseCache",
            "dummy": "django.core.cache.backends.dummy.DummyCache",
            "memcached": "django.core.cache.backends.memcached.BaseMemcachedCache",
            "memcached+pylibmccache": "django.core.cache.backends.memcached.PyLibMCCache",
            "file": "django.core.cache.backends.filebased.FileBasedCache",
        },
        "keys_invalid_with_url": [
            "BACKEND",
            "LOCATION",
            "OPTIONS",
        ],
    },
}
