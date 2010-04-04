#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
#
# Ailurus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ailurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ailurus; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import sys, os
from libapp import *
from lib import *

class ChangeTerminalColor(_set_gconf):
    __doc__ = _('Change background color of GNOME terminal to black.')
    detail = _('Set background color to black. Set foreground color to white.\n'
       'The trick is to change GConf values:\n'
       '/apps/gnome-terminal/profiles/Default/use_theme_colors = False\n'
       '/apps/gnome-terminal/profiles/Default/background_color = #000000000000\n'
       '/apps/gnome-terminal/profiles/Default/foreground_color = #FFFFFFFFFFFF')
    logo = 'terminal-color.png'
    def __init__(self):
        self.set=(
('/apps/gnome-terminal/profiles/Default/use_theme_colors',False,True), 
('/apps/gnome-terminal/profiles/Default/background_color','#000000000000','#FFFFFFFFFFFF'), 
('/apps/gnome-terminal/profiles/Default/foreground_color','#FFFFFFFFFFFF','#000000000000'),
                  )
        self.add=()

class NScripts():
    __doc__ = _('NScripts: a set of useful Nautilus scripts')
    detail = _('NScripts help you change the background, create/check MD5 checksums, create a diff, create shortcuts via Nautilus. '
               'Its web site is http://freshmeat.net/projects/nscripts . '
               'NScripts is installed in ~/.gnome2/nautilus-scripts.')
    license = 'GNU General Public License v3'
    logo = 'nautilus.png'
    category = 'nautilus'

    def install(self):
        f = R('http://www.nanolx.org/free/NScripts-3.6.tar.bz2').download()
        import os
        dir = os.path.expanduser('~/.gnome2/nautilus-scripts/')
        if not os.path.exists(dir): os.mkdir(dir)
        FileServer.chdir('/tmp')
        try:
            os.system('tar xf ' + f)
            os.system('cp -r nscripts/* ' + dir)
            os.remove(dir + 'ChangeLog')
            os.remove(dir + 'TODO')
            os.system('touch ' + dir +'.nscripts_is_installed')
        finally:
            FileServer.chdir_back()

    def installed(self):
        import os
        d = os.path.expanduser('~/.gnome2/nautilus-scripts/.nscripts_is_installed')
        return os.path.exists(d)

    def remove(self):
        for dir in ['Admin', 'Files', 'Root', 'Utils']:
            os.system('rm -rf ~/.gnome2/nautilus-scripts/' + dir)
        os.system('rm ~/.gnome2/nautilus-scripts/.nscripts_is_installed')

class Gedit_GB2312(_set_gconf) :
    __doc__ = _('Add GB2312 detection ability to GEdit')
    detail = _('The trick behind is to change GConf values:\n'
       '/apps/gedit-2/preferences/encodings/auto_detected += ["GB2312", "GBK", "GB18030"]\n'
       '/apps/gedit-2/preferences/encodings/shown_in_menu += ["GB2312"]')
    Chinese = True
    logo = 'gedit.png'
    def __init__(self):
        self.set = ()
        self.add = (
('/apps/gedit-2/preferences/encodings/auto_detected', [ 'GB2312', 'GBK', 'GB18030' ] ),
('/apps/gedit-2/preferences/encodings/shown_in_menu', [ 'GB2312' ] ),
                    )
    def get_reason(self, f):
        self._get_reason(f)

class Speedup_Nautilus():
    __doc__ = _('Speed up Nautilus')
    detail = _('Change Nautilus settings: '
       'Do not count directory items. Do not preview sound. '
       'Do not show texts in icon. Use tighter layout. \n'
       'The trick behind is to change GConf settings as follows.\n'
       '/apps/nautilus/preferences/show_directory_item_counts = never\n'
       '/apps/nautilus/preferences/preview_sound = never\n'
       '/apps/nautilus/preferences/show_icon_text = never\n'
       '/apps/nautilus/icon_view/default_use_tighter_layout = true')
    logo = 'nautilus.png'
    category = 'nautilus'
    set_gconf = ['/apps/nautilus/preferences/show_icon_text',
                     '/apps/nautilus/preferences/show_directory_item_counts',
                     '/apps/nautilus/preferences/preview_sound',
                     '/apps/nautilus/list_view/default_visible_columns', 
                     '/apps/nautilus/icon_view/default_use_tighter_layout', ]
    def __init__(self):
        pass
        
    def install(self):
        import gconf
        g = gconf.client_get_default()
        for string in self.set_gconf[0:3]:
            g.set_string(string, 'never')
        value = g.get_list(self.set_gconf[3], gconf.VALUE_STRING)
        if 'size' in value:
            value.remove('size')
        g.set_list(self.set_gconf[3], gconf.VALUE_STRING, value)
        g.set_bool(self.set_gconf[4], True)
    def remove(self):
        import gconf
        g = gconf.client_get_default()
        value = g.get_list(self.set_gconf[3], gconf.VALUE_STRING)
        if 'size' not in value:
            value.insert(1,'size')
        g.set_list(self.set_gconf[3], gconf.VALUE_STRING, value)
        g.set_bool(self.set_gconf[4], False)
        for string in self.set_gconf[0:3]:
            g.set_string(string,  'local_only')
    def installed(self):
        import gconf
        g = gconf.client_get_default()
        value = g.get_list(self.set_gconf[3], gconf.VALUE_STRING)
        if(
        'size' in value and
        g.get_bool(self.set_gconf[4]) == False and
        g.get_string(self.set_gconf[0]) == 'local_only' and
        g.get_string(self.set_gconf[1]) == 'local_only' and
        g.get_string(self.set_gconf[2]) == 'local_only'
        ):
            return False
        else:
            return True
    def _get_reason(self, f):
        pass