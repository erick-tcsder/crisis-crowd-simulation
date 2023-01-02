'''
    Automatic profiling and stat visualization tool.
'''
import cProfile as prof
import os
import pstats as st
from datetime import datetime
from os import path
from typing import Any, Callable, Dict, Iterable

DEBUG = True

LOG_DIR = None  # None to use default

PROFILE_DIR = None  # None to use default

EXECUTION_ID = (str(datetime.now())).replace(' ', '-').replace(':', '-')

__profiles__ = {}


def profileFunc(
        function: Callable, *_, f_args: Iterable[Any],
        f_kwargs: Dict[str, Any],
        stat_limit: int = 150,
        limit: int = 15):
    # Only profile if DEBUG is True
    if not DEBUG:
        r = function(*f_args, **f_kwargs)
        return r

    # Profiler initialization
    prof_dir = path.abspath(path.join(path.dirname(
        __file__), 'profiles'))

    profile_count = __profiles__.get(function.__name__, 0)+1
    if profile_count > limit:
        r = function(*f_args, **f_kwargs)
        return r

    PROFILE_ID = f"{function.__name__}.{profile_count:03d}"

    if PROFILE_DIR is not None:
        prof_dir = path.abspath(PROFILE_DIR)

    os.makedirs(prof_dir, exist_ok=True)

    prof_filename = path.join(
        prof_dir,
        f"{EXECUTION_ID}.{PROFILE_ID}.profile"
    )

    prof_file = open(prof_filename, mode='w')

    __profiles__[function.__name__] = profile_count
    pr = prof.Profile()

    pr.enable()  # Start Profiling

    r = function(*f_args, **f_kwargs)

    pr.disable()  # End profiling

    # Write profiler stats
    st.Stats(pr, stream=prof_file).sort_stats(
        st.SortKey.CUMULATIVE).print_stats(stat_limit)

    prof_file.close()

    return r  # Return the same the function returned


def profile(stat_limit: int = 150, limit: int = 15):
    def __profile_wrap(f: Callable):
        # Reduce nesting if not in DEBUG
        if not DEBUG:
            return f

        def __wrapper(*args, **kwargs):
            return profileFunc(f, f_args=args, f_kwargs=kwargs,
                               stat_limit=stat_limit, limit=limit)

        return __wrapper

    return __profile_wrap
