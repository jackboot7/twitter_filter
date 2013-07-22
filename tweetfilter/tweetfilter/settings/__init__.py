import sys
from common import *

try:
    from local import *
except sys.exc_info()[0], e:
    print e
