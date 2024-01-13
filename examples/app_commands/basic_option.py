from __future__ import annotations

from enum import Enum, auto
from typing import Literal

import discord
from discord import app_commands

MY_GUILD = discord.Object(id=0)  # replace your guild id


class MyClient(discord.Client):
    guild_id: discord.Object = MY_GUILD
    sync_global: bool = False  # using main.py

    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        if self.sync_global:
            await self.tree.sync()
        else:
            self.tree.clear_commands(guild=self.guild_id)
            self.tree.copy_global_to(guild=self.guild_id)
            await self.tree.sync(guild=self.guild_id)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")  # type: ignore
    print("------")


# default, optional.


@client.tree.command()
async def basic(interaction: discord.Interaction, string: str):
    """basic command"""
    await interaction.response.send_message(f"string: {string}")


@client.tree.command()
async def default(interaction: discord.Interaction, string: str = "default"):
    """default command"""
    await interaction.response.send_message(f"string: {string}")


@client.tree.command()
async def optional(interaction: discord.Interaction, string: str | None = None):
    """optional command"""
    if string is None:
        await interaction.response.send_message("string is None")
    else:
        await interaction.response.send_message(f"string: {string}")


# user, user/member, mentionable(member/role).


@client.tree.command()
async def user(interaction: discord.Interaction, user: discord.User):
    """user command"""
    await interaction.response.send_message(f"user: {user}")


@client.tree.command()
@app_commands.guild_only()
async def user_or_member(
    interaction: discord.Interaction, user: discord.User | discord.Member
):
    """user or member command"""
    await interaction.response.send_message(f"user or member: {user}")


@client.tree.command()
@app_commands.guild_only()
async def mentionable(
    interaction: discord.Interaction, mentionable: discord.Member | discord.Role
):
    """mentionable command"""
    await interaction.response.send_message(f"mentionable: {mentionable}")


# Choice


@client.tree.command()
@app_commands.choices(
    color=[
        app_commands.Choice(name="red", value=0),
        app_commands.Choice(name="green", value=1),
        app_commands.Choice(name="blue", value=2),
    ]
)
async def choice(interaction: discord.Interaction, color: app_commands.Choice[int]):
    """choice command"""
    await interaction.response.send_message(f"color: {color.name}")


# Literal


@client.tree.command()
async def literal(
    interaction: discord.Interaction, color: Literal["red", "green", "blue"]
):
    """literal command"""
    await interaction.response.send_message(f"color: {color}")


# Enum


class ColorEnum(Enum):
    red = auto()
    green = auto()
    blue = auto()


@client.tree.command()
async def enum(interaction: discord.Interaction, color: ColorEnum):
    """enum command"""
    await interaction.response.send_message(f"color: {color.name}")


# Autocomplete


color_list = ["red", "green", "blue"]


async def color_autocomplete(interaction: discord.Interaction, current: str):
    """color autocomplete"""
    return [
        app_commands.Choice(name=color, value=color)
        for color in color_list
        if color.startswith(current)
    ]


@client.tree.command()
@app_commands.autocomplete(color=color_autocomplete)
async def autocomplete(interaction: discord.Interaction, color: str):
    """with autocomplete command"""
    await interaction.response.send_message(f"color: {color}")


# Another way to register autocomplete


@client.tree.command()
async def autocomplete2(interaction: discord.Interaction, color: str):
    """with autocomplete command"""
    await interaction.response.send_message(f"color: {color}")


@autocomplete2.autocomplete("color")
async def color_autocomplete2(interaction: discord.Interaction, current: str):
    """color autocomplete"""
    return [
        app_commands.Choice(name=color, value=color)
        for color in color_list
        if color.startswith(current)
    ]


# Range


@client.tree.command()
async def range(
    interaction: discord.Interaction, number: app_commands.Range[int, 1, 10]
):
    """number with range (1 <= number <= 10). see document(discord.app_commands.Range)"""
    await interaction.response.send_message(f"number: {number}")


if __name__ == "__main__":
    client.run("token")  # replace your bot token
