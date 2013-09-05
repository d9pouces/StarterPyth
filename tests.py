#coding=utf-8
"""
Test starterpyth against different Python versions
"""
import logging
import os
import shutil
import subprocess
import sys
from starterpyth.utils import py3k_unicode, py3k_bytes
from starterpyth.log import CONSOLE, dict_config

__author__ = 'd9pouces'

os.environ['DJANGO_SETTINGS_MODULE'] = "test.djangoproject.settings"

TEST_DIRECTORY = 'Test'

STDIN_PREFIXES = ['''{0}
test
{1}9pouces.net
{1}9pouces
d9pouces@19pouces.net
cecill b'''.format(TEST_DIRECTORY, '∂' if sys.version_info[0] == 3 else '\xe2\x88\x82')]

PY_VERSIONS = {
    '''3.4''': ('3.4', ),
    '''3.3''': ('3.3', '3.4', ),
    '''3.2''': ('3.2', '3.3', '3.4', ),
    '''3.1''': ('3.1', '3.2', '3.3', '3.4', ),
    '''3.0''': ('3.0', '3.1', '3.2', '3.3', '3.4', ),
    '''2.7
yes''': ('2.7', '3.1', '3.2', '3.3', '3.4', ),
    '''2.7
no
yes''': ('2.7', ),
    '''2.6
yes''': ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4', ),
    '''2.6
no
yes''': ('2.6', '2.7', ),
}

PLUGIN_VERSIONS = [
    #     '''yes
    # yes
    # yes
    # yes
    # yes''',
    #     '''yes
    # yes
    # no
    # yes
    # yes''',
    #     '''yes
    # no
    # yes
    # yes''',
    '''no
yes
no''',
]

AVAILABLE_PYTHONS = []
for min_version in ('2.6', '2.7', '3.0', '3.1', '3.2', '3.3', '3.4'):
    popen = subprocess.Popen('which python' + min_version, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate()
    if stdout:
        AVAILABLE_PYTHONS.append(min_version)

if __name__ == '__main__':
    log_config = CONSOLE
    dict_config(log_config)

    for prefix in STDIN_PREFIXES:
        for min_version in PY_VERSIONS:
            for plugins in PLUGIN_VERSIONS:
                for trans in ('yes', 'no'):
                    data = prefix + "\n" + min_version + "\n" + trans + "\n0.1\n" + plugins + "\n"
                    print(data)
                    for run_version in AVAILABLE_PYTHONS:
                        print('Running StarterPyth with ' + run_version)
                        if os.path.isdir(TEST_DIRECTORY):
                            shutil.rmtree(TEST_DIRECTORY)
                        cmd = "python{0} -c 'from starterpyth.core import main; main()'".format(run_version)
                        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 stdin=subprocess.PIPE)
                        stdout, stderr = popen.communicate(py3k_bytes(data))
                        if popen.returncode:
                            logging.error(cmd)
                            print(stdout)
                            print(stderr)
                            sys.exit(1)
#                            continue
                        for test_version in PY_VERSIONS[min_version]:
                            if test_version not in AVAILABLE_PYTHONS:
                                continue
                            print('Testing generated code with ' + test_version)
                            for dist_cmd in ('build', 'build_ext', 'doctest', 'test'):
                                cmd = "python{0} setup.py {1}".format(test_version, dist_cmd)
                                popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                         stderr=subprocess.PIPE,
                                                         cwd=TEST_DIRECTORY)
                                stdout, stderr = popen.communicate()
                                if popen.returncode:
                                    logging.error(cmd)
                                    print(stdout)
                                    print(stderr)
                                    sys.exit(1)
 #                                   continue
