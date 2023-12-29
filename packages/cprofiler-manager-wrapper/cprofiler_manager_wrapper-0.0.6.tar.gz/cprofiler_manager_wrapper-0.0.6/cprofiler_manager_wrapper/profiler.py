# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cProfile
from datetime import datetime
import os

from pathlib import Path

__all__ = [
    'Profiler',
]

TIME_FORMAT = "%H:%M:%S"


class ProfilerStorage:
    def __init__(self, profiler_object: cProfile.Profile, time: str = None):
        self.profile_object = profiler_object
        self.time = time


class Profiler:
    def __init__(self, comment: str, prof_folder: str = 'prof_folder', disable: bool = False):
        log_folder_abs_path = Path().absolute() / prof_folder
        if not log_folder_abs_path.exists():
            os.mkdir(log_folder_abs_path)

        self._log_folder_abs_path = log_folder_abs_path
        self._comment = comment
        self._is_disable = disable

    def __enter__(self):
        if self._is_disable:
            return
        now = datetime.now().strftime(TIME_FORMAT)
        profiler_object = cProfile.Profile()
        self._storage = ProfilerStorage(time=now, profiler_object=profiler_object)
        profiler_object.enable()
        return profiler_object

    def __exit__(self, exc_type, *args):
        if exc_type:
            return

        if self._is_disable:
            return

        profiler_object = self._storage.profile_object
        prof_filename = '{}__{}.prof'.format(
            self._comment,
            self._storage.time,
        )
        profiler_object.dump_stats(file=self._log_folder_abs_path / prof_filename)
        profiler_object.disable()
        return True
