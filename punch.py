import punch_clock
import click


@click.command()
@click.option("--dir", default="punch", help="directory to store the log files", type=str)
@click.option(
    "--punch_in",
    "-in",
    type=bool,
    default=False,
    help="log the time in",
    required=True,
    is_flag=True,
)
@click.option(
    "--punch_out",
    "-out",
    type=bool,
    default=False,
    help="log the time out",
    required=True,
    is_flag=True,
)
def punch(dir: str, punch_in: bool, punch_out: bool) -> None:
    if not (punch_in or punch_out):
        click.echo("!!! please specify either -in or -out !!!")
        return
    
    repo = punch_clock.get_repo()
    name = punch_clock.get_name(repo.config_reader())
    email = punch_clock.get_email(repo.config_reader())
    punch_clock.create_user(name, email, dir)

    if punch_in:
        try:
            punch_clock.entry_in(name, dir)
            click.echo(f"pushed in at {punch_clock.get_time()} for {name}")
        except Exception as e:
            click.echo(e)
            exit(1)
    else:
        try:
            punch_clock.entry_out(name, dir)
            click.echo(f"pushed out at {punch_clock.get_time()} for {name}")
        except Exception as e:
            click.echo(e)
            exit(1)

    try:
        punch_clock.push_repo(repo, f"punched {name}", dir, name)
    except Exception as e:
        click.echo(e)


if __name__ == "__main__":
    punch()
