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

class Varkon(apt_install, path_lists):
    __doc__ = _('Varkon: A concise CAD software')
    detail = ( _('Be good at geometric modeling. '
                 'Please study the documentation '
                 '<span color="blue"><u>http://varkon.sourceforge.net/man.htm</u></span> before using it. ') +
               _(u'Developed by Örebro university, Sweden.') )
    category = 'em'
    license = 'GNU General Public License (GPL), Lesser GNU General Public License (LGPL)'
    size = 5000000
    time = 10
    logo = 'varkon.png'
    def __init__(self):
        self.pkgs = 'varkon-user-manual varkon'
        self.shortcut = '/usr/share/applications/varkon.desktop'
        self.paths = [ self.shortcut ]
    def install(self):
        apt_install.install(self)
        create_file(self.shortcut, '''[Desktop Entry]
Name=Varkon
Exec=/usr/bin/varkon
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering;''')
    def installed(self):
        return apt_install.installed(self)
    def remove(self):
        apt_install.remove(self)
        gksudo('rm -f %s'%self.shortcut)

class FreeCAD(apt_install):
    __doc__ = _('FreeCAD: A CAD software based on OpenCasCade')
    detail = _('Be good at three-dimensional solid design. Official site: <span color="blue"><u>http://sourceforge.net/projects/free-cad/</u></span>')
    category = 'em'
    license = ('GNU General Public License (GPL), GNU Library or Lesser General Public License (LGPL). '
               'See http://sourceforge.net/projects/free-cad/')
    size = 15724000
    time = 51
    logo = 'freecad.png'
    def __init__(self):
        self.pkgs = 'freecad'
    def install(self):
        if get_arch()==32 and Config.get_Ubuntu_version()=='hardy':
            
            r=R(
['http://tdt.sjtu.edu.cn/S/freecad_0.8.2237-1hardy1_i386.deb',
'http://ncu.dl.sourceforge.net/project/free-cad/FreeCAD%20Linux/FreeCAD%200.8%20R2237/freecad_0.8.2237-1hardy1_i386.deb'],
5481522, '366835db62f7f2ffb73908ad6e77c82be826fc35')

        elif get_arch()==32 and Config.get_Ubuntu_version()=='intrepid':
            
            r=R(
['http://tdt.sjtu.edu.cn/S/freecad_0.8.2237-1intrepid1_i386.deb',
'http://ncu.dl.sourceforge.net/project/free-cad/FreeCAD%20Linux/FreeCAD%200.8%20R2237/freecad_0.8.2237-1intrepid1_i386.deb'],
5138150, '58ec68193200787d3f237016f0c6ba9e36021cbf')
            
        elif get_arch()==32 and Config.get_Ubuntu_version()=='jaunty':
            
            r=R(
['http://tdt.sjtu.edu.cn/S/freecad_0.8.2237-1jaunty1_i386.deb',
'http://ncu.dl.sourceforge.net/project/free-cad/FreeCAD%20Linux/FreeCAD%200.8%20R2237/freecad_0.8.2237-1jaunty1_i386.deb'],
5174974, 'f98fb51f95a1630d754480740ee0f192e30a2acf')
            
        elif get_arch()==64 and Config.get_Ubuntu_version()=='jaunty':
            
            r=R(
['http://tdt.sjtu.edu.cn/S/freecad_0.8.2237-1jaunty1_amd64.deb',
'http://ncu.dl.sourceforge.net/project/free-cad/FreeCAD%20Linux/FreeCAD%200.8%20R2237/freecad_0.8.2237-1jaunty1_amd64.deb'],
5267100, '681c05fd60b10a8b37661c339eb77debff881305')
            
        f = r.download()
        
        depends = DPKG.get_deb_depends(f)
        depends.remove('libgl1-mesa')
        depends.append('libgl1-mesa-dev')
        for depend in depends:
            gksudo('apt-get install -qq %s'%depend)
        gksudo('dpkg -i %s'%f)
        APT.cache_changed()
    def support(self):
        ver = Config.get_Ubuntu_version()
        if ver=='jaunty': return True
        if ver in ['hardy', 'intrepid'] and get_arch()==32: return True 
        return False

class QCad(apt_install):
    'QCad'
    detail = _('A CAD software which supports DXF-format. ')
    category = 'em'
    license = 'Non-free with limited-time free trial (professional edition) or GPL (community edition)'
    size = 18056000
    logo = 'qcad.png'
    def __init__(self):
        self.pkgs = 'qcad'

class Moonlight(apt_install):
    __doc__ = _(u'Moonlight: an open source implementation of Microsoft® Silverlight')
    detail = _(u'Moonlight provides Windows® media codecs. '
       u'By this application, you can enjoy Windows® video/audio in webpages.\n'
       'Command: sudo apt-get install moonlight-plugin-mozilla')
    license = ('Moonlight 2.0 is licensed under LGPL and MIT X11 licenses. '
               'Moonlight 1.0 is licensed under LGPL. '
               'See http://www.mono-project.com/Moonlight')
    category = 'media'
    logo = 'moonlight.png'
    def __init__(self):
        self.pkgs = 'moonlight-plugin-mozilla'

#class Moonlight_Chinese_Font_Bug:
#    __doc__ = _('Eliminate Moonlight Chinese font bug')
#    detail = _('Eliminate the bug that Chinese characters are displayed as blank square.')
#    category = 'media'
#    Chinese = True
#    logo = 'moonlight.png'
#    def install(self):
#        try:
#            FileServer.chdir('/usr/share/fonts/truetype/')
#            if not os.path.exists('msyh'):
#                gksudo('mkdir msyh')
#            os.chdir('msyh')
#            
#            f = R(
#['http://tdt.sjtu.edu.cn/S/msyh.tar.bz2',],
#16587122, 'b5b34bd523802510ddf4949358cd445b0693c5bc').download()
#
#            gksudo('tar xf %s'%f)
#            gksudo('mkfontscale')
#            gksudo('mkfontdir')
#            gksudo('fc-cache')
#            gksudo('chmod a+rX . -R')
#        finally:
#            FileServer.chdir_back()
#    def installed(self):
#        return os.path.exists('/usr/share/fonts/truetype/msyh')
#    def remove(self):
#        gksudo('rm -rf /usr/share/fonts/truetype/msyh')

class DisableGetty:
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    logo = 'tty.png'
    def support(self):
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty']
    def installed(self):
        FileServer.chdir('/etc/event.d/')
        try:
            for i in range(2,7):
                if file_contain('tty%s'%i, 'start on runlevel 2'):
                    return False
            return True
        finally:
            FileServer.chdir_back()
    def install(self):
        FileServer.chdir('/etc/event.d/')
        try:
            for i in range(2,7):
                filename = 'tty%s'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='start on runlevel 2\n':
                            contents[j]='stop on runlevel 2\n'
                        elif line=='start on runlevel 3\n':
                            contents[j]='stop on runlevel 3\n'
                    with open(filename, 'w') as f:
                        f.writelines(contents)
        finally:
            FileServer.chdir_back()
    def remove(self):
        FileServer.chdir('/etc/event.d/')
        try:
            for i in range(2,7):
                filename = 'tty%s'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='stop on runlevel 2\n':
                            contents[j]='start on runlevel 2\n'
                        elif line=='stop on runlevel 3\n':
                            contents[j]='start on runlevel 3\n'
                    with open(filename, 'w') as f:
                        f.writelines(contents)
        finally:
            FileServer.chdir_back()

class DisableGettyKarmic(DisableGetty):
    __doc__ = DisableGetty.__doc__
    logo = 'tty.png'
    def support(self):
        return Config.get_Ubuntu_version() in ['karmic']
    def installed(self):
        FileServer.chdir('/etc/init/')
        try:
            for i in range(2,7):
                if file_contain('tty%s.conf'%i, 'exec /sbin/getty -8 38400 tty%s'%i):
                    return False
            return True
        finally:
            FileServer.chdir_back()
    def install(self):
        FileServer.chdir('/etc/init/')
        try:
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line.strip()=='exec /sbin/getty -8 38400 tty%s'%i:
                            contents[j]='#exec\n'
                            break
                    else:
                        raise Exception('Not found')
                    with open(filename, 'w') as f:
                        f.writelines(contents)
        finally:
            FileServer.chdir_back()
    def remove(self):
        FileServer.chdir('/etc/init/')
        try:
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename) as o:
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line=='#exec\n':
                            contents[j]='exec /sbin/getty -8 38400 tty%s\n'%i
                            break
                    else:
                        raise Exception('Not found')
                    with open(filename, 'w') as f:
                        f.writelines(contents)
        finally:
            FileServer.chdir_back()

#class TencentQQ:
#    __doc__ = "QQ"
#    detail = _(u'Tencent® QQ. Official site: <span color="blue"><u>http://im.qq.com/qq/linux/</u></span>')
#    category = 'internet'
#    size = 6264000
#    time = 14
#    Chinese = True
#    logo = 'qq.png'
#    def install(self):
#        f = R(
#['http://tdt.sjtu.edu.cn/S/linuxqq_v1.0.2-beta1_i386.deb',
#'http://dl_dir.qq.com/linuxqq/linuxqq_v1.0.2-beta1_i386.deb'],
#5028066, 'a8ef309143c86019819a01fa5f7163d81c722c43').download()
#
#        gksudo('dpkg --install --force-architecture %s'%f)
#        APT.cache_changed() #do not use DPKG.install_deb(), since the dependency is wrong.
#    def installed(self):
#        return DPKG.installed('linuxqq')
#    def remove(self):
#        gksudo('dpkg --purge linuxqq')

class Octave(apt_install):
    __doc__ = 'Octave'
    detail = _(u'A Matlab® compatible numerical computation appliation.\n'
       'Command: sudo apt-get install qtoctave')
    logo = 'octave.png'
    license = 'GNU General Public License (GPL)'
    category = 'math'
    time = 16
    size = 1736000
    def __init__(self):
        self.pkgs = 'qtoctave'
    def remove(self):
        apt_install.remove(self)
        gksudo('apt-get remove octave* -qq')

class Generic_Genome_Browser:
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>') 
    category='biology'
    license = ('Creative Commons Licence'
               'see http://gbrowse.org/wiki/index.php/GBrowse:Copyrights') 
    logo = 'generic_genome_browser.png'
    def install(self):
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run('sudo perl %s' %f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class Realplayer32:
    'RealPlayer® 11'
    detail = _('If you cannot play RMVB video, try this application!\n'
       'Official site: <span color="blue"><u>http://www.real.com/linux</u></span>')
    size = 19911000
    category = 'media'
    license = 'Proprietary'
    logo = 'realplayer.png'
    def install(self):
        f = R(
['http://tdt.sjtu.edu.cn/S/RealPlayer11GOLD.deb',
'http://software-dl.real.com/13e4dfe0c5f6c7d54105/unix/RealPlayer11GOLD.deb'],
8632310, '85aefc200314b3d0b11f5820e1139a9d0338154b').download()
        gksudo('dpkg -i --force-all %s'%f)
    def installed(self):
        return DPKG.installed('realplay')
    def remove(self):
        gksudo('dpkg --purge realplay')

class Screenlets(apt_install):
    __doc__ = _('Screenlets')
    detail = _('Screenlets is able to add eye candy gadgets on desktop, '
       'such as sticky notes, clocks, weather forecasts, calendars and so on, '
       'in order to decorate the desktop.\n'
       'Command: sudo apt-get install screenlets')
    category = 'appearance'
    license = 'GNU General Public License (GPL)'
    logo = 'screenlets.png'
    size = 9089000
    def __init__(self):
        self.pkgs = 'screenlets'

class CompizSettingManager(apt_install):
    __doc__ = _('Compiz settings manager')
    detail = _('Compiz Fusion is the unification of the Beryl project and the community around the Compiz Window Manager. '
       'Compiz settings manager is the configuration application for Compiz Fusion. '
       'It can configurate effects such as "Desktop cube" and "3D windows".\n'
       'Command: sudo apt-get install compizconfig-settings-manager')
    category = 'appearance'
    license = 'GNU General Public License (GPL)'
    logo = 'compizconfig.png'
    size = 4166000 #estimated
    def __init__(self):
        self.pkgs = 'compizconfig-settings-manager'

class CompizSettingManagerSimple(apt_install):
    __doc__ = _('A simple Compiz settings manager')
    detail = _('Command: sudo apt-get install simple-ccsm')
    category = 'appearance'
    logo = 'compizconfig.png'
    license = 'GNU General Public License (GPL)'
    size = 635000 #estimated
    def __init__(self):
        self.pkgs = 'simple-ccsm'

class GoogleChrome:
    __doc__ = _('Google Chrome browser')
    detail = _(
        'This is the web browser from Google. \n'
        'You can change themes by opening web-page https://tools.google.com/chrome/intl/pt/themes/index.html in Google Chrome.')
    license = 'Google Chrome Terms of Service'
    category = 'internet'
    def install(self):
        if get_arch() == 32:
            f = R('http://dl.google.com/dl/linux/direct/google-chrome-beta_current_i386.deb').download()
        else:
            f = R('http://dl.google.com/dl/linux/direct/google-chrome-beta_current_amd64.deb').download()
        gksudo('gdebi-gtk %s' %f)
        APT.cache_changed()
    def installed(self):
        return APT.installed('google-chrome-beta')
    def remove(self):
        return APT.remove('google-chrome-beta')
    def get_reason(self, f):
        if APT.installed('google-chrome-unstable'):
            print >>f, _('"google-chrome-beta" is not installed. '
                         'However, you have installed "google-chrome-unstable".'),

class ScienceBiology(apt_install):
    __doc__= _('Micro-biology software')
    detail = _('This software is for molecular biology, structural biology and bioinformatics.\n' 
               'Command: sudo apt-get install med-bio med-bio-dev')
    category='biology'
    license = 'Eclipse Public License, GNU General Public License (GPL)'
    logo = 'med-bio.png'
    def __init__(self):
        self.pkgs='med-bio med-bio-dev'
    def remove(self):
        apt_install.remove(self)
        run('sudo apt-get autoremove')

class TuxPaint(apt_install):
    __doc__ = _('Tux Paint')
    detail = _('This is a drawing program for young children three years and up.\n' 
                    'Command: sudo apt-get install tuxpaint')
    category = 'education'
    license = 'GNU General Public License (GPL)'
    logo = 'tuxpaint.png'
    def __init__(self):
        self.pkgs='tuxpaint'

class CodeBlocks(apt_install):
    __doc__ = _('Code::Blocks - C/C++ IDE')
    license = 'GNU General Public License (GPL)'
    category = 'dev'
    logo = 'codeblocks.png'
    def __init__(self):
        self.pkgs = 'codeblocks'

class ChildsPlay(apt_install):
    __doc__ = 'ChildsPlay'
    detail = _('This is a suite of educational games for young children.\n'
                    'Command: sudo apt-get install childsplay')
    category = 'education'
    license = 'GNU General Public License (GPL)'
    logo = 'childsplay.png'
    def __init__(self):
        pkgs = APT.get_existing_pkgs_set()
        voices = [ e for e in pkgs if e.startswith('childsplay-alphabet-sounds-') ]
        lang = Config.get_locale().split('_')[0]
        voice = 'childsplay-alphabet-sounds-'+lang
        if not voice in voices: voice = ''
        else: voice = ' ' + voice
        self.pkgs ='childsplay' + voice
        # There is no 'childsplay-plugins-lfc' package in Karmic :)
        # 'childsplay-plugins-lfc' is letterFlashscard game.
        if APT.exist('childsplay-plugins-lfc'):
            self.pkgs += ' childsplay-plugins-lfc'
    def get_reason(self, f):
        self._get_reason(f)
        
class GCompris(apt_install):
    __doc__ = 'GCompris'
    detail = _('GCompris provides educational games for children aged 2 to 10.\n'
                    'Command: sudo apt-get install gcompris')
    category = 'education'
    license = 'GNU General Public License (GPL)'
    logo = 'gcompris.png'
    def __init__(self):
        pkgs = APT.get_existing_pkgs_set()
        voices = [ e for e in pkgs if e.startswith('gcompris-sound-') ]
        lang = Config.get_locale().split('_')[0]
        voice = 'gcompris-sound-'+lang
        if not voice in voices: voice = ''
        else: voice = ' ' + voice
        self.pkgs = 'gnucap gcompris' + voice
    def get_reason(self, f):
        self._get_reason(f)
 
class QT_Creator(apt_install):
    'Qt Creator'
    detail = _('This is an IDE for Qt.\n'
               'Command: sudo apt-get install qtcreator qt-4-dev-tools qt4-doc qt4-qtconfig')
    category = 'dev'
    license = 'GNU General Public License (GPL)'
    logo = 'qtcreator.png'
    def __init__(self):
        self.pkgs = 'qtcreator qt4-dev-tools qt4-doc qt4-qtconfig'

class Kadu(apt_install):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.\n'
               'Command : sudo apt-get install kadu')
    category = 'internet'
    def __init__(self):
        self.pkgs = 'kadu'
    def support(self):
        return Config.is_Poland_locale()

class Qnapi(apt_install):
    __doc__ = 'Qnapi'
    detail = _('QNapi is unofficial free clone of NAPI-PROJEKT program. '
                'Its purpose is to find and download subtitles for given video file. Currently only Polish subtitles are available.\n'
                'Command: sudo apt-get install qnapi')
    license = 'GNU General Public License (GPL)'
    category = 'media'
    def __init__(self):
        self.pkgs = 'qnapi'
    def support(self):
        return Config.is_Poland_locale()

class Parcellite(apt_install):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = 'GNU General Public License'
    logo = 'parcellite.png'
    def __init__(self):
        self.pkgs = 'parcellite'
    def support(self):
        return not ( Config.get_Ubuntu_version() in ['hardy'] )

class R_Language_Basic(apt_install):
    __doc__ = _('R language (basic development environment)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/\n'
               'Command: sudo apt-get install r-base r-base-dev')
    category = 'statistics'
    license = 'GNU General Public License' 
    logo = 'R_language.png'
    def __init__(self):
        self.pkgs = 'r-base r-base-dev'

class R_Language_Full(apt_install):
    __doc__ = _('R language (full development environment and all plugins)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/\n'
               'Command: sudo apt-get install r-base r-base-dev r-cran-*')
    category = 'statistics'
    logo = 'R_language.png'
    license = 'GNU General Public License' 
    def __init__(self):
        import StringIO
        value = StringIO.StringIO()
        print >>value, 'r-base r-base-dev',
        for p in APT.get_existing_pkgs_set():
            if p.startswith('r-cran-'): print >>value, p,
        self.pkgs = value.getvalue()

class Bluefish(apt_install):
    __doc__ = _('Bluefish: Edit HTML web-pages')
    detail = _('Command: sudo apt-get install bluefish')
    license = 'GNU General Public License' 
    category = 'dev'
    logo = 'bluefish.png'
    def __init__(self):
        self.pkgs = 'bluefish'

class Native_64bit_Flash(path_lists):
    __doc__ = _('Adobe native 64bit Flash plugin for Firefox')
    category = 'media'
    logo = 'flash.png'
    license = 'Proprietary freeware,EULA'
    def __init__(self):
        self.paths = [
            '/usr/lib/mozilla/plugins/libflashplayer.so',
            '/usr/lib/firefox-addons/plugins/libflashplayer.so',
            '/usr/lib/xulrunner-addons/plugins/libflashplayer.so',
            ]
    def install(self):
        import os
        file = D+'../support/ubuntu-native-64bit-flash-installer.sh'
        FileServer.chdir('/tmp')
        try:
            run_in_new_terminal(file)
        finally:
            FileServer.chdir_back()
    def support(self):
        return get_arch() == 64

class Wallpaper_Tray(apt_install):
    __doc__ = _('WallpaperTray: Randomly change GNOME desktop background')
    category = 'appearance'
    detail = _('Command: sudo apt-get install wallpaper-tray\n'
               'After installation, please restart your computer. '
               'Then right-click GNOME panel, and select "Add to panel"->"Wallpaper Tray".')
    logo = 'wallpaper-tray.png'
    license = 'GNU General Public License'
    def __init__(self):
        self.pkgs = 'wallpaper-tray'

class _tasksel:
    category = 'server'
    logo = 'tasksel.png'
    def install(self):
        Tasksel.install(self.name)
    def installed(self):
        return Tasksel.installed(self.name)
    def remove(self):
        Tasksel.remove(self.name)
    def support(self):
        return Tasksel.exists(self.name)

class Tasksel_LAMP_server(_tasksel):
    __doc__ = _('LAMP: Install Apache2 + MySQL + PHP')
    detail = _('Command: sudo tasksel install lamp-server')
    def __init__(self):
        self.name = 'lamp-server'

class Tasksel_DNS_server(_tasksel):
    __doc__ = _('DNS server')
    detail = _('Command: sudo tasksel install dns-server')
    def __init__(self):
        self.name = 'dns-server'

class Tasksel_Mail_server(_tasksel):
    __doc__ = _('Mail server')
    detail = _('Command: sudo tasksel install mail-server')
    def __init__(self):
        self.name = 'mail-server'

class Tasksel_Openssh_server(_tasksel):
    __doc__ = _('OpenSSH server')
    detail = _('Command: sudo tasksel install openssh-server')
    def __init__(self):
        self.name = 'openssh-server'

class Tasksel_Postgresql_server(_tasksel):
    __doc__ = _('PostgreSQL server')
    detail = _('Command: sudo tasksel install postgresql-server')
    def __init__(self):
        self.name = 'postgresql-server'

class Tasksel_Print_server(_tasksel):
    __doc__ = _('Printer server')
    detail = _('Command: sudo tasksel install print-server')
    def __init__(self):
        self.name = 'print-server'

class Tasksel_Samba_server(_tasksel):
    __doc__ = _('Samba file sharing server')
    detail = _('Command: sudo tasksel install samba-server')
    def __init__(self):
        self.name = 'samba-server'

class Tasksel_Tomcat_server(_tasksel):
    __doc__ = _('Tomcat Java server')
    detail = _('Command: sudo tasksel install tomcat-server')
    def __init__(self):
        self.name = 'tomcat-server'

class Tasksel_Ubuntustudio_graphics(_tasksel):
    __doc__ = _('Ubuntustudio-graphics: 2D/3D creation and editing')
    detail = _('Command: sudo tasksel install ubuntustudio-graphics')
    def __init__(self):
        self.name = 'ubuntustudio-graphics'

class Tasksel_Ubuntustudio_audio(_tasksel):
    __doc__ = _('Ubuntustudio-audio: Audio creation and editing')
    detail = _('Command: sudo tasksel install ubuntustudio-audio')
    def __init__(self):
        self.name = 'ubuntustudio-audio'

class Tasksel_Ubuntustudio_audio_plugins(_tasksel):
    __doc__ = _('Ubuntustudio-audio-plugins: LADSPA and DSSI audio creation and editing')
    detail = _('Command: sudo tasksel install ubuntustudio-audio-plugins')
    def __init__(self):
        self.name = 'ubuntustudio-audio-plugins'

class Tasksel_Mobile_MID(_tasksel):
    __doc__ = _('Ubuntu MID')
    detail = _('Command: sudo tasksel install mobile-mid')
    def __init__(self):
        self.name = 'mobile-mid'

class Tasksel_Mobile_netbook_remix(_tasksel):
    __doc__ = _('Ubuntu Netbook')
    detail = _('Command: sudo tasksel install mobile-netbook-remix')
    def __init__(self):
        self.name = 'mobile-netbook-remix'

class Tasksel_Ubuntustudio_video(_tasksel):
    __doc__ = _('Ubuntustudio-video: Video creation and editing')
    detail = _('Command: sudo tasksel install ubuntustudio-video')
    def __init__(self):
        self.name = 'ubuntustudio-video'

class Tasksel_Mobile_Live(_tasksel):
    __doc__ = _('Ubuntu MID Live')
    detail = _('Command: sudo tasksel install mobile-live')
    def __init__(self):
        self.name = 'mobile-live'

class Tasksel_Eucalyptus_simple_cluster(_tasksel):
    __doc__ = _('Eucalyptus cloud computing cluster')
    detail = _('Command: sudo tasksel install eucalyptus-simple-cluster')
    def __init__(self):
        self.name = 'eucalyptus-simple-cluster'
        
class Tasksel_Eucalyptus_node(_tasksel):
    __doc__ = _('Eucalyptus cloud computing node')
    detail = _('Command: sudo tasksel install eucalyptus-node')
    def __init__(self):
        self.name = 'eucalyptus-node'

class Tasksel_UEC(_tasksel):
    __doc__ = _('Ubuntu Enterprise Cloud server')
    detail = _('Command: sudo tasksel install uec')
    def __init__(self):
        self.name = 'uec'

class Tasksel_Ubuntustudio_font_meta(_tasksel):
    __doc__ = _('Ubuntustudio-font-meta: A lot of font')
    detail = _('Command: sudo tasksel install ubuntustudio-font-meta')
    def __init__(self):
        self.name = 'ubuntustudio-font-meta'

class Launch_Tasksel:
    __doc__ = _('* Launch tasksel')
    detail = _('This is a helper item. It just launches command: "sudo tasksel". '
               'Then you are free to customize your computer via "tasksel".')
    category = 'server'
    def installed(self):
        return False
    def install(self):
        if not APT.installed('tasksel'): APT.install('tasksel')
        run('sudo tasksel')
        APT.cache_changed()
    def remove(self):
        raise NotImplementedError

class Fctix:
    'Fcitx'
    detail = _('This is a popular Chinese input method.\n'
               'It is from http://fcitx.googlecode.com/')
    Chinese = True
    license = 'GNU General Public License (GPL)'
    def install(self):
        if get_arch() == 32:
            f = R(['http://fcitx.googlecode.com/files/fcitx-svn_3.6.3-20100305-r309_i386.deb'],
                7377508,'bb5deee1dc997ce72c8be22b4d90c6fef1210b46').download()
        else:
            f=R(['http://fcitx.googlecode.com/files/fcitx-svn_3.6.3-20100305-r309_amd64.deb'],
                7408298,'00e9508a6602f71495e21222c204d14289ff0f13').download()
        run('gdebi-gtk ' + f)
    def installed(self):
        return APT.installed('fcitx-svn')
    def remove(self):
        APT.remove('fcitx-svn')
        
class XBMC(apt_install):
    'XBMC'
    category = 'media'
    license = 'GNU General Public License (GPL)'
    def install(self):
        from third_party_repos import Repo_XBMC
        xbmc_obj=Repo_XBMC()
        if not xbmc_obj.installed():
            xbmc_obj.install()
        apt_install.install(self)
    def __init__(self):
        self.pkgs = 'xbmc'

class Songbird(apt_install):
    'Songbird'
    category = 'media'
    license = 'GNU General Public License (GPL)'
    def install(self):
        from third_party_repos import Repo_Songbird
        song_obj = Repo_Songbird()
        if not song_obj.installed():
            song_obj.install()
        apt_install.install(self)
    def __init__(self):
        self.pkgs = 'songbird'
        
class DropBox(apt_install):
    'Dropbox'
    category = 'internet'
    license = 'free for Linux'
    def install(self):
        from third_party_repos import Repo_Dropbox
        drop_obj = Repo_Dropbox()
        if not drop_obj.installed():
            drop_obj.install()
        apt_install.install(self)
    def __init__(self):
        self.pkgs = 'nautilus-dropbox'

class Skype(apt_install):
    'Skype'
    category = 'internet'
    license = 'proprietary'
    def install(self):
        from third_party_repos import Repo_Skype
        sky_obj = Repo_Skype()
        if not sky_obj.installed():
            sky_obj.install()
        apt_install.install(self)
    def __init__(self):
        self.pkgs = 'skype'
    def support(self):
        return get_arch() == 32

class Vuze_Karmic(apt_install):
    # Latest Vuze is in 9.10 repository.
    'Vuze'
    category = 'internet'
    logo = 'vuze.png'
    license = 'GNU General Public License (GPL)'
    detail = _('Download via bittorrent + Search videos + Play videos\n'
               'Command: sudo apt-get install vuze')
    def __init__(self):
        self.pkgs = 'vuze'
    def support(self):
        return Config.get_Ubuntu_version() not in ['hardy', 'intrepid', 'jaunty']
