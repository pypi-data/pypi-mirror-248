# #########################################################################################
# logit用到了logger的stacklevel参数，此参数在py3.8版本加入的，所以需要进行版本区分
# python version < 3.8 版本，logit不支持tag，例如：
# logit.debug("this is %s log", "debug", log_id=123456, tag1="value1", tag2=123456)
# #########################################################################################

import sys

from logit_python import base_logger
from logit_python.multi_logger import setup_multiprocess_logger

IS_PY_VERSION_GREATER_37: bool = '{}.{}'.format(sys.version_info[0], sys.version_info[1]) > '3.7'

if IS_PY_VERSION_GREATER_37:
    from logit_python import default_logger as logger
    from logit_python import db_logger

else:
    from logit_python.default_logger import _logger
    from logit_python.db_logger import _db_logger

    logger = _logger.logger
    db_logger = _db_logger.logger

level_trace = base_logger.level_trace
