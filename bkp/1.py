import discord
from discord.ext import commands


# Configuração do bot
intents = discord.Intents.all()
intents.typing = False
intents.presences = False


# Criar o bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Evento de inicialização
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')


# Comando simples
@bot.command()
async def oi(ctx):
    await ctx.send('Olá!')


# Comando com argumento
@bot.command()
async def bv(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send('Por favor, mencione um usuário para cumprimentar!')
    else:
        await ctx.send(f'Olá, {member.mention}!')


# Rodar o bot
bot.run('MTA4NTkwMDYyODI0MjQ3NzA1Ng.Gjpk8b.tuyObT7jXcvp2yDSHNoP5PzdJ2GIm4jmwavfFs')
