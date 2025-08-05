import contextlib
import os
import sys

import click

from .proof import ProofApi


@contextlib.contextmanager
def suppress_cache_messages():
    """Context manager to suppress cache-related print statements"""
    original_stdout = sys.stdout

    class FilteredStdout:
        def __init__(self, original):
            self.original = original

        def write(self, text):
            if text.strip() not in [
                "result not in cache",
                "result in cache, returning it",
            ]:
                self.original.write(text)

        def flush(self):
            self.original.flush()

        def __getattr__(self, name):
            return getattr(self.original, name)

    try:
        sys.stdout = FilteredStdout(original_stdout)
        yield
    finally:
        sys.stdout = original_stdout


@click.command()
@click.option(
    "--regulated/--not-regulated",
    help="Run a PROOF Cromwell server in regulated or unregulated mode",
)
@click.option(
    "--check-status",
    is_flag=True,
    help="Check the status of the Cromwell server",
)
@click.pass_context
def server_type(ctx, regulated, check_status):
    """Run a PROOF Cromwell server in regulated or unregulated mode"""
    op_srv_acct_token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    if not op_srv_acct_token:
        click.echo(
            "OP_SERVICE_ACCOUNT_TOKEN environment variable is not set", err=True
        )
        raise click.Abort()

    with suppress_cache_messages():
        proof_api = ProofApi()

        cromwell_server_is_up = proof_api.is_cromwell_server_up()

        if check_status:
            if cromwell_server_is_up:
                click.echo(click.style("Cromwell server is up", fg="green"))
            else:
                click.echo(click.style("Cromwell server is down", fg="red"))

            click.echo(
                f"regulated data: {click.style(str(proof_api.status()['jobInfo']['USE_REGULATED_DATA']), fg='blue')}"
            )
            ctx.exit(0)

        if regulated:
            click.echo("Running server in regulated mode")
            proof_api.regulated_data = True
            if cromwell_server_is_up:
                click.echo("Cromwell server is up")
                if proof_api.status()["jobInfo"]["USE_REGULATED_DATA"]:
                    click.echo("Regulated data is enabled, let's do this!")
                    ctx.exit(0)
                else:
                    click.echo(
                        "Regulated data is disabled; stopping then starting as regulated"
                    )
                    proof_api.stop()
                    proof_api.wait_for_stopped()
                    proof_api.start()
                    proof_api.wait_for_up()
                    click.echo("Regulated data is enabled, let's do this!")
            else:
                click.echo("Cromwell server is down; starting as regulated")
                proof_api.start()
                proof_api.wait_for_up()
                click.echo("Regulated data is enabled, let's do this!")
        else:
            click.echo("Running server in not-regulated mode")
            proof_api.regulated_data = False
            if cromwell_server_is_up:
                click.echo("Cromwell server is up")
                if not proof_api.status()["jobInfo"]["USE_REGULATED_DATA"]:
                    click.echo("Regulated data is disabled, let's do this!")
                    ctx.exit(0)
                else:
                    click.echo(
                        "Regulated data is enabled; stopping then starting as not regulated"
                    )
                    proof_api.stop()
                    proof_api.wait_for_stopped()
                    proof_api.start()
                    proof_api.wait_for_up()
                    click.echo("Regulated data is disabled, let's do this!")
            else:
                click.echo("Cromwell server is down; starting as not regulated")
                proof_api.start()
                proof_api.wait_for_up()
                click.echo("Regulated data is disabled, let's do this!")


if __name__ == "__main__":
    server_type()
