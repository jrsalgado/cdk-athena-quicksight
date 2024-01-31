import click

@click.group()
def deploy():
    click.echo("Inside Deploy group")

# Analysis Commands
@deploy.command()
def analysis():
    click.echo("Deploying Analysis")

@deploy.command()
def analyses():
    click.echo("Deploying multiple Analysis")


# DataSources Commands
@deploy.command()
def data_source():
    click.echo("Deploying DataSources")

@deploy.command()
def data_sources():
    click.echo("Deploying multiple DataSources")


# DataSources Commands
@deploy.command()
def data_set():
    click.echo("Deploying DataSets")

@deploy.command()
def data_sets():
    click.echo("Deploying multiple DataSets")


# Dashboards Commands
@deploy.command()
def dashboard():
    click.echo("Deploying Dashboard")

@deploy.command()
def dashboards():
    click.echo("Deploying multiple Dashboards")

