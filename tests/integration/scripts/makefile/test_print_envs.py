import sys
from types import MappingProxyType
from unittest.mock import Mock, patch

from scripts.makefile.print_envs import BASE_DIR_PATH, ValidEnvs, main, run_cli


def test_main(tmp_path, monkeypatch, capsys):
    config_file = tmp_path / "development.toml"
    config_file.write_text(
        """
    [postgres]
    USER = "test_integration_user"
    PASSWORD = "test_test_integration_password"
    DB = "test_test_integration_db"
    PORT = 5432
        """
    )
    fake_config_paths = MappingProxyType(
        {
            ValidEnvs.DEVELOPMENT: config_file,
        }
    )
    monkeypatch.setattr(
        "scripts.makefile.print_envs.ENV_CONFIG_PATHS", fake_config_paths
    )

    main(env="development")

    captured = capsys.readouterr()
    assert 'export APP_ENV="development"' in captured.out
    assert 'export POSTGRES_USER="test_integration_user"' in captured.out
    assert 'export POSTGRES_PASSWORD="test_test_integration_password"' in captured.out
    assert 'export POSTGRES_DB="test_test_integration_db"' in captured.out
    assert 'export POSTGRES_PORT="5432"' in captured.out


def test_run_cli(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["script_name.py", "development"])

    with patch("scripts.makefile.print_envs.main") as mock_main:
        run_cli()
        mock_main.assert_called_once_with(env="development")
