import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')


@bot.event
async def on_message(message):
    if message.author == bot.user:  # Verifica se o autor da mensagem é o próprio bot
        return  # Ignora mensagens do próprio bot
    if bot.user.mentioned_in(message):
        embed = discord.Embed(
            title="Help",
            description="",
            color=discord.Color.blurple()
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
            url="https://cdn.discordapp.com/attachments/1040612684317601896/1115355022981599363/Mov_1920_720_px.png")
        embed.add_field(
            name="hora",
            value="Comando usado para exibir a hora atual.",
            inline=False
        )
        embed.add_field(
            name="av @user",
            value="Comando usado para exibir o av do usuário.",
            inline=True
        )
        embed.add_field(
            name="bn @user",
            value="Comando usado para exibir o banner do usuário.",
            inline=True
        )
        embed.add_field(
            name="listar @cargo",
            value="Lista o ID de todos os usuários que possuem um determinado cargo.",
            inline=True
        )
        embed.add_field(
            name="mencionar @cargo",
            value="Menciona todos os usuários que possuem um determinado cargo.",
            inline=True
        )
        embed.add_field(
            name="verificar @cargo [ID's]",
            value="Retorna todos os usuários que possuem o cargo e não estão na lista informada, além de também exibir uma lista dos usuários que não possuem o cargo e foram informados.",
            inline=True
        )
        embed.add_field(
            name="levantamento",
            value="Faz o levantamento, exibindo os membros que não possuem a tag Equipe Mov Chat e os que possuem.",
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


@bot.command()
async def av(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.avatar:
        embed = discord.Embed(
            title="Avatar",
            description=f"Avatar de {member.mention}",
            color=discord.Color.blue()
        )
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Usuário sem av.')


@bot.command()
async def bn(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    user = await bot.fetch_user(user.id)
    if user.banner:
        embed = discord.Embed(
            title="Banner",
            description=f"Banner de {user.mention}",
            color=discord.Color.blue()
        )
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Usuário sem banner.')


@bot.command()
async def listar(ctx, cargo: discord.Role):
    membros = [str(membro.id)
               for membro in ctx.guild.members if cargo in membro.roles]
    membros_list = "\n".join(membros)
    await ctx.send(f'ID dos membros com o cargo {cargo.mention}:\n\n{membros_list}')


@bot.command()
async def mencionar(ctx, cargo: discord.Role):
    membros = [
        membro.mention for membro in ctx.guild.members if cargo in membro.roles]
    membros_list = "\n".join(membros)
    await ctx.send(f'Membros com o cargo {cargo.mention}:\n\n{membros_list}')


@bot.command()
async def verificar(ctx, cargo: discord.Role, *, membros_lista: str):
    # Obtém a lista de membros mencionada pelo usuário
    membros_mencionados = membros_lista.split()

    # Obtém todos os membros do servidor que possuem o cargo
    membros_com_cargo = cargo.members

    # Filtra os membros que possuem o cargo, mas não estão na lista mencionada
    membros_nao_mencionados = [
        membro for membro in membros_com_cargo if str(membro.id) not in membros_mencionados
    ]

    # Filtra os membros mencionados que não possuem o cargo
    membros_sem_cargo = [
        membro_id for membro_id in membros_mencionados if discord.utils.get(ctx.guild.members, id=int(membro_id)) not in membros_com_cargo
    ]

    # Menciona os membros que possuem o cargo, mas não foram mencionados
    if membros_nao_mencionados:
        mencoes = ' \n '.join(
            [membro.mention for membro in membros_nao_mencionados])
        await ctx.send(f'> Membros com o cargo {cargo.name}, mas não mencionados: \n\n\{mencoes}')
    else:
        await ctx.send('Todos os membros com o cargo estão mencionados.')

    # Exibe os membros mencionados que não possuem o cargo
    if membros_sem_cargo:
        membros_sem_cargo_nomes = ' \n '.join(
            [f"<@{membro_id}>" for membro_id in membros_sem_cargo])
        await ctx.send(f'> Membros mencionados sem o cargo {cargo.name}:\n\n {membros_sem_cargo_nomes}')
    else:
        await ctx.send('Todos os membros mencionados possuem o cargo.')


# Informe a tag desejada aqui
ID_TAG = "1093694361801338921"
ID_TAG2 = "1093694341505105984"
data_atual = datetime.now()
data_formatada = data_atual.strftime("%d/%m")
@bot.command()
async def levantamento(ctx):
    # Obtém o número total de membros no servidor
    total_members = len(ctx.guild.members)

    # Filtra os membros que possuem a tag desejada
    members_with_tag = [
        member for member in ctx.guild.members if ID_TAG in [str(role.id) for role in member.roles]
    ]
    # Filtra os membros que possuem a tag desejada
    members_with_tag2 = [
        member for member in ctx.guild.members if ID_TAG2 in [str(role.id) for role in member.roles]
    ]
    # Obtém o número de membros com a tag
    members_with_tag_count = len(members_with_tag)

    # Obtém o número de membros com a tag2
    members_with_tag2_count = len(members_with_tag2)

    # Cria a tabela usando a formatação de string
    # <@&{ID_TAG}>
    table = f"""**__LEVANTAMENTO {data_formatada}__**

**Sem tag:** {members_with_tag2_count:<5}\n
**Com tag:** {members_with_tag_count:<5}
"""
    await ctx.send(f"{table}")


@bot.command()
async def meus_servidores(ctx):
    servidores = bot.guilds
    for servidor in servidores:
        nome_servidor = servidor.name
        await ctx.send(f"Bot está presente no servidor: {nome_servidor}")


@bot.command()
@commands.has_permissions(administrator=True)
async def enviar_mensagem_privada(ctx, cargo: discord.Role, *, mensagem: str):
    # Filtra os membros que possuem o cargo
    membros_com_cargo = [
        membro for membro in ctx.guild.members if cargo in membro.roles]

    # Cria um canal de texto para coletar as respostas dos usuários
    canal_respostas = await ctx.guild.create_text_channel(name="respostas-bot")

    for membro in membros_com_cargo:
        try:
            # Envia a mensagem privada para cada membro com o cargo
            await membro.send(mensagem)

            # Aguarda a resposta do usuário no canal de respostas
            def check(m):
                return m.author == membro and m.channel == canal_respostas

            resposta = await bot.wait_for("message", check=check)

            # Envia a resposta para o canal de respostas
            await canal_respostas.send(f"Resposta de {membro.name}#{membro.discriminator}: {resposta.content}")

            print(
                f"Mensagem enviada para {membro.name}#{membro.discriminator}")
        except discord.Forbidden:
            print(
                f"Não foi possível enviar a mensagem para {membro.name}#{membro.discriminator} (privacidade desativada)")

    # Finaliza o comando removendo o canal de respostas
    await canal_respostas.delete()

