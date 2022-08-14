from unittest import TestCase
from beret_utils import get_config, EnvValue, join_path_value
from beret_utils import get_dir

get_path = get_dir(depth=1)


class ConfigTestCase(TestCase):

    def setUp(self):
        DEFAULT_CONFIG = (
            ('ONE', 1, int),
            ('TWO', 2, int),
            ('THREE', 3, int),
            ('TWO_AGAIN', EnvValue('TWO'), int),
            ('VALUE', 'default_value'),
            ('DIR', 'test', get_path),
            ('DIR_BIS', 'test', get_path),
            ('SUBDIR', 'parent', join_path_value('DIR')),
            ('SUBDIR_ENV_VALUE', EnvValue('VALUE'), join_path_value('SUBDIR')),
            ('FILE', 'file', join_path_value('SUBDIR')),
        )

        ENV_FILES = (
            'test.env',
            'test_bis.env',
        )

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
