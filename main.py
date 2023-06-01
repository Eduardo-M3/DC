import discord
from discord.ext import commands
import os


# Configuração do bot
intents = discord.Intents.all()
intents.typing = False
intents.presences = False


# Criar o bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Evento de inicialização
@bot.event
async def on_ready():
    os.system('cls')  # Executa o comando clr no console
    print(f'{bot.user.name} está online!')


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


# Comando para exibir o avatar do perfil de um usuário
@bot.command()
async def av(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.avatar:
        embed = discord.Embed(
            title="Avatar", description=f"Avatar de {member.mention}")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('O usuário não possui um avatar definido.')

# Rodar o bot
bot.run('')
