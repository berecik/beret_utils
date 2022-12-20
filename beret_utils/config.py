import os
import sys
import re

try:
    from os import PathLike
except ImportError:  # Python 3.5 support
    from pathlib import PurePath as PathLike

Openable = (str, PathLike)

from abc import abstractmethod
from typing import Optional, Iterable, Type, AnyStr
from logging import getLogger

from .mapping import MappingConst

logger = getLogger(__name__)


class Value:

    def __call__(self, *envs: dict) -> Optional[AnyStr]:
        for env in envs:
            result = self.get_value(env)
            if result is not None:
                return result
        return None

    @abstractmethod
    def get_value(self, config: object) -> AnyStr:
        pass


class EnvValue(Value):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def get_value(self, env):
        return env.get(self.var_name)


def join_path(*args):
    return os.path.join(*args)


def join_path_value(dir_id):
    """
    produce a special parser with join another variable value to given path
    """

    class JoinPathValue(EnvValue):
        def get_value(self, env):
            if dir_id in env:
                value = join_path(env[dir_id], self.var_name)
                return value

    return JoinPathValue


def format_string(string):

    class FormatString(Value):
        def get_value(self, env):
            return string.format(**env)

    return FormatString()


def bool_value(value):
    try:
        i = float(value)
        return bool(i)
    except ValueError:
        pass

    s = str(value).lower()
    if "true" in s:
        return True
    if "false" in s:
        return False
    return None


def expand_defaults(init):
    return (
        map(
            lambda args:
            (lambda key, value=None, parser=str, env_key=None, parse_default=True:
             (
                 key,
                 value,
                 parser,
                 key if env_key is None else env_key,
                 parse_default
             )
             )(*args),
            init
        )
    )


class Config(MappingConst):

    @abstractmethod
    def get_values(self) -> dict:
        return {}

    def __init__(self):
        super().__init__()
        self.__dict__ = self.get_values()


def init_envs(envs: Optional[Iterable]) -> list:
    return list(envs) if envs is not None else []


class ConfigEnv(Config):
    DEFAULTS = []

    def get_envs(self, envs: Optional[Iterable[dict]] = None) -> list:
        envs = init_envs(envs)
        envs.append(os.environ)
        return envs

    def get_values(self, init=None):
        if init is not None:
            defaults = expand_defaults(init)
        else:
            defaults = self.DEFAULTS
        values = {}
        envs = self.get_envs()
        for key, value, parser, env_key, parse_default in defaults:
            env_val = EnvValue(env_key)(*envs)

            if env_val is not None:
                value = parser(env_val)
            elif parse_default and not callable(value):
                value = parser(value)

            while callable(value):
                value = value(values, *envs)
                if parser:
                    value = parser(value)
                    parser = False

            values[key] = value
        return values

    def update(self, init):
        return super().update(self.get_values(init))


class ConfigEnvFiles(ConfigEnv):
    ENV_FILES = []

    def get_env_files(self) -> dict:
        env = {}
        for env_file_path in self.ENV_FILES:
            env = read_dot_env(env_file_path, **env) or env
        return env

    def get_envs(self, envs: Optional[Iterable[dict]] = None) -> list:
        envs = super().get_envs(envs)
        envs.append(self.get_env_files())
        return envs


def read_dot_env(env_file=None, **env):
    """
    From: https://github.com/joke2k/django-environ

    Read a .env file into os.environ.

    If not given a path to a dotenv path, does filthy magic stack
    backtracking to find the dotenv in the same directory as the file that
    called read_env.

    Existing environment variables take precedent and are NOT overwritten
    by the file content. ``overwrite=True`` will force an overwrite of
    existing environment variables.

    Refs:
    - https://wellfire.co/learn/easier-12-factor-django
    - https://gist.github.com/bennylope/2999704

    :param env_file: The path to the `.env` file your application should
        use. If a path is not provided, `read_env` will attempt to import
        the Django settings module from the Django project root.
    :param **env: Any additional keyword arguments provided directly
        to read_env will be added to the environment. If the key matches an
        existing environment variable, the value will be overridden.
    """
    if env_file is None:
        frame = sys._getframe()
        env_file = os.path.join(
            os.path.dirname(frame.f_back.f_code.co_filename),
            '.env'
        )
        if not os.path.exists(env_file):
            logger.info(
                "%s doesn't exist - if you're not configuring your "
                "environment separately, create one." % env_file)
            return

    try:
        if isinstance(env_file, Openable):
            # Python 3.5 support (wrap path with str).
            with open(str(env_file)) as f:
                content = f.read()
        else:
            with env_file as f:
                content = f.read()
    except OSError:
        logger.info(
            "%s not found - if you're not configuring your "
            "environment separately, check this." % env_file)
        return

    logger.debug('Read environment variables from: {}'.format(env_file))

    def _keep_escaped_format_characters(match):
        """Keep escaped newline/tabs in quoted strings"""
        escaped_char = match.group(1)
        if escaped_char in 'rnt':
            return '\\' + escaped_char
        return escaped_char

    for line in content.splitlines():
        m1 = re.match(r'\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', _keep_escaped_format_characters,
                             m3.group(1))
            env[key] = str(val)
        elif not line or line.startswith('#'):
            # ignore warnings for empty line-breaks or comments
            pass
        else:
            logger.warning('Invalid line: %s', line)

    return env


def get_config(
        defaults: Iterable[tuple],
        env_files: Optional[Iterable[AnyStr]] = None,
        config_class: Optional[Type[Config]] = ConfigEnvFiles
) -> Type[Config]:

    class ConfigClass(config_class):
        DEFAULTS = expand_defaults(defaults)
        ENV_FILES = env_files or []

    return ConfigClass
