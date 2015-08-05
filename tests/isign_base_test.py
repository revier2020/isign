from os.path import abspath, dirname, exists, join, isdir
from isign import isign
import logging
from monitor_temp_file import MonitorTempFile
import os
import shutil
import tempfile
import unittest

log = logging.getLogger(__name__)


class IsignBaseTest(unittest.TestCase):
    TEST_DIR = dirname(__file__)
    TEST_APP = join(TEST_DIR, 'SimpleSaucyApp.app')
    TEST_APPZIP = TEST_APP + '.zip'
    TEST_IPA = join(TEST_DIR, 'SimpleSaucyApp.ipa')
    TEST_NONAPP_TXT = join(TEST_DIR, 'NotAnApp.txt')
    TEST_NONAPP_IPA = join(TEST_DIR, 'NotAnApp.ipa')
    TEST_SIMULATOR_APP = join(TEST_DIR, 'IosSimulatorApp.app.zip')
    REPO_ROOT = dirname(dirname(abspath(__file__)))
    KEY = join(TEST_DIR, 'credentials', 'test.key.pem')
    CERTIFICATE = join(TEST_DIR, 'credentials', 'test.cert.pem')
    PROVISIONING_PROFILE = join(TEST_DIR, 'credentials', 'test.mobileprovision')
    ERROR_KEY = '_errors'
    # Sauce Labs apple organizational unit
    OU = 'JWKXD469L2'

    def setUp(self):
        """ this helps us monitor if we're not cleaning up temp files """
        MonitorTempFile.start()

    def tearDown(self):
        """ remove monitor on tempfile creation """
        remaining_temp_files = MonitorTempFile.get_temp_files()
        if len(remaining_temp_files) != 0:
            log.error("remaining temp files: %s",
                      ', '.join(remaining_temp_files))
        assert len(remaining_temp_files) == 0
        MonitorTempFile.stop()

    def resign(self, filename, **args):
        """ resign with test credentials """
        args.update({
            "key": self.KEY,
            "certificate": self.CERTIFICATE,
            "provisioning_profile": self.PROVISIONING_PROFILE
        })
        return isign.resign(filename, **args)

    def unlink(self, path):
        if exists(path):
            if isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    def get_temp_file(self, prefix='isign-test-'):
        """ just getting a file path that probably isn't in use """
        (fd, path) = tempfile.mkstemp(prefix=prefix)
        os.close(fd)
        os.unlink(path)
        return path
