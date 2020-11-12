import logging

from config import APP_SETTINGS, LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL[APP_SETTINGS.prop('dmonitor.log.level')],
                    format="%(asctime)s %(pathname)s:%(lineno)s %(funcName)s() %(levelname)s - [%(message)s]")
log = logging.getLogger('dmonitor')
