from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final

import rtoml

BASE_DIR_PATH: Final[Path] = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH: Final[Path] = BASE_DIR_PATH / "config"


class ValidEnvs(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


ENV_CONFIG_PATHS: Final[MappingProxyType[ValidEnvs, Path]] = MappingProxyType(
    {
        ValidEnvs.DEVELOPMENT: CONFIG_PATH / "development.toml",
        ValidEnvs.PRODUCTION: CONFIG_PATH / "production.toml",
    }
)


@dataclass
class PostgresConfig:
    user: str
    password: str
    db: str
    port: int

    def __post_init__(self):
        if not isinstance(self.user, str):
            raise TypeError("USER must be a string")
        if not isinstance(self.password, str):
            raise TypeError("PASSWORD must be a string")
        if not isinstance(self.db, str):
            raise TypeError("DB must be a string")
        if not isinstance(self.port, int):
            raise TypeError("PORT must be an integer")


def validate_env(*, env: str) -> ValidEnvs:
    if env not in ValidEnvs:
        valid_values = ", ".join(e.value for e in ValidEnvs)
        raise ValueError(
            f"Invalid environment '{env}'. Must be one of: {valid_values}."
        )
    return ValidEnvs(env)


def read_config(*, env: ValidEnvs) -> dict[str, Any]:
    path = ENV_CONFIG_PATHS.get(env)
    if path is None or not path.is_file():
        raise FileNotFoundError(
            f"The file does not exist at the specified path: {path}"
        )
    with open(file=path, mode="r", encoding="utf-8") as file:
        return rtoml.load(file)


def extract_pg_config(*, config: dict[str, Any]) -> PostgresConfig:
    pg_data = config.get("postgres", {})
    return PostgresConfig(
        user=pg_data["USER"],
        password=pg_data["PASSWORD"],
        db=pg_data["DB"],
        port=pg_data["PORT"],
    )


def print_env_var(*, env: ValidEnvs) -> None:
    print(f'export APP_ENV="{env.value}"')


def print_pg_vars(*, config: PostgresConfig) -> None:
    for key, value in asdict(config).items():
        print(f'export POSTGRES_{key.upper()}="{value}"')


def print_success(*, env: ValidEnvs) -> None:
    print(f"# Environment variables for {env.value.upper()} are printed.")


def main(*, env: str) -> None:
    validated_env = validate_env(env=env)
    config = read_config(env=validated_env)
    pg_config = extract_pg_config(config=config)

    print_env_var(env=validated_env)
    print_pg_vars(config=pg_config)
    print_success(env=validated_env)


def run_cli() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "env",
        choices=[e.value for e in ValidEnvs],
        help="Environment to export",
    )
    args = parser.parse_args()

    main(env=args.env)


if __name__ == "__main__":
    run_cli()  # pragma: no cover
