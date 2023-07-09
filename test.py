import git
import os
import click
from datetime import datetime


def get_repo() -> git.Repo:
    return git.Repo(".")


def create_folder(dir: str) -> None:
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            raise Exception("ERROR - cannot create the folder")


def get_name(git_config: git.GitConfigParser) -> str:
    name = git_config.get_value("user", "name")
    name = name.replace(" ", "-")
    name = "".join([c if c.isalnum() else "-" for c in name])
    name = "_".join(name.split("-"))
    name = name.lower()
    return name


def get_email(git_config: git.GitConfigParser) -> str:
    return git_config.get_value("user", "email")


def get_time() -> str:
    now = datetime.now()
    time, day = now.strftime("%H:%M:%S"), now.strftime("%Y-%m-%d")
    return f"{day}_{time}"


def push_repo(repo: git.Repo, m: str, dir: str, name: str) -> None:
    pass
        


def create_user(name: str, email: str, dir: str) -> None:
    if not os.path.exists(f"{dir}/{name}.md"):
        try:
            create_folder(dir)
            with open(f"{dir}/{name}.md", "w") as f:
                f.write(f"| Name | Email |\n")
                f.write(f"| ---- | ----- |\n")
                f.write(f"| {name} | {email} |\n\n\n")
                f.write(f"| in | out | content |\n")
                f.write(f"| -- | --- | ------- |\n")
        except:
            raise Exception("ERROR - cannot create the user file")


def entry_in(name: str, dir: str) -> None:
    try:
        with open(f"{dir}/{name}.md", "r+") as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            if f.read(1) == "\n":
                f.write(f"| {get_time()} |")
            else:
                raise Exception("!!! already punched in !!!")
    except Exception as e:
        raise e


def entry_out(name: str, dir: str) -> None:
    try:
        with open(f"{dir}/{name}.md", "r+") as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 1, os.SEEK_SET)
            if f.read(1) != "\n":
                content = click.prompt(">> what did you do?", type=str)
                f.write(f" {get_time()} | {content} |\n")
            else:
                raise Exception("!!! already punched out !!!")
    except Exception as e:
        raise e


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

    dir = "./" + dir + "/"
    repo = get_repo()
    name = get_name(repo.config_reader())
    email = get_email(repo.config_reader())
    create_user(name, email, dir)
    if punch_in:
        try:
            entry_in(name, dir)
            click.echo(f"pushed in at {get_time()} for {name}")
        except Exception as e:
            click.echo(e)
            exit(1)
    else:
        try:
            entry_out(name, dir)
            click.echo(f"pushed out at {get_time()} for {name}")
        except Exception as e:
            click.echo(e)
            exit(1)

    try:
        push_repo(repo, f"punched {name}", dir, name)
    except Exception as e:
        click.echo(e)


if __name__ == "__main__":
    punch()
