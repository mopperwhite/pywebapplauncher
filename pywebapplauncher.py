#!/usr/bin/env python
#encoding=UTF-8
#  
#  Copyright 2014 MopperWhite <mopperwhite@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
import sys,optparse,locale,json,os,webbrowser


class CookieJar(QNetworkCookieJar):
        def __init__(self,url,filename,parent=None):
                super(QNetworkCookieJar,self).__init__(parent)
                self._filename=filename
                self._url=url
                if os.path.exists(filename):self.load()
        def load(self):
                self.setCookiesFromUrl( [ QNetworkCookie.parseCookies(QByteArray(cs))[0]  for cs in json.load(open(self._filename)) ]  ,QUrl(self._url))
        def save(self):
                l=[unicode(QString(c.toRawForm())) for c in self.allCookies()]
                json.dump(l,open(self._filename,'w'))
 
def linkClicked(q_url):
        url=unicode(q_url.toString())
        print url
        webbrowser.open_new_tab(url)
        
def main():
        p = optparse.OptionParser()
        p.add_option('--url', '-u',help="The url of the webapp.")
        p.add_option('--name', '-n',default="PyWebAppLauncher",help="The name of the webapp.")
        p.add_option('--cookiesfile', '-c',default="pwalcookies.json",help="The cookies file of webkit(json).")
        p.add_option('--maxsize', '-m',default="false",help="A bool value to make the window show max size or not.(true/[false])")
        options, arguments = p.parse_args()
        
        cookiesfilename=options.cookiesfile       
        url=options.url
        maxsize=json.loads(options.maxsize)
        if not url:
                if arguments:url=arguments[0]
                else:
                        print u'Please input url.'
                        sys.exit()
        name=options.name.decode(locale.getdefaultlocale()[1])
        app=QApplication(sys.argv)
        cookiejar=CookieJar(url,cookiesfilename)
        window=QWebView()
        if maxsize:
                window.showMaximized()
        window.page().networkAccessManager().setCookieJar(cookiejar);
        window.setWindowTitle(name)
        QObject.connect(window,SIGNAL("linkClicked(const QUrl&)"),linkClicked)
        window.setUrl(QUrl(url))
        window.show()
        app.exec_()
        cookiejar.save()
        
if __name__=='__main__':
        main()
