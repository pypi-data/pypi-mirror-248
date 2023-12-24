#########################################################################
#             GNU HEALTH HOSPITAL MANAGEMENT - GTK CLIENT               #
#                      https://www.gnuhealth.org                        #
#########################################################################
#       The GNUHealth HMIS client based on the Tryton GTK Client        #
#########################################################################
#
# SPDX-FileCopyrightText: 2008-2021 The Tryton Community <info@tryton.org>
# SPDX-FileCopyrightText: 2017-2023 GNU Health Community <info@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later


# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import os
import importlib
import gettext

from gnuhealth.config import get_config_dir, CURRENT_DIR

__all__ = ['MODULES', 'register']

_ = gettext.gettext

MODULES = []


def register():
    global MODULES
    paths = [
        os.path.join(get_config_dir(), 'plugins'),
        os.path.join(CURRENT_DIR, 'plugins'),
        ]
    paths = list(filter(os.path.isdir, paths))

    imported = set()
    for path in paths:
        finder = importlib.machinery.FileFinder(
            path, (
                importlib.machinery.SourceFileLoader,
                importlib.machinery.SOURCE_SUFFIXES))
        for plugin in os.listdir(path):
            module = os.path.splitext(plugin)[0]
            if (module.startswith('_') or module in imported):
                continue
            module = 'gnuhealth.plugins.%s' % module
            spec = finder.find_spec(module)
            if not spec:
                continue
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except ImportError:
                continue
            else:
                MODULES.append(module)
                imported.add(module.__name__)
