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
import configparser
import optparse
import os
import gettext
import logging
import sys
import locale

from gi.repository import GdkPixbuf

from gnuhealth import __version__

_ = gettext.gettext


def get_config_dir():
    # Allow releases in the form of major.minor.patch (X.Y.N)
    # and Release Candidate versions X.YrcN
    # Returns: X.Y
    return os.path.join(
        os.environ['HOME'], '.config', 'gnuhealth',
        '.'.join(__version__.split('.', 2)[:2]).split('rc')[0])


os.makedirs(get_config_dir(), mode=0o700, exist_ok=True)

# Create the GNU Health plugins directory at $HOME
GH_PLUGINS_DIR = os.path.join(os.environ['HOME'], 'gnuhealth_plugins')
if not os.path.isdir(GH_PLUGINS_DIR):
    os.makedirs(GH_PLUGINS_DIR, 0o700)


class ConfigManager(object):
    "Config manager"

    def __init__(self):
        demo_server = 'federation.gnuhealth.org'
        demo_database = ''
        self.defaults = {
            'login.profile': demo_server,
            'login.login': 'admin',
            'login.host': demo_server,
            'login.db': demo_database,
            'login.expanded': True,
            'client.title': 'GNU Health HMIS',
            'client.toolbar': 'default',
            'client.maximize': False,
            'client.save_width_height': True,
            'client.save_tree_state': True,
            'client.spellcheck': False,
            'client.lang': locale.getdefaultlocale()[0],
            'client.language_direction': 'ltr',
            'client.email': '',
            'client.can_change_accelerators': False,
            'client.limit': 1000,
            'client.bus_timeout': 10 * 60,
            'icon.colors': '#11b0b8',
            'tree.colors': '#777,#dff0d8,#fcf8e3,#f2dede',
            'calendar.colors': '#fff,#3465a4',
            'graph.color': '#3465a4',
            'image.max_size': 10 ** 6,
            'client.cli_position': 'top',
            'menu.pane': 200,
            'menu.expanded': True,
        }

        self.config = {}
        self.options = {}
        self.arguments = []

    def parse(self):
        parser = optparse.OptionParser(
            version=("GNU Health %s" % __version__),
            usage="Usage: %prog [options] [url]")
        parser.add_option(
            "-c", "--config", dest="config",
            help=_("specify alternate config file"))
        parser.add_option(
            "-d", "--dev", action="store_true",
            default=False, dest="dev",
            help=_("development mode"))
        parser.add_option(
            "-v", "--verbose", action="store_true",
            default=False, dest="verbose",
            help=_("logging everything at INFO level"))
        parser.add_option(
            "-l", "--log-level", dest="log_level",
            help=_("specify the log level: "
                   "DEBUG, INFO, WARNING, ERROR, CRITICAL"))
        parser.add_option(
            "-u", "--user", dest="login", help=_("specify the login user"))
        parser.add_option(
            "-s", "--server", dest="host",
            help=_("specify the server hostname:port"))
        opt, self.arguments = parser.parse_args()
        self.rcfile = opt.config or os.path.join(
            get_config_dir(), 'gnuhealth-client.conf')
        self.load()

        self.options['dev'] = opt.dev
        logging.basicConfig()
        loglevels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
            }
        if not opt.log_level:
            if opt.verbose:
                opt.log_level = 'INFO'
            else:
                opt.log_level = 'ERROR'
        logging.getLogger().setLevel(loglevels[opt.log_level.upper()])

        for arg in ['login', 'host']:
            if getattr(opt, arg):
                self.options['login.' + arg] = getattr(opt, arg)

    def save(self):
        try:
            parser = configparser.ConfigParser()
            for entry in list(self.config.keys()):
                if not len(entry.split('.')) == 2:
                    continue
                section, name = entry.split('.')
                if not parser.has_section(section):
                    parser.add_section(section)
                parser.set(section, name, str(self.config[entry]))
            with open(self.rcfile, 'w') as fp:
                parser.write(fp)
        except IOError:
            logging.getLogger(__name__).warn(
                _('Unable to write config file %s.')
                % (self.rcfile,))
            return False
        return True

    def load(self):
        parser = configparser.ConfigParser()
        parser.read([self.rcfile])
        for section in parser.sections():
            for (name, value) in parser.items(section):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                if section == 'client' and name == 'limit':
                    # First convert to float to be backward compatible with old
                    # configuration
                    value = int(float(value))
                self.config[section + '.' + name] = value
        return True

    def __setitem__(self, key, value, config=True):
        self.options[key] = value
        if config:
            self.config[key] = value

    def __getitem__(self, key):
        return self.options.get(key, self.config.get(key,
                                self.defaults.get(key)))


CONFIG = ConfigManager()
CURRENT_DIR = os.path.dirname(__file__)
if hasattr(sys, 'frozen'):
    CURRENT_DIR = os.path.dirname(sys.executable)
if not isinstance(CURRENT_DIR, str):
    CURRENT_DIR = str(CURRENT_DIR, sys.getfilesystemencoding())

PIXMAPS_DIR = os.path.join(CURRENT_DIR, 'data', 'pixmaps', 'gnuhealth')
if not os.path.isdir(PIXMAPS_DIR):
    # do not import when frozen
    import pkg_resources
    PIXMAPS_DIR = pkg_resources.resource_filename(
        'gnuhealth', 'data/pixmaps/gnuhealth')

GNUHEALTH_ICON = GdkPixbuf.Pixbuf.new_from_file(
    os.path.join(PIXMAPS_DIR, 'gnuhealth-icon.png'))

GH_ABOUT = GdkPixbuf.Pixbuf.new_from_file(
    os.path.join(PIXMAPS_DIR, 'gnuhealth-hmis-about.png'))

BANNER = 'banner.png'
