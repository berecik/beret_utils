import math

from beret_utils.config import get_config, EnvValue
from beret_utils.path import path_fun

go_here = path_fun(depth=0)
go_one_up = path_fun(depth=1)
go_two_up = path_fun(depth=2)

DEFAULTS = (
    ('POSTGRES_DB', 'test_db'),
    ('POSTGRES_USER', 'password'),
    ('POSTGRES_PASSWORD', 'postgres'),
    ('POSTGRES_HOST', 'localhost'),
    ('POSTGRES_PORT', 5432, int),
    ('POSTGRES_RETRIES', 120, lambda x: int(x)*math.pi),
    ('POSTGRES_WAIT', EnvValue('POSTGRES_PORT'), int),
    ('POSTGRES_SLEEP', EnvValue('POSTGRES_RETRIES'), lambda x: math.sin(float(x))),
    ('POSTGRES_WAKEUP', EnvValue('POSTGRES_RETRIES'), lambda x: math.sin(float(x))),
    ('SOME_PATH', 'beret_utils', go_here, 'ENV_PATH'),
    ('SOME_PATH_UP', EnvValue('SOME_PATH'), go_one_up, 'ENV_PATH'),
    ('SOME_PATH_DOUBLE_UP', EnvValue('SOME_PATH'), go_two_up, 'ENV_PATH')
)
ENV_FILES = (
    go_here('example_env.sh'),
)

ConfigClass = get_config(DEFAULTS, ENV_FILES)
config = ConfigClass()

if __name__ == '__main__':
    for name, value in config.items():
        print(f"{name}={value}")
