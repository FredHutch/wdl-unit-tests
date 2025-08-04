ifeq ($(GITHUB_ACTIONS),true)
    WORKERS = 24
else
    WORKERS = auto
endif

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

check_wdl_dirs:
	@uv run tests/validate_wdls.py

server_type_regulated:
	op run --no-masking -- uv run python -m tests.cromwellapi.server_type --regulated

server_type_not_regulated:
	op run --no-masking -- uv run python -m tests.cromwellapi.server_type --not-regulated

test_api_cached: check_env_vars check_wdl_dirs
	@op run -- uv run pytest -n $(WORKERS) \
	--color=yes --record-mode=once --verbose \
	tests/cromwellapi/

test_api_rewrite: check_env_vars
	op run -- uv run pytest -n $(WORKERS) \
	--color=yes --record-mode=rewrite --verbose \
	tests/cromwellapi/

regulated-data-envs:
	op inject -i .env-regulated > .env-temp

test_api_regulated_local: check_env_vars regulated-data-envs
	op run -- uv run --env-file .env-temp \
	pytest -n $(WORKERS) \
	--color=yes --record-mode=rewrite --verbose \
	tests/cromwellapi/ && \
	rm .env-temp

test_api_regulated: check_env_vars
	op run -- uv run pytest -n $(WORKERS) \
	--color=yes --record-mode=rewrite --verbose \
	tests/cromwellapi/

test_api_rewrite_json_report: check_env_vars
	op run -- uv run pytest -n $(WORKERS) \
	--json-report --json-report-file=results.json \
	--color=yes --record-mode=rewrite --verbose \
	tests/cromwellapi/

test_java_validate:
	@echo "Validating WDL files with womtool validate..."
	@bash scripts/cromwell_validate.sh

test_java_run:
	@echo "Running WDL files with cromwell run..."
	@bash scripts/cromwell_run.sh

ipython: check_env_vars
	cd tests/cromwellapi/ && \
	op run --no-masking -- uv run --with rich --with ipython python -m IPython

py: check_env_vars
	cd tests/cromwellapi/ && \
	op run --no-masking -- uv run python
