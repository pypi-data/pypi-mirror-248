import click
import requests
from vijil_cli.vijilapi.config_handler import save_config
from vijil_cli.evaluations.commands import *

VIGIL_API_BASE_URL = "http://dockder-test-alb-2018306447.us-west-2.elb.amazonaws.com/api/v1"

@click.group()
def main():
    """Welcome to Vijil CLI tool."""

@main.command()
def demo():
    """Demonstrate the Vijil CLI."""
    click.echo("Hello from Vijil CLI!")

@main.command()
@click.option('--username', prompt='Enter your username')
@click.option('--token', prompt='Enter your token', hide_input=True)
def configure(username, token):
    """Configure the Vijil CLI."""
    click.echo(f"Configuring with username: {username} and token: {token}")
    save_config(username, token)
    verify_url = f"{VIGIL_API_BASE_URL}/tokens/verify"
    data = {"username": username, "token": token}

    try:
        response = requests.post(verify_url, json=data)
        response.raise_for_status()

        if response.json().get("verify"):
            click.echo("Token verification successful. Configuration complete.")
        else:
            click.echo("Token verification failed. Please check your credentials.")

    except requests.exceptions.RequestException as e:
        click.echo(f"Error during API request: {e}")

main.add_command(run_evaluation)
main.add_command(check_job_status)
main.add_command(stop_job)
main.add_command(stop_all_job)
main.add_command(delete_job)
main.add_command(download_file)
main.add_command(list_jobs)
main.add_command(get_job_detail)

if __name__ == '__main__':
    main()
