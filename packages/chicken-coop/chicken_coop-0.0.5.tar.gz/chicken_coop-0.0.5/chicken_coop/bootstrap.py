from __future__ import annotations

import time
import sys
import os
import multiprocessing
from typing import ContextManager, Optional, Type
from types import TracebackType as Traceback

class WingDebuggerPause(ContextManager):
    def __enter__(self) -> WingDebuggerPause:
        try:
            wing_debugger = sys._wing_debugger # pytype: disable=module-attr
        except AttributeError:
            pass
        else:
            wing_debugger.SuspendDebug()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[Traceback]) -> Optional[bool]:
        try:
            wing_debugger = sys._wing_debugger # pytype: disable=module-attr
        except AttributeError:
            pass
        else:
            wing_debugger.ResumeDebug()


if os.environ.get('BOOTSTRAP_KERFUFFLE'):
    show_import_time = ((multiprocessing.current_process().name == 'MainProcess') and
                        sys.argv[0].endswith('chicken_coop/__main__.py') or
                        sys.argv[0].endswith('chicken_coop') or
                        sys.argv[0].endswith('_wing_run.py'))
    start_time = time.monotonic()
    if show_import_time:
        print('Starting Chicken Coop, importing heavy modules...')

        with WingDebuggerPause():
            from . import county # Importing this before ray because of filtros.

        if show_import_time:
            print(f'Done importing heavy modules in {time.monotonic() - start_time:.1f}s.')
else:
    from . import county # Importing this before ray because of filtros.
