# from https://stackoverflow.com/a/10858332/1091766
# function to check a named environment variable
# see usage below for examples
check_defined = \
  $(strip $(foreach 1,$1, \
    $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
  $(if $(value $1),, \
    $(error Undefined $1$(if $2, ($2))))

# include sort imports via `--select I`
lint-fix:
	uv run ruff check --select I --fix tests/

# included rules that are check specified in pyproject.toml
# see https://docs.astral.sh/ruff/rules/ for rules
lint-check:
	uv run ruff check tests/

format-fix:
	uv run ruff format tests/

format-check:
	uv run ruff format --check tests/

check_env_vars:
	$(call check_defined, PATH_ROOTS, env var for which paths to scrub in vcr cassettes)
	$(call check_defined, PROOF_API_TOKEN_DEV, env var for test PROOF user)

test_api_cached: check_env_vars
	op run -- uv run pytest -n auto --color=yes --record-mode=once --verbose -s tests/cromwellapi/

test_api_rewrite: check_env_vars
	op run -- uv run pytest -n auto --color=yes --record-mode=rewrite --verbose -s tests/cromwellapi/

ipython: check_env_vars
	cd tests/cromwellapi/ && \
	op run --no-masking -- uv run --with rich --with ipython python -m IPython

py: check_env_vars
	cd tests/cromwellapi/ && \
	op run --no-masking -- uv run python
