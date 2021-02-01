from beret_utils.config import get_config, EnvValue
from beret_utils.path import path_fun

go_here = path_fun()

DEFAULTS = (
    ('POSTGRES_DB', 'test_db'),
    ('POSTGRES_USER', 'password'),
    ('POSTGRES_PASSWORD', 'postgres'),
    ('POSTGRES_HOST', 'localhost'),
    ('POSTGRES_PORT', 5432),
    ('POSTGRES_RETRIES', 120),
    ('POSTGRES_WAIT', 5),
    ('SOME_PATH', 'beret_utils', go_here, 'ENV_PATH')
)
ENV_FILES = (
    go_here('example_env.sh'),
)

Config = get_config(DEFAULTS, ENV_FILES)
config = Config()

if __name__ == '__main__':
    for name, value in config.items():
        print(f"{name}={value}, {config[name]}")
