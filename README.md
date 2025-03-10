# toml-to-env

<p align="center">
  <a href="https://codecov.io/gh/ivan-borovets/toml-to-env">
    <img src="https://codecov.io/gh/ivan-borovets/toml-to-env/graph/badge.svg" alt="Codecov Coverage"/>
  </a>
</p>

Example implementation of loading environment variables directly from TOML configs, bypassing .env files.

<p align="center">
  <img src="docs/pipeline.svg" alt="Pipeline" />
  <br><em>Figure 1: <b>Pipeline</b></em>
</p>

## Purpose

Demonstrates converting TOML config files into shell environment variables.
Enables environment switching with one command, avoiding `.env` files.
Not a library or tool — purely an example to adapt for your needs.

## Usage

1. Copy these files to your project:

* `config/` (TOML configs, e.g., `development.toml`, `production.toml`)
* `scripts/makefile/print_envs.py`
* Makefile snippets: `env.dev`, `env.prod`, `env.which` (and dependencies) or entire `Makefile`

2. Set aliases in shell:

```shell
alias env.dev='source <(make env.dev) && echo APP_ENV is set to $APP_ENV'
alias env.prod='source <(make env.prod) && echo APP_ENV is set to $APP_ENV'
```

Aliases disappear on shell restart; run the commands again or add to shell config (e.g., ~/.bashrc, ~/.zshrc).

3. Switch environments:

```shell
env.dev   # Load dev environment
env.prod  # Load prod environment
```

4. Check current environment:

```shell
make env.which  # Prints APP_ENV value
```

## Test Coverage

Optional, available in this repository for `print_envs.py`:

```shell
make code.cov.html
```

## Docker Compose Demo

Optional, tests environment variable setup with Postgres:

* Docker Compose uses exported variables (e.g., `POSTGRES_*`).
* Run: `make up.db`
* Stop: `make down`
* See `docker-compose.yaml` in repo for details.

## Notes

* Requires Python 3.12 and `rtoml` (`pip install rtoml`) for `print_envs.py`.
* Add `config/production.toml` to `.gitignore` — use `production.toml.example` as a placeholder.
* Adapt files and logic as needed — this is a minimal example, not a complete solution.

