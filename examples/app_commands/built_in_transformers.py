from __future__ import annotations

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


# see discord.app_commands.transformers.BUILT_IN_TRANSFORMERS


@client.tree.command(name="str")
async def str_tr(interaction: discord.Interaction, string: str):
    """receive a string"""
    await interaction.response.send_message(f"string: {string}")


@client.tree.command(name="int")
async def int_tr(interaction: discord.Interaction, integer: int):
    """receive an integer"""
    await interaction.response.send_message(f"integer: {integer}")


@client.tree.command(name="float")
async def float_tr(interaction: discord.Interaction, number: int):
    """receive a float"""
    await interaction.response.send_message(f"number: {number}")


@client.tree.command(name="bool")
async def bool_tr(interaction: discord.Interaction, boolean: bool):
    """receive a boolean"""
    await interaction.response.send_message(f"boolean: {boolean}")


@client.tree.command()
async def user(interaction: discord.Interaction, user: discord.User):
    """receive a user"""
    await interaction.response.send_message(f"user: {user}")


@client.tree.command()
@app_commands.guild_only()
async def member(interaction: discord.Interaction, member: discord.Member):
    """receive a member"""
    await interaction.response.send_message(f"member: {member}")


@client.tree.command()
@app_commands.guild_only()
async def role(interaction: discord.Interaction, role: discord.Role):
    """receive a role"""
    await interaction.response.send_message(f"role: {role}")


@client.tree.command()
@app_commands.guild_only()
async def app_command_channel(
    interaction: discord.Interaction, channel: app_commands.AppCommandChannel
):
    """receive a channel. (stage, voice, text, announce(news), category, forum)"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def app_command_thread(
    interaction: discord.Interaction, thread: app_commands.AppCommandThread
):
    """receive a thread. (announce(news), private, public)"""
    await interaction.response.send_message(f"thread: {thread}")


@client.tree.command()
@app_commands.guild_only()
async def guild_channel(
    interaction: discord.Interaction, channel: discord.abc.GuildChannel
):
    """receive a guild channel. (stage, voice, text, announce(news), category, forum)"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def thread(interaction: discord.Interaction, thread: discord.Thread):
    """receive a thread. (announce(news), private, public)"""
    await interaction.response.send_message(f"thread: {thread}")


@client.tree.command()
@app_commands.guild_only()
async def stage_channel(
    interaction: discord.Interaction, channel: discord.StageChannel
):
    """receive a stage channel"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def voice_channel(
    interaction: discord.Interaction, channel: discord.VoiceChannel
):
    """receive a voice channel"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def text_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    """receive a text channel. (text, announce(news))"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def category_channel(
    interaction: discord.Interaction, channel: discord.CategoryChannel
):
    """receive a category channel"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
@app_commands.guild_only()
async def forum_channel(
    interaction: discord.Interaction, channel: discord.ForumChannel
):
    """receive a forum channel"""
    await interaction.response.send_message(f"channel: {channel}")


@client.tree.command()
async def attachment(interaction: discord.Interaction, attachment: discord.Attachment):
    """receive an attachment"""
    await interaction.response.send_message(f"attachment: {attachment}")


@client.tree.command()
async def all_dm(
    interaction: discord.Interaction,
    string: str,
    integer: int,
    number: float,
    boolean: bool,
    user: discord.User,
    attachment: discord.Attachment,
):
    """receive all types in a DM"""
    await interaction.response.send_message(
        "\n".join(
            (
                f"string: {string}",
                f"integer: {integer}",
                f"number: {number}",
                f"boolean: {boolean}",
                f"user: {user}",
                f"attachment: {attachment}",
            )
        )
    )


@client.tree.command()
@app_commands.guild_only()
async def all(
    interaction: discord.Interaction,
    string: str,
    integer: int,
    number: float,
    boolean: bool,
    user: discord.User,
    member: discord.Member,
    role: discord.Role,
    app_channel: app_commands.AppCommandChannel,
    app_thread: app_commands.AppCommandThread,
    guild_channel: discord.abc.GuildChannel,
    thread: discord.Thread,
    stage_channel: discord.StageChannel,
    voice_channel: discord.VoiceChannel,
    text_channel: discord.TextChannel,
    category_channel: discord.CategoryChannel,
    forum_channel: discord.ForumChannel,
):
    """receive all types in a guild"""
    await interaction.response.send_message(
        "\n".join(
            (
                f"string: {string}",
                f"integer: {integer}",
                f"number: {number}",
                f"boolean: {boolean}",
                f"user: {user}",
                f"member: {member}",
                f"role: {role}",
                f"app_channel: {app_channel}",
                f"app_thread: {app_thread}",
                f"guild_channel: {guild_channel}",
                f"thread: {thread}",
                f"stage_channel: {stage_channel}",
                f"voice_channel: {voice_channel}",
                f"text_channel: {text_channel}",
                f"category_channel: {category_channel}",
                f"forum_channel: {forum_channel}",
            )
        )
    )


if __name__ == "__main__":
    client.run("token")  # replace your bot token
