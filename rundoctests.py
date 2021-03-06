#!/usr/bin/env python
#
# Run doctests for cysignals
#
# We add the ELLIPSIS flag by default and we run all tests even if
# one fails.
#

import os
import sys
import doctest

flags = doctest.ELLIPSIS

filenames = sys.argv[1:]
print("Doctesting {} files.".format(len(filenames)))

# For doctests, we want exceptions to look the same,
# regardless of the Python version. Python 3 will put the
# module name in the traceback, which we avoid by faking
# the module to be __main__.
from cysignals.signals import AlarmInterrupt, SignalError
for typ in [AlarmInterrupt, SignalError]:
    typ.__module__ = "__main__"


success = True
for f in filenames:
    print(f)
    sys.stdout.flush()

    # Test every file in a separate process (like in SageMath) to avoid
    # side effects from doctests.
    pid = os.fork()
    if not pid:
        # Child process
        try:
            failures, _ = doctest.testfile(f, module_relative=False, optionflags=flags)
            if not failures:
                os._exit(0)
        finally:
            os._exit(1)

    pid, status = os.waitpid(pid, 0)
    if status != 0:
        success = False

sys.exit(0 if success else 1)
