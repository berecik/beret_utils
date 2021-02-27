import os
from unittest import TestCase
from beret_utils import get_config, EnvValue, join_path_value
from beret_utils import get_path_fun

get_path = get_path_fun()

DEFAULT_CONFIG = (
    ('ONE', 1, int),
    ('TWO', 2, int),
    ('THREE', 3, int),
    ('TWO_AGAIN', EnvValue('TWO')),
    ('DIR', 'test', get_path),
    ('DIR_BIS', 'test', get_path),
    ('SUBDIR', 'dir', join_path_value('DIR')),
    ('FILE', 'file', join_path_value('SUBDIR')),
)

ENV_FILES = (
    os.path.join('test_dir', 'test.env'),
    os.path.join('test_dir', 'test_bis.env'),
)


Config = get_config(DEFAULT_CONFIG, ENV_FILES)
config = Config()


class TestConfig(TestCase):

    def test_config_key(self):
        self.assertEqual(1, config['ONE'])
        self.assertEqual(22, config['TWO'])
        self.assertEqual(333, config['THREE'])

    def test_config_val(self):
        self.assertEqual(1, config.ONE)
        self.assertEqual(22, config.TWO)
        self.assertEqual(333, config.THREE)

    def test_env_value(self):
        self.assertEqual(22, config.TWO_AGAIN)

    def test_dir(self):
        self.assertEqual(get_path('test_dir'), config.DIR)
        self.assertEqual(get_path('test'), config.DIR_BIS)

    def test_subdir(self):
        self.assertEqual(get_path('test_dir', 'subdir'), config.SUBDIR)

    def test_subdir_file(self):
        self.assertEqual(get_path('test_dir', 'subdir', 'test.txt'), config.FILE)
