'''
Simple install script that installs cit and its dependencies without touching the local python 
installation.

Usage::
    curl -s https://raw.github.com/nicoddemus/cit/master/cit_install.py > cit_install.py
    python cit_install.py
'''
import subprocess
import os
import sys
import shutil
import urllib2

# can only start installation if in an empty directory or if directory contains this file
contents = os.listdir('.') 
if contents and contents != [os.path.basename(__file__)]:
    sys.exit('cit must be installed in an empty directory.')

#===================================================================================================
# Download
#===================================================================================================
os.mkdir('repos')
os.chdir('repos')

print '--> pyyaml'    
subprocess.check_call('git clone http://github.com/yaml/pyyaml.git', shell=True)
print '--> JenkinsAPI'    
subprocess.check_call('git clone http://github.com/salimfadhley/jenkinsapi', shell=True)
print '--> cit'    
subprocess.check_call('git clone http://github.com/nicoddemus/cit.git', shell=True)

os.chdir('..')
shutil.copy('repos/cit/cit.py', 'cit.py')
shutil.copytree('repos/jenkinsapi/jenkinsapi', 'jenkinsapi')
shutil.copytree('repos/pyyaml/lib/yaml', 'yaml')
print 'Download done.'

import yaml
from jenkinsapi.jenkins import Jenkins
import jenkinsapi.utils.retry # initializing logging, so it will shut up later and don't mess our output

#===================================================================================================
# Configure
#===================================================================================================
print '=' * 60
print 'Configuring:'
print '=' * 60
jenkins_url = raw_input('Jenkins URL (make sure to include http:// or https://): ')
config = {
    'jenkins' : {
        'url' : jenkins_url,
    }
}

filename = os.path.abspath('citconfig.yaml')
f = file(filename, 'w')
f.write(yaml.dump(config, default_flow_style=False))
f.close()

print 'Written configuration to: %s' % filename
print

#===================================================================================================
# Check Jenkins
#===================================================================================================
print 'Checking if Jenkins server is correct...',
try:
    jenkins = Jenkins(jenkins_url)
except urllib2.URLError, e:
    print 'Could not connect:'
    print ' --> %s' % e
    print 'Update configuration file manually.'
else:
    print 'OK'
