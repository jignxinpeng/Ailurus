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

from __future__ import with_statement
import sys, os
from lib import *
from libapp import *

class SUN_JDK6(apt_install):
    __doc__ = _(u'SUN Java® 6.')
    detail = _('<span color="red">You should manually agree a license during the installation.</span>\n'
       'In the installation process, these commands will be executed: '
       '"sudo apt-get install sun-java6-jdk" and "update-java-alternatives -s java-6-sun". '
       'Then these environment variables is added into file "/etc/environment", which are JAVA_HOME, JAVA_BIN and CLASSPATH.')
    category = 'dev'
    manual = True
    license = 'Sun License'
    logo = 'java.png'
    def __init__(self):
        self.in_jvm = "/usr/lib/jvm/java-6-sun\n"
        self.jvm_file = '/etc/jvm'
    def __install_sun_jdk(self):
        APT.install('sun-java6-jdk')
    def install(self):
        self.__install_sun_jdk()
        env = ETCEnvironment()
        env.add('JAVA_HOME', '/usr/lib/jvm/java-6-sun')
        env.add('JAVA_BIN', '/usr/lib/jvm/java-6-sun/bin')
        env.add('CLASSPATH', '.', '/usr/lib/jvm/java-6-sun/lib/dt.jar', '/usr/lib/jvm/java-6-sun/lib/tools.jar')
        env.save()
        # this command will return 1 although java-6-sun is set as default. 
        # Therefore we use ignore_error==True
        gksudo('update-java-alternatives -s java-6-sun', ignore_error=True) 
        with TempOwn(self.jvm_file) as o:
            with open(self.jvm_file, "w") as f:
                f.write(self.in_jvm)
        with open('/usr/lib/jvm/java-6-sun/jre/lib/fontconfig.properties') as f:
            contents = f.readlines()
            for i, line in enumerate(contents):
                if line.endswith('uming.ttf\n'):
                    contents[i] = line.replace('uming.ttf\n', 'uming.ttc\n')
        with open('/usr/lib/jvm/java-6-sun/jre/lib/fontconfig.properties', 'w') as f:
            f.writelines(contents)

    def installed(self):
        return APT.installed('sun-java6-jdk')
    
    def remove(self):
        APT.remove('sun-java6-jdk', 'sun-java6-jre', 'sun-java6-bin')
        env = ETCEnvironment()
        env.remove('JAVA_HOME', '/usr/lib/jvm/java-6-sun')
        env.remove('JAVA_BIN', '/usr/lib/jvm/java-6-sun/bin')
        env.remove('CLASSPATH', '.', '/usr/lib/jvm/java-6-sun/lib/dt.jar', '/usr/lib/jvm/java-6-sun/lib/tools.jar')
        env.save()

class WINE(apt_install):
    __doc__ = _('WINE')
    detail = _('This is an indispensable application for running Windows applications on Linux.\n'
       'Command: sudo apt-get install wine wine-gecko')
    license = ('GNU Lesser General Public License, '
               'see http://wiki.winehq.org/Licensing')
    category = 'vm'
    time = 37
    size = 72280 * 1000
    international = True
    logo = 'wine.png'
    def __init__(self):
        self.pkgs = 'wine wine-gecko'
    def install(self):
        apt_install.install(self)
        import os
        if not os.path.exists( os.path.expanduser('~/.wine') ):
            run("wineprefixcreate") #Do not use 'winecfg' !
    def installed(self):
        if not apt_install.installed(self):
            return False
        import os
        if not os.path.exists( os.path.expanduser('~/.wine') ):
            return False
        return True

class WINE_Chinese(apt_install):
    __doc__ = _('WINE &amp; Wen-Quan-Yi Chinese font')
    detail = _('WINE is an indispensable application for running Windows applications on Linux.\n'
       'During the installation process, firstly "sudo apt-get install wine wine-gecko ttf-wqy-zenhei" command is executed, '
       'then Wen-Quan-Yi font is used as default Chinese font.')
    license = ('GNU Lesser General Public License, '
               'see http://wiki.winehq.org/Licensing')
    category = 'vm'
    time = 37
    size = 72280 * 1000
    Chinese = True
    logo = 'wine.png'
    def __init__(self):
        self.pkgs = 'ttf-wqy-zenhei wine wine-gecko'
        self.wqy = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
    def install(self):
        apt_install.install(self)
        import os
        if not os.path.exists( os.path.expanduser('~/.wine') ):
            run("wineprefixcreate") #Do not use 'winecfg' !
        run("cp %s ~/.wine/drive_c/windows/Fonts/"%self.wqy)
        run(r"wine regedit "+D+"../support/wine_wqy_font.reg")
    def installed(self):
        if not apt_install.installed(self):
            return False
        import os
        if not os.path.exists( os.path.expanduser('~/.wine') ):
            return False
        if not os.path.exists( os.path.expanduser('~/.wine/drive_c/windows/Fonts/wqy-zenhei.ttc') ):
            return False
        return True

def make_sure_JDK_installed():
    obj =  SUN_JDK6()

    if not obj.installed():
        print _('SUN_JDK6 is required. It is to be installed.')
        obj.install()

def make_sure_WINE_installed():
    if Config.is_Chinese_locale():
        obj =  WINE_Chinese()
    else:
        obj = WINE()

    if not obj.installed():
        print _('WINE is required. It is to be installed.')
        obj.install()
