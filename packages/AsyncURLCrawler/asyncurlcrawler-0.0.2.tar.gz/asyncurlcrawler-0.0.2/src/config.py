import yaml
from dataclasses import dataclass


@dataclass
class ParserConfig:
    delay_start: float
    max_retries: int
    request_timeout: float
    user_agent: str


@dataclass
class Config:
    parser: ParserConfig


def read_config() -> dict:
    file_path = 'config.yaml'
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_config() -> Config:
    json_config = read_config()
    parser_config = ParserConfig(**json_config['PARSER'])
    config = Config(parser=parser_config)
    return config
