import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')


@bot.command()
async def oi(ctx):
    embed = discord.Embed(
        title="Apresentação",
        description="Olá! Eu sou um bot de exemplo.",
        color=discord.Color.blue()
    )
    embed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar.url  # Corrigido para usar ctx.author.avatar.url
    )
    embed.set_footer(
        text="Bot de Exemplo",
        icon_url=bot.user.avatar.url  # Corrigido para usar bot.user.avatar.url
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_image(url="https://example.com/image.jpg")
    embed.add_field(
        name="Campo 1",
        value="Valor 1",
        inline=False
    )
    embed.add_field(
        name="Campo 2",
        value="Valor 2",
        inline=True
    )
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)
