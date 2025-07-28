import click

from .proof import ProofApi

proof_api = ProofApi()


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
    cromwell_server_is_up = proof_api.is_cromwell_server_up()

    if check_status:
        if cromwell_server_is_up:
            click.echo("Cromwell server is up")
        else:
            click.echo("Cromwell server is down")

        click.echo(
            f"regulated data: {proof_api.status()['jobInfo']['USE_REGULATED_DATA']}"
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
