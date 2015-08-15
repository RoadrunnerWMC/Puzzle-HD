from distutils.core import setup
from py2exe.build_exe import py2exe
import os, os.path, shutil, sys

upxFlag = False
if '-upx' in sys.argv:
    sys.argv.remove('-upx')
    upxFlag = True

dir = 'distrib/windows'

print '[[ Running Puzzle Through py2exe! ]]'
print 'Note: Puzzle MUST have NSMBlib-0.5a or none at all to function.'
print '>> Destination directory: %s' % dir
sys.argv.append('py2exe')

if os.path.isdir(dir): shutil.rmtree(dir)
os.makedirs(dir)

# exclude QtWebKit to save space, plus Python stuff we don't use
excludes = ['encodings', 'doctest', 'pdb', 'unittest', 'difflib', 'inspect',
    'os2emxpath', 'posixpath', 'optpath', 'locale', 'calendar',
    'threading', 'select', 'socket', 'hashlib', 'multiprocessing', 'ssl',
    'PyQt4.QtWebKit', 'PyQt4.QtNetwork']

# set it up
setup(
    name='Puzzle',
    version='1.0',
    description='Puzzle - Tileset Editor',
    windows=[
        {'script': 'puzzle.py',
         }
    ],
    options={'py2exe':{
        'includes': ['sip', 'encodings', 'encodings.hex_codec', 'encodings.utf_8'],
        'compressed': 1,
        'optimize': 2,
        'excludes': excludes,
        'bundle_files': 3,
        'dist_dir': dir
    }}
)

print '>> Built frozen executable!'

# now that it's built, configure everything
os.unlink(dir + '/w9xpopen.exe') # not needed

if upxFlag:
    if os.path.isfile('upx.exe'):
        print '>> Found UPX, using it to compress the executables!'
        files = os.listdir(dir)
        upx = []
        for f in files:
            if f.endswith('.exe') or f.endswith('.dll') or f.endswith('.pyd'):
                upx.append('"%s/%s"' % (dir,f))
        os.system('upx -9 ' + ' '.join(upx))
        print '>> Compression complete.'
    else:
        print '>> UPX not found, binaries can\'t be compressed.'
        print '>> In order to build Reggie! with UPX, place the upx.exe file into '\
              'this folder.'

if os.path.isdir(dir + '/Icons'): shutil.rmtree(dir + '/Icons') 
if os.path.isdir(dir + '/nsmblib-0.5a'): shutil.rmtree(dir + '/nsmblib-0.5a') 
shutil.copytree('Icons', dir + '/Icons') 
shutil.copytree('nsmblib-0.5a', dir + '/nsmblib-0.5a') 
shutil.copy('license.txt', dir)

print '>> Attempting to copy VC++2008 libraries...'
if os.path.isdir('Microsoft.VC90.CRT'):
    shutil.copytree('Microsoft.VC90.CRT', dir + '/Microsoft.VC90.CRT')
    print '>> Copied libraries!'
else:
    print '>> Libraries not found! The frozen executable will require the '\
          'Visual C++ 2008 runtimes to be installed in order to work.'
    print '>> In order to automatically include the runtimes, place the '\
          'Microsoft.VC90.CRT folder into this folder.'

print '>> Reggie has been frozen to %s!' % dir
