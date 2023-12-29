# commands.py
import click
import types
from datetime import datetime
from vijil_cli.vijilapi.api_handler import (
    send_evaluation_request,
    job_status_request,
    stop_job_request,
    stop_all_job_request,
    delete_job_request,
    download_report_request,
    list_job_request,
    model_token_request
)
from .options import *

@click.command()
@click.option('--model-type', prompt='Choose the model type', type=click.Choice(MODEL_TYPE_CHOICES))
@click.option('--model-name', prompt='Enter the model name')
@click.option('--dimension', prompt='Choose the trust dimension', type=click.Choice(PROBES_CHOICES))
@click.option('--generations', prompt='Enter the number of generations', type=click.IntRange(1, 100))
def run(model_type, model_name, dimension, generations):
    """Run the evaluation."""

    available_model_names = MODEL_NAMES_MAPPING.get(model_type, [])
    if not available_model_names:
        click.echo("No model names available for the selected model type.")
        return
    if model_name not in available_model_names:
        # click.echo(f"Invalid model name. Available model names are: {', '.join(available_model_names)}")
        model_name = click.prompt('Please Choose the model name from this options', type=click.Choice(available_model_names))
    if model_name == 'other':
        custom_model_name = click.prompt('Enter custom model name')
        model_name = custom_model_name

    probes = PROBES_DIMENSIONS_MAPPING.get(dimension)

    click.echo(f"Running evaluation for model type: {model_type}, model name: {model_name}")

    try:
        result = send_evaluation_request(model_type, model_name, probes, generations)
        if result.get("task_id"):
            click.echo(f"Successfully Create Evaluation, Check Job Status by ID: {result.get('task_id')}")    
        else:
            click.echo(f"Response: {result}")

    except ValueError as e:
        click.echo(f"Error: {e}")


@click.command()
@click.option('--id', prompt='Enter ID that you received while creating evaluation', type=str)
def status(id):
    """Check Job Status By it's ID."""

    click.echo(f"Getting Job status for ID: {id}")

    try:
        result = job_status_request(id)
        if "job_result" in result:
            click.echo(f"Job Status: {result.get('status')}") 
            click.echo(f"Job Result: {result.get('job_result')}")
        elif "status" in result:
            click.echo(f"Job Status: {result.get('status')}") 
        elif isinstance(result, type([])) and len(result) > 0:
            click.echo("-" * 60)
            for job in result:
                click.echo(f"Job ID: {job.get('job_id', '')}")
                click.echo(f"Model Type: {job.get('model_type', '')}")
                click.echo(f"Model Name: {job.get('model_name', '')}")
                click.echo(f"Probe Group: {job.get('probe_group', '')}")
                click.echo("Probes:")
                for probe in job.get('probe', []):
                    click.echo(f"  - {probe}")

                click.echo("Detectors:")
                for detector in job.get('detector', []):
                    click.echo(f"  - {detector}")
                click.echo(f"Start Time: {format_datetime(job.get('start_time', ''))}")
                click.echo(f"Report: {job.get('report', '')}")
                click.echo(f"Hitlog: {job.get('hitlog', '')}")
                click.echo("-" * 60)
        else:
            click.echo("No Data Found.")

    except ValueError as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--id', default='', help='Enter ID that you received while creating evaluation')
@click.option('-a', '--all', is_flag=True, help='Stop all running evaluations.')
def stop(id, all):
    """Stop Evaluation by it's Id or stop all evaluations."""

    if all:
        click.echo(f"Stopping all running evaluations.")
        try:
            result = stop_all_job_request()
            if result.get("status"):
                click.echo(f"Job Status: {result.get('status')}") 
        except ValueError as e:
            click.echo(f"Error: {e}")
    else:
        if not id:
            click.echo("Please provide the ID for stopping a specific job.")
            return
        click.echo(f"Stopping Evaluation of ID: {id}")
        try:
            result = stop_job_request(id)
            if result.get("status"):
                click.echo(f"Job Status: {result.get('status')}") 
        except ValueError as e:
            click.echo(f"Error: {e}")

@click.command()
@click.option('--id', prompt='Enter ID that you received while creating evaluation', type=str)
def delete(id):
    """Delete Evaluation by it's Id."""

    click.echo(f"Deleting evaluation of ID: {id}")

    try:
        result = delete_job_request(id)
        if result:
            click.echo(f"{result.get('message')}") 

    except ValueError as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--file-id', prompt='Enter the Report/Hitlog ID')
def download(file_id):
    """Download a Report/Hitlog file by on its ID."""
    
    try:
        result = download_report_request(file_id)
        if result:
            click.echo(f"{result}") 

    except ValueError as e:
        click.echo(f"Error: {e}")

def format_datetime(datetime_str):
    """Format datetime from API response."""
    if datetime_str:
        try:
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%Y/%m/%d %H:%M")
        except ValueError:
            return datetime_str
    else:
        return datetime_str

@click.command()
def list():
    """List all jobs."""

    try:
        result = list_job_request()
        if len(result) > 0:
            # table_data = result.get("table_data")
            
            for job in result:
                click.echo(f"ID: {job.get('task_id', '')}")
                click.echo(f"Model Type: {job.get('model_type', '')}")
                click.echo(f"Model Name: {job.get('model_name', '')}")
                click.echo(f"Probe Group: {job.get('probe_group', '')}")
                click.echo(f"Job ID: {job.get('job_id', '')}")
                click.echo(f"Status: {job.get('status', '')}")
                click.echo(f"Result: {job.get('job_result', '')}")
                click.echo(f"Start Time: {format_datetime(job.get('start_time', ''))}")
                click.echo(f"End Time: {format_datetime(job.get('end_time', ''))}")
                click.echo("-" * 60)  
        else:
            click.echo("No Jobs found.")

    except ValueError as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--token', prompt='Enter the token of replicate account')
def replicate(token):
    """Set Repliate Account Token to Vijil."""
    
    try:
        result = model_token_request(token, "replicate")
        if result:
            click.echo(f"SuccessFully Saved Replicate Token.") 

    except ValueError as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--token', prompt='Enter the token of huggingface account')
def huggingface(token):
    """Set Huggingface Account Token to Vijil."""
    
    try:
        result = model_token_request(token, "hf")
        if result:
            click.echo(f"SuccessFully Saved Huggingface Token.") 

    except ValueError as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--token', prompt='Enter the token of OctoAI account')
def octo(token):
    """Set OctoAI Account Token to Vijil."""
    
    try:
        result = model_token_request(token, "octoai")
        if result:
            click.echo(f"SuccessFully Saved OctoAI Token.") 

    except ValueError as e:
        click.echo(f"Error: {e}")