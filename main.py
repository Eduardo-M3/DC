import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        embed = discord.Embed(
            title="Help",
            description="Olá! Eu sou um bot de exemplo.",
            color=discord.Color.random()
        )

        if message.author.avatar:
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.avatar.url
            )
        else:
            embed.set_author(
                name=message.author.name
            )

        embed.set_footer(
            text="Menu de ajuda",
            icon_url=bot.user.avatar.url
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1040612684317601896/1114192302982823946/Banner.png")
        embed.add_field(
            name="hora",
            value="Comando usado para exibir a hora atual.",
            inline=False
        )
        embed.add_field(
            name="Campo 2",
            value="Valor 2",
            inline=True
        )
        embed.timestamp = datetime.utcnow()

        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.command()
async def hora(ctx):
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M:%S")
    await ctx.send(f"A hora atual é: {hora_atual}")

