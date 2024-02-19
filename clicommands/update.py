import click
from clicommands.glue_commands import update_stack_by_name as update_glue_stack_by_name

@click.group()
def update():
    click.echo("Inside update group")

@update.command()
def dashboard():
    click.echo("Inside dashboard command")

@update.command()
@click.option('--stack-name', required=True, help='Name of the stack to be updated')
@click.option('--template-body', help='Path to the modified template')
@click.option('--template-url', help='S3 url to the modified template') 
@click.option('--parameters-path', default="glue.local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
def glue(stack_name, template_body, template_url, parameters_path, region, profile):
    if template_body and template_url:
        raise ValueError("template_body and template_url are mutually exclusive")
    elif not template_body and not template_url:
        raise ValueError("Either template_body or template_url must be provided")

    update_glue_stack_by_name(stack_name, template_body, template_url, parameters_path, region, profile)