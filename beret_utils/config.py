import os
from abc import abstractmethod
from typing import Optional, Iterable, Type, AnyStr

from .mapping import MappingConst
from .singleton import Singleton


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

    def get_values(self):
        values = {}
        envs = self.get_envs()
        for key, value, parser, env_key in self.DEFAULTS:
            env_val = EnvValue(env_key)(*envs)
            if env_val is not None:
                value = parser(env_val)
            if callable(value):
                value = value(values, *envs)
            values[key] = value
        return values


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


def get_config_class(
        defaults: Iterable[Type[tuple]],
        env_files: Iterable[AnyStr],
        config_class: Optional[Type[Config]] = ConfigEnvFiles
) -> Type[Config]:

    class ConfigClass(config_class):
        DEFAULTS = tuple(
            map(
                lambda args:
                (lambda key, value=None, parser=str, env_key=None:
                 (
                     key,
                     value,
                     parser,
                     key if env_key is None else env_key
                 )
                 )(*args),
                defaults
            )
        )
        ENV_FILES = env_files

    return ConfigClass


def get_config(
        defaults: Iterable[Type[tuple]],
        env_files: Iterable[AnyStr],
        config_class: Optional[Type[Config]] = None
) -> Type[Singleton, Config]:

    args = [defaults, env_files]
    if config_class is not None:
        args.append(config_class)
    return Singleton(get_config_class(*args))
