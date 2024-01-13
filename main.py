from __future__ import annotations

import importlib
from collections.abc import Generator
from pathlib import Path
from typing import Any

import click
import discord


@click.group()
def cli():
    pass


def get_path(dir: Path, root: Path) -> Generator[str, Any, Any]:
    if not dir.exists() and not dir.is_dir():
        return

    for path in dir.iterdir():
        if path.is_dir():
            yield from get_path(path, root)
        elif path.suffix == ".py":
            yield path.relative_to(root).with_suffix("").as_posix().replace("/", ".")


def get_names() -> tuple[str, ...]:
    root = Path(__file__).parent
    dir = root / "examples"
    return tuple(get_path(dir, root))


@cli.command()
@click.option("--token", "-t", type=str, required=True)
@click.option("--guild-id", "-g", type=int, required=True)
@click.argument("name")
def run(token: str, guild_id: int, name: str):
    names = get_names()
    if name not in names:
        click.echo("name must be a valid example name. see list command.", err=True)

    click.echo(f"starting {name}...")
    module = importlib.import_module(name)
    client: discord.Client = module.client
    client.guild_id = discord.Object(id=guild_id)  # type: ignore
    client.run(token)


@cli.command(name="list")
def list_up():
    names = get_names()
    click.echo("\n".join(names))


if __name__ == "__main__":
    cli()
