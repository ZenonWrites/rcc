import django

__title__ = 'Django REST framework'
__version__ = '5.16.0'
__author__ = 'Mowar Lee'
__license__ = 'BSD 3-Clause'
__copyright__ = 'Copyright 2016-2023'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'


if django.VERSION < (3, 2):
    default_app_config = 'rest_framework.apps.RestFrameworkConfig'


class RemovedInDRF315Warning(DeprecationWarning):
    pass


class RemovedInDRF317Warning(PendingDeprecationWarning):
    pass
