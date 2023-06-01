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

# Comando para o módulo VIP


@bot.command()
@commands.has_role('VIP')  # Verifica se o usuário possui o cargo "VIP"
async def vip(ctx):
    options = {
        '🟢': 'create_role',
        '🟠': 'change_role_name',
        '🔵': 'change_role_color'
    }

    embed = discord.Embed(
        title='Menu VIP', description='Selecione uma opção para gerenciar seu VIP:')

    for emoji, option in options.items():
        embed.add_field(name=emoji, value=option, inline=True)

    message = await ctx.send(embed=embed)

    for emoji in options.keys():
        await message.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author and reaction.message == message

    try:
        while True:
            reaction, _ = await bot.wait_for('reaction_add', check=check, timeout=60.0)

            option = options.get(reaction.emoji)
            await handle_option(ctx, option)

            # Exclui a mensagem anterior do menu
            await message.delete()

            # Atualiza o menu com as opções restantes
            embed = discord.Embed(
                title='Menu VIP', description='Selecione uma opção para gerenciar seu VIP:')

            for emoji, option in options.items():
                embed.add_field(name=emoji, value=option, inline=True)

            message = await ctx.send(embed=embed)

            for emoji in options.keys():
                await message.add_reaction(emoji)

    except TimeoutError:
        await ctx.send('Tempo esgotado. Por favor, tente novamente.')


async def handle_option(ctx, option):
    if option == 'create_role':
        await create_role(ctx)
    elif option == 'change_role_name':
        await change_role_name(ctx)
    elif option == 'change_role_color':
        await change_role_color(ctx)


async def create_role(ctx):
    # Verifica se o usuário já tem um cargo associado
    if get_vip_role(ctx.author) is not None:
        await ctx.send('Você já possui um cargo associado.')
        return

    vip_role_name = f'VIP - {ctx.author.name}'
    vip_role = discord.utils.get(ctx.guild.roles, name=vip_role_name)
    if vip_role is None:
        vip_role = await ctx.guild.create_role(name=vip_role_name)
        await ctx.author.add_roles(vip_role)

    await ctx.send('Cargo criado com sucesso!')


async def change_role_name(ctx):
    vip_role = get_vip_role(ctx.author)
    if vip_role is not None:
        await ctx.send('Digite o novo nome para o cargo:')

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            message = await bot.wait_for('message', check=check, timeout=60.0)
            new_name = message.content

            # Verifica se o novo nome já está sendo usado por outro cargo VIP
            existing_role = discord.utils.get(ctx.guild.roles, name=new_name)
            if existing_role is not None and existing_role != vip_role:
                await ctx.send('O nome escolhido já está sendo usado por outro cargo VIP.')
                return

            await vip_role.edit(name=new_name)
            await ctx.send('Nome do cargo alterado com sucesso!')
        except TimeoutError:
            await ctx.send('Tempo esgotado. Por favor, tente novamente.')
    else:
        await ctx.send('Você ainda não criou um cargo.')


async def change_role_color(ctx):
    vip_role = get_vip_role(ctx.author)
    if vip_role is not None:
        await ctx.send('Digite o código RGB para a nova cor do cargo (formato: R, G, B):')

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            message = await bot.wait_for('message', check=check, timeout=60.0)
            rgb = message.content.split(',')
            rgb = [int(c.strip()) for c in rgb]

            # Verifica se o código RGB é válido
            if len(rgb) != 3 or any(c < 0 or c > 255 for c in rgb):
                await ctx.send('O código RGB fornecido é inválido.')
                return

            # Altera a cor do cargo
            color = discord.Color.from_rgb(*rgb)
            await vip_role.edit(color=color)
            await ctx.send('Cor do cargo alterada com sucesso!')
        except TimeoutError:
            await ctx.send('Tempo esgotado. Por favor, tente novamente.')
    else:
        await ctx.send('Você ainda não criou um cargo.')


def get_vip_role(member):
    for role in member.roles:
        if role.name.startswith('VIP -') and role.name.split(' - ')[-1] == member.name:
            return role
    return None


# Rodar o bot
bot.run('MTA4NTkwMDYyODI0MjQ3NzA1Ng.GLHfhF.7xlHOPZkMlKCWWOReRVDgbVwiZu1ElOqhTNXCE')