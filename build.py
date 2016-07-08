import os
import os.path
import shutil
import sysconfig

import main


platform = sysconfig.get_platform()
exe_name = 'build/MeterReader_%s_v%s' % (platform, main.version)
exe_dir = 'build/exe.%s-%s' % (platform, sysconfig.get_python_version())

if os.path.exists(exe_dir):
    shutil.rmtree(exe_dir)
if os.path.exists(exe_name):
    shutil.rmtree(exe_name)
if os.path.exists(exe_name + '.exe'):
    os.remove(exe_name + '.exe')

os.system('python.exe setup.py build')

##shutil.rmtree(exe_dir + '/tk/demos')
##shutil.rmtree(exe_dir + '/tk/images')

os.rename(exe_dir, exe_name)

#os.system('"C:/Program Files/7-Zip/7z.exe"'\
#          ' a -sfx7z.sfx {0}.exe ./{0} -mx9'.format(exe_name))

input("按任意键退出.")
