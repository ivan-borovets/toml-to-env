from pathlib import Path
from types import MappingProxyType

import pytest

from scripts.makefile.print_envs import (
    PostgresConfig,
    ValidEnvs,
    extract_pg_config,
    main,
    print_env_var,
    print_pg_vars,
    print_success,
    read_config,
    validate_env,
)


def test_validate_env():
    assert validate_env(env="development") == ValidEnvs.DEVELOPMENT
    assert validate_env(env="production") == ValidEnvs.PRODUCTION
    with pytest.raises(ValueError):
        validate_env(env="invalid")


def test_read_config(tmp_path, monkeypatch):
    config_file = tmp_path / "development.toml"
    config_file.write_text('[postgres]\nUSER = "admin"\nPORT = 5432\n')
    fake_config_paths = MappingProxyType(
        {
            ValidEnvs.DEVELOPMENT: config_file,
        }
    )
    monkeypatch.setattr(
        "scripts.makefile.print_envs.ENV_CONFIG_PATHS", fake_config_paths
    )
    result = read_config(env=ValidEnvs.DEVELOPMENT)
    assert result == {"postgres": {"USER": "admin", "PORT": 5432}}

    fake_config_paths = MappingProxyType(
        {
            ValidEnvs.DEVELOPMENT: Path("wrong_path"),
            ValidEnvs.PRODUCTION: None,
        }
    )
    monkeypatch.setattr(
        "scripts.makefile.print_envs.ENV_CONFIG_PATHS", fake_config_paths
    )
    with pytest.raises(FileNotFoundError):
        read_config(env=ValidEnvs.DEVELOPMENT)
    with pytest.raises(FileNotFoundError):
        read_config(env=ValidEnvs.PRODUCTION)


def test_extract_pg_config():
    config = {
        "postgres": {
            "USER": "user",
            "PASSWORD": "password",
            "DB": "db",
            "PORT": 5432,
        }
    }
    result = extract_pg_config(config=config)
    assert result == PostgresConfig(
        user="user", password="password", db="db", port=5432
    )

    config = {}
    with pytest.raises(KeyError):
        extract_pg_config(config=config)

    config = {
        "postgres": {
            "PASSWORD": "password",
            "DB": "db",
            "PORT": 5432,
        }
    }
    with pytest.raises(KeyError):
        extract_pg_config(config=config)


@pytest.mark.parametrize("field_to_break", ["USER", "PASSWORD", "DB", "PORT"])
def test_extract_pg_config_invalid_types(field_to_break):
    config = {
        "postgres": {
            "USER": "user",
            "PASSWORD": "password",
            "DB": "db",
            "PORT": 5432,
        }
    }
    config["postgres"][field_to_break] = {}
    with pytest.raises(TypeError):
        extract_pg_config(config=config)


def test_print_env_var(capsys, monkeypatch):
    print_env_var(env=ValidEnvs.DEVELOPMENT)
    captured = capsys.readouterr()
    assert captured.out.strip() == 'export APP_ENV="development"'


def test_print_pg_vars(capsys):
    config = PostgresConfig(user="user", password="password", db="db", port=5432)
    print_pg_vars(config=config)
    captured = capsys.readouterr()
    assert captured.out.strip() == (
        'export POSTGRES_USER="user"\n'
        'export POSTGRES_PASSWORD="password"\n'
        'export POSTGRES_DB="db"\n'
        'export POSTGRES_PORT="5432"'
    )


def test_print_success(capsys):
    print_success(env=ValidEnvs.DEVELOPMENT)
    captured = capsys.readouterr()
    assert captured.out.strip() == (
        "# Environment variables for DEVELOPMENT are printed."
    )
