from unittest import TestCase
from beret_utils import get_config, EnvValue, join_path_value, format_string
from beret_utils import get_dir

from example.config import config, DEFAULT_CONFIG
from example.config import get_path as example_path

get_path = get_dir(depth=1)

ENV_FILES = (
    'test.env',
    'test_bis.env',
)


class ConfigTestCase(TestCase):

    def setUp(self):
        Config = get_config(DEFAULT_CONFIG, ENV_FILES)
        self.config = Config()


class TestConfig(ConfigTestCase):

    def test_config_key(self):
        self.assertEqual(1, self.config['ONE'])
        self.assertEqual(22, self.config['TWO'])
        self.assertEqual(333, self.config['THREE'])

    def test_config_val(self):
        self.assertEqual(1, self.config.ONE)
        self.assertEqual(22, self.config.TWO)
        self.assertEqual(333, self.config.THREE)

    def test_env_value(self):
        self.assertEqual(22, self.config.TWO_AGAIN)

    def test_dir(self):
        self.assertEqual(get_path('test_dir'), self.config.DIR)
        self.assertEqual(get_path('test'), self.config.DIR_BIS)

    def test_subdir(self):
        self.assertEqual(get_path('test_dir', 'subdir'), self.config.SUBDIR)

    def test_subdir_file(self):
        self.assertEqual(get_path('test_dir', 'subdir', 'test.txt'), self.config.FILE)

    def test_subdir_env_value(self):
        self.assertEqual(get_path('test_dir', 'subdir', 'env_value_bis'), self.config.SUBDIR_ENV_VALUE)

    def test_sformat_sting(self):
        self.assertEqual(f"{self.config.ONE} {self.config.TWO} {self.config.THREE} {self.config.TWO_AGAIN} {self.config.DIR} {self.config.SUBDIR_ENV_VALUE}", self.config.FORMAT_STRING)


class ConfigTestNoEnvFiles(TestCase):

    def test_set_up_config(self):

        NON_EXISTING_FILES = (
            'non_exist_test.env',
            'non_exist_test_bis.env',
        )

        TestConfig = get_config(DEFAULT_CONFIG, NON_EXISTING_FILES)
        self.config = TestConfig()

        self.assertEqual(1, self.config['ONE'])
        self.assertEqual(2, self.config['TWO'])
        self.assertEqual(3, self.config['THREE'])
        self.assertEqual(2, self.config['TWO_AGAIN'])
