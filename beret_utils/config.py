import os

from abc import abstractmethod
from typing import Optional, Iterable, Type, AnyStr

from .mapping import MappingConst


class Value(object):

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
            if callable(value):
                value = value(values, *envs)
            values[key] = value
        return values

    def update(self, init):
        return super().update(self.get_values(init))


class ConfigEnvFiles(ConfigEnv):
    ENV_FILES = []

    def get_env_files(self) -> dict:
        env = {}
        for env_file_path in self.ENV_FILES:
            try:
                with open(env_file_path, 'r') as env_file:
                    for line in env_file.readlines():
                        line = line.strip()
                        if '#' in line:
                            line = line.split('#')[0].strip()
                        if '=' in line:
                            try:
                                key, value = line.split('=')
                                env[key.strip()] = value.strip()
                            except ValueError:
                                pass
            except FileNotFoundError:
                pass
        return env

    def get_envs(self, envs: Optional[Iterable[dict]] = None) -> list:
        envs = super().get_envs(envs)
        envs.append(self.get_env_files())
        return envs


def get_config(
        defaults: Iterable[tuple],
        env_files: Optional[Iterable[AnyStr]] = None,
        config_class: Optional[Type[Config]] = ConfigEnvFiles
) -> Type[Config]:

    class ConfigClass(config_class):
        DEFAULTS = expand_defaults(defaults)
        ENV_FILES = env_files or []

    return ConfigClass
