# from https://stackoverflow.com/a/10858332/1091766
# function to check a named environment variable
# see usage below for examples
check_defined = \
  $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
  $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Virtual env is not activated, run: 'source .venv/bin/activate'"; \
		exit 1; \
	fi

# include sort imports via `--select I`
lint-fix: check_venv
	uv sync
	ruff check --select I --fix tests/

# include sort imports via `--select I`
lint-check: check_venv
	uv sync
	ruff check --select I tests/

format: check_venv
	uv sync
	ruff format tests/

check_env_vars:
	$(call check_defined, PATH_ROOTS, env var for which paths to scrub in vcr cassettes)
	$(call check_defined, PROOF_API_TOKEN_DEV, env var for test PROOF user)

test_api_cached: check_venv check_env_vars
	uv run pytest --record-mode=once tests/cromwellapi/ --verbose -s

test_api_rewrite: check_venv check_env_vars
	uv run pytest --record-mode=rewrite tests/cromwellapi/ --verbose -s
