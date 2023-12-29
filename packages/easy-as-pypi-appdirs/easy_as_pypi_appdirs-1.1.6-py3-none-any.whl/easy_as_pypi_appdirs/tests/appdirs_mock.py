# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-appdirs#🛣
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Public fixtures."""

import os
from unittest import mock

import pytest

from easy_as_pypi_appdirs.app_dirs_with_mkdir import AppDirsWithMkdir
from easy_as_pypi_appdirs.expand_and_mkdirs import must_ensure_directory_exists

__all__ = (
    "tmp_appdirs",
    "xdg_appdirs",
    # PRIVATE:
    #  'ensure_appdir_exists',
)

# XDG_* mapping as seen in appdirs source:
#  $(virtualenvwrapper_get_site_packages_dir)/appdirs.py
APPDIRS_DIRS = (
    ("user_data", "XDG_DATA_HOME"),
    ("site_data", "XDG_DATA_DIRS"),
    ("user_config", "XDG_CONFIG_HOME"),
    ("site_config", "XDG_CONFIG_DIRS"),
    ("user_cache", "XDG_CACHE_HOME"),
    ("user_state", "XDG_STATE_HOME"),
    ("user_log", ""),  # {XDG_CACHE_HOME}/log
)


@pytest.fixture
def tmp_appdirs(mocker, tmpdir):
    """Provide mocked AppDirs whose paths share a common base tmpdir."""

    def _tmp_appdirs():
        for appdir_dir_def in APPDIRS_DIRS:
            mocker_patch_app_dirs(mocker, tmpdir, appdir_dir_def[0])

        return AppDirsWithMkdir()

    def mocker_patch_app_dirs(mocker, tmpdir, appdir_dir):
        tmp_appdir = ensure_appdir_exists(tmpdir, appdir_dir)
        pkg_path = "easy_as_pypi_appdirs.app_dirs_with_mkdir.AppDirsWithMkdir"
        prop_name = "{}_dir".format(appdir_dir)
        target = "{}.{}".format(pkg_path, prop_name)
        mocker.patch(target, new_callable=mock.PropertyMock(return_value=tmp_appdir))

    return _tmp_appdirs()


@pytest.fixture
def xdg_appdirs(mocker, tmpdir):
    """Provide mocked AppDirs whose paths use tmpdir via XDG_* environs."""

    def _xdg_appdirs():
        for appdir_dir, xdg_environ in APPDIRS_DIRS:
            environ_patch_app_dirs(mocker, tmpdir, appdir_dir, xdg_environ)

        return AppDirsWithMkdir()

    def environ_patch_app_dirs(mocker, tmpdir, appdir_dir, xdg_environ):
        if not xdg_environ:
            return

        tmp_appdir = ensure_appdir_exists(tmpdir, appdir_dir)
        mocker.patch.dict(os.environ, {xdg_environ: tmp_appdir})

    return _xdg_appdirs()


def ensure_appdir_exists(tmpdir, appdir_dir):
    tmp_appdir = os.path.join(tmpdir.mkdir(appdir_dir).strpath, "easy-as-pypi-appdirs")
    # Because mocking property, which is wrapped by @mkdir_side_effect, do same,
    # albeit preemptively. (lb): Seriously, such a smelly side effect.
    must_ensure_directory_exists(tmp_appdir)
    return tmp_appdir
