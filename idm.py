# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Install Drupal Module (idm)
# Author : Jonas Björk, jonas@jonasbjork.net
# Date   : 2009-10-22
# License: EUPL v1.1 (http://ec.europa.eu/idabc/eupl) #
# Modified by Marcus Follrud 2009-10-23:
# Added Filtering options for different drupal versions plus developer packages
# Also added a better help :) 
import sys,re,string
from optparse import OptionParser #For parsing command line arguments.

from ftplib import FTP

optParser = OptionParser()
optParser.set_defaults(drupalfilter="all")
optParser.add_option("-f","--filter", action="store", type="string", dest="drupalfilter",
					help="Filter the results in version numbers.", metavar="version")

optParser.add_option("-d", "--dev", action="store_true", dest="devpackages", help="Show developer packages", default=False)

(options, args) = optParser.parse_args()

#drupal filter is in options.drupalfilter

if len(sys.argv) == 1:
    print 'Syntax: ' + sys.argv[0] + ' modulename'
    sys.exit(1)

module = args[0]
server = 'ftp.drupal.org'
path = '/pub/drupal/files/projects/'

try: ftp = FTP( server )
except:
  print 'Error: Host '+server+' could not be resolved.'
  sys.exit()
else: pass
try: ftp.login()
except:
  print 'Error: Could not log in.'
  sys.exit()
else: pass

ftp.cwd( path )
fdir = ftp.nlst()
print 'Found a total of ' + str(len(fdir)) + ' files!'

#l = []
#for f in fdir:
#  p = re.compile('.*'+module+'*')
#  if p.match(f):
#    l.append(f)
#print l

l = [f for f in fdir if module in f]
l2 = [] #This is the filtered list.
for i in range(0, len(l)):
  #This is where we write out the files found.
  #Also. This is where we do the filtering. 6.x, 5.x, 4.x and dev (for now..)
  if options.drupalfilter == "all":
    l2.append(l[i])
  else:
  #Parse after the version entered.
    if string.find(l[i],options.drupalfilter+".x",0,len(l[i])) > 0:
    #We got a match for the filter.
      if options.devpackages == True:
        if string.find(l[i],"-dev",0,len(l[i])) > 0:
          l2.append(l[i])
      else:
         if string.find(l[i],"-dev",0,len(l[i])) < 0:
           l2.append(l[i])

if (len(l2) > 0): #We got a result
  print "Files containing \""+module+"\""
  print " Based on filter: "+options.drupalfilter
  if options.devpackages == True:
    print "  Showing developer packages"
  else:
    print "  Not showing developer packages"
  for i in range(0,len(l2)):
    print '[' + str(i) + '] '+ l2[i]
else:
  print 'Error: Could not find a module by that name.'
  sys.exit(0)

getid = int(raw_input("Which module do you want to download? ")) 
print 'Ok, lets get ' + l[getid]
lf = open(l[getid],'wb') 
ftp.retrbinary('RETR ' + l[getid],lf.write)
lf.close()

ftp.close()
