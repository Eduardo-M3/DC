import random
import discord
import asyncio
import datetime
from datetime import datetime
from discord.ext import commands


intents = discord.Intents.all()

# Definindo os prefixos
prefixes = ['!', '$']
bot = commands.Bot(command_prefix=prefixes, intents=intents)

# Função personalizada para verificar o prefixo usado
def get_prefix(bot, message):
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix
    return None

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Verifica se o autor da mensagem é o próprio bot
        return  # Ignora mensagens do próprio bot
    if bot.user.mentioned_in(message):
        # Lista de funcionalidades do bot
# Lista de funcionalidades do bot
        funcionalidades = [
            {
                "comando": "!hora",
                "descricao": "Exibe a hora atual."
            },
            {
                "comando": "!av @usuário",
                "descricao": "Mostra o avatar do usuário mencionado."
            },
            {
                "comando": "!bn @usuário",
                "descricao": "Exibe o banner do usuário mencionado."
            },
            {
                "comando": "!listar @cargo",
                "descricao": "Lista o ID de todos os membros com um determinado cargo."
            },
            {
                "comando": "!mencionar @cargo",
                "descricao": "Menciona todos os membros com um determinado cargo."
            },
            {
                "comando": "!verificar @cargo [ID's]",
                "descricao": "Verifica os membros com um cargo e uma lista de IDs fornecida."
            },
            {
                "comando": "!levantamento",
                "descricao": "Faz um levantamento dos membros com determinadas tags."
            },
            {
                "comando": "!msg @cargo mensagem",
                "descricao": "Envia uma mensagem para todos os membros com um determinado cargo."
            },
            {
                "comando": "!verificacao",
                "descricao": "Executa uma verificação personalizada (apenas para usuários autorizados)."
            },
        ]

        embed = discord.Embed(
            title="Menu de Ajuda",
            description="Aqui estão algumas das funcionalidades disponíveis:",
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

        for funcionalidade in funcionalidades:
            comando = funcionalidade["comando"]
            descricao = funcionalidade["descricao"]
            embed.add_field(
                name=comando,
                value=descricao,
                inline=False
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
@commands.has_permissions(administrator=True)
async def msg(ctx, cargo: discord.Role, *, mensagem: str):
    # Filtra os membros que possuem o cargo
    membros_com_cargo = [
        membro for membro in ctx.guild.members if cargo in membro.roles]

    membros_nao_enviados = []

    # Envia a mensagem privada para cada membro com o cargo
    for membro in membros_com_cargo:
        try:
            await membro.send(mensagem)
            await ctx.send(f"Mensagem enviada para {membro.name}#{membro.discriminator}")
        except discord.Forbidden:
            await ctx.send(f"Não foi possível enviar a mensagem para {membro.name}#{membro.discriminator} (privacidade desativada)")
            membros_nao_enviados.append(membro)

    if membros_nao_enviados:
        nomes_membros_nao_enviados = "\n".join(
            [f"{membro.name}#{membro.discriminator}" for membro in membros_nao_enviados])
        await ctx.send(f"Não foi possível enviar a mensagem para os seguintes membros com o cargo {cargo.mention}:\n{nomes_membros_nao_enviados}")
    else:
        await ctx.send(f"Mensagem enviada para todos os membros com o cargo {cargo.mention}.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Desculpe, você não tem permissão para usar esse comando.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando incorreto ou inexistente. Me marque ou digit !help para ver a lista de comandos disponíveis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argumento(s) necessário(s) está faltando. Verifique a sintaxe e tente novamente.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Argumento(s) inválido(s) fornecido(s). Verifique a sintaxe e tente novamente.")
    else:
        await ctx.send(f"Ocorreu um erro ao executar o comando: {error}")

@bot.command()
async def meus_servidores(ctx):
    allowed_ids = ["816633063147569162", "863502898041061397"]  # Lista de IDs permitidos

    if str(ctx.author.id) in allowed_ids:
        servidores = bot.guilds
        for servidor in servidores:
            nome_servidor = servidor.name
            await ctx.send(f"O bot está presente no servidor: {nome_servidor}")
    else:
        await ctx.send("Desculpe, você não tem permissão para executar este comando.")

@bot.command()
@commands.has_permissions(administrator=True)
async def verificacao(ctx, member: discord.Member):
    # Verifica se o autor do comando tem permissão para gerenciar cargos
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("Você não tem permissão para gerenciar cargos.")
        return
    
    # ID do cargo a ser removido
    id_cargo_remover = 1093694341505105984
    
    # IDs dos cargos a serem adicionados
    id_cargo_adicionar1 = 1093694361801338921
    id_cargo_adicionar2 = 1093693730642477118
    
    # Obtém o cargo a ser removido pelo ID
    cargo_remover = discord.utils.get(ctx.guild.roles, id=id_cargo_remover)
    if not cargo_remover:
        await ctx.send("O cargo a ser removido não foi encontrado.")
        return
    
    # Obtém os cargos a serem adicionados pelos IDs
    cargo_adicionar1 = discord.utils.get(ctx.guild.roles, id=id_cargo_adicionar1)
    cargo_adicionar2 = discord.utils.get(ctx.guild.roles, id=id_cargo_adicionar2)
    if not cargo_adicionar1 or not cargo_adicionar2:
        await ctx.send("Um ou mais cargos a serem adicionados não foram encontrados.")
        return
    
    # Remove o cargo especificado do membro mencionado
    await member.remove_roles(cargo_remover)
    
    # Adiciona os cargos definidos ao membro mencionado
    await member.add_roles(cargo_adicionar1, cargo_adicionar2)
    
    # Obtém as mensagens do canal
    async for message in ctx.channel.history(limit=10):
        # Verifica se a mensagem é anterior à do comando
        if message.id < ctx.message.id:
            # Verifica se há uma imagem anexada à mensagem
            if message.attachments:
                # Obtém a primeira imagem anexada
                attachment = message.attachments[0]
                # Baixa a imagem
                image = await attachment.to_file()
                
                # Envia a imagem para o canal de destino
                canal_destino = bot.get_channel(1093685279912628365)
                if canal_destino:
                    await canal_destino.send(file=image)
                    await canal_destino.send(member.id)
                    break
                else:
                    await ctx.send("O canal de destino não foi encontrado.")
                    break
            else:
                await ctx.send("Não foi encontrada uma imagem anexada à mensagem acima do comando.")
                break

# ==============================================================================================
# ==============================================================================================
# ==============================================================================================
metas = {
    "1093693730642477118": {
        "pontos": 20,
        "mensagens": 50
    },
    "1093693729388367953": {
        "pontos": 60,
        "mensagens": 100
    },
    "1093693727656128522": {
        "pontos": 100,
        "mensagens": 200
    },
    "1093693722941730856": {
        "pontos": 150,
        "mensagens": 350
    },
    "1093693720362229900": {
        "pontos": 200,
        "mensagens": 500
    },
    "1093689031142944838": {
        "pontos": 250,
        "mensagens": 800
    },
    "1093689024033603725": {
        "pontos": 300,
        "mensagens": 1200
    },
    "1093686708853297172": {
        "pontos": 350,
        "mensagens": 1800
    },
    "1093686694248730624": {
        "pontos": 420,
        "mensagens": 2000
    },
    "1093686692927520788": {
        "pontos": 460,
        "mensagens": 2500
    },
    "1093686691409186866": {
        "pontos": 460,
        "mensagens": 2500
    },
    "1093686688913563658": {
        "pontos": 480,
        "mensagens": 2700
    },
    "1093686686858358786": {
        "pontos": 500,
        "mensagens": 3000
    }
}

@bot.command()
@commands.has_permissions(administrator=True)
async def atmeta(ctx, cargo: discord.Role, pontos: int, mensagens: int):
    prefix = get_prefix(bot, ctx.message)
    if prefix == '$':
        metas[str(cargo.id)] = {
            "pontos": pontos,
            "mensagens": mensagens
        }
        await ctx.send(f"As metas para o cargo {cargo.mention} foram atualizadas.")

@bot.command()
@commands.has_permissions(administrator=True)
async def meta(ctx):
    prefix = get_prefix(bot, ctx.message)
    if prefix == '$':
        embed = discord.Embed(
            title="Metas dos Cargos",
            description="Aqui estão as metas definidas para cada cargo:",
            color=discord.Color.blurple()
        )

        for cargo_id, meta in metas.items():
            cargo = discord.utils.get(ctx.guild.roles, id=int(cargo_id))
            if cargo:
                embed.add_field(
                    name=cargo.name,
                    value=f"Pontos: {meta['pontos']}\nMensagens: {meta['mensagens']}",
                    inline=False
                )
        
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def up(ctx, member: discord.Member, pontos: int, mensagens: int):
    prefix = get_prefix(bot, ctx.message)
    if prefix == '$':
        for cargo_id, meta in metas.items():
            cargo = discord.utils.get(ctx.guild.roles, id=int(cargo_id))
            if cargo in member.roles:
                if pontos >= meta['pontos'] and mensagens >= meta['mensagens']:
                    # Membro atingiu a meta, verifica se é possível avançar para o próximo cargo
                    index = cargo.position
                    next_cargo = ctx.guild.roles[index + 1]
                    if next_cargo:
                        await member.add_roles(next_cargo)
                        await member.remove_roles(cargo)
                        await ctx.send(f"{member.mention} foi promovido para o cargo {next_cargo.mention}.")
                    else:
                        await ctx.send(f"{member.mention} atingiu a meta máxima.")
                else:
                    # Membro não atingiu a meta, verifica se é necessário rebaixar para o cargo anterior
                    index = cargo.position
                    previous_cargo = ctx.guild.roles[index - 1]
                    if previous_cargo:
                        await member.add_roles(previous_cargo)
                        await member.remove_roles(cargo)
                        await ctx.send(f"{member.mention} foi rebaixado para o cargo {previous_cargo.mention}.")
                    else:
                        await ctx.send(f"{member.mention} está no cargo mais baixo.")
                break
        else:
            await ctx.send(f"{member.mention} não possui nenhum cargo com metas definidas.")

# ==============================================================================================
# ==============================================================================================
# ==============================================================================================

citações = [
    "*Com grandes poderes vêm grandes responsabilidades*. - **Tio Ben, Homem-Aranha**",
    "*A persistência é o caminho do êxito.* - **Charlie Chaplin**",
    "*Só se pode alcançar um grande êxito quando nos mantemos fiéis a nós mesmos.* - **Dumbledore, Harry Potter**",
    "*O futuro pertence àqueles que acreditam na beleza de seus sonhos.* - **Eleanor Roosevelt**",
    "*Não há caminho para a felicidade. A felicidade é o caminho.* - **Buda**",
    "*O sucesso é a soma de pequenos esforços repetidos dia após dia.* - **Robert Collier**",
    "A verdadeira sabedoria está em reconhecer a própria ignorância. - Sócrates",
    "A felicidade não depende do que você tem ou de quem você é. Ela só depende do que você pensa. - Dale Carnegie",
    "*A verdadeira força vem de dentro.* - **Garen, League of Legends**",
    "*Nossos medos nos deixam mais humanos.* - **Vayne, League of Legends**",
    "*A coragem é a resistência e o domínio do medo, não a ausência dele.* - **Mark Twain**",
    "*O que não provoca minha morte faz com que eu fique mais forte.* - **Friedrich Nietzsche**",
    "*Não é a força, mas a constância dos bons sentimentos que conduz os homens à felicidade.* - **Friedrich Nietzsche**",
    "*A maior glória em viver não está em nunca cair, mas em nos levantarmos cada vez que caímos.* - **Ralph Waldo Emerson**",
    "*A educação é a arma mais poderosa que você pode usar para mudar o mundo.* - **Nelson Mandela**",
    "*O tempo é muito lento para os que esperam, muito rápido para os que têm medo, muito longo para os que lamentam, muito curto para os que festejam. Mas, para os que amam, o tempo é eternidade.* - **William Shakespeare**",
    "*O sucesso é ir de fracasso em fracasso sem perder entusiasmo.* - **Winston Churchill**",
]

@bot.command()
async def citação(ctx, variavel1: str, variavel2: str):
    # Lista de IDs permitidos
    allowed_ids = ["816633063147569162", "863502898041061397"]
    if str(ctx.author.id) in allowed_ids:
        citação_aleatória = random.choice(citações)
        texto = f"*Bom dia webfofos!*\nDormiram bem? Já tomaram café?\n\n{citação_aleatória}\n\n**Não esqueçam de clicar no “tenho interesse”.**\n{variavel1}\n@here\n\n> Mandem nas suas g10 queridos Assessores, vamos manter nossos staffs ativos, sejam espertos evitem advertências vocês tem até as {variavel2}h para mandar o print, lembrando que se não postar o print e não deixar ausência levará advertência da mesma forma."
        await ctx.send(texto)


@bot.command()
async def tarde(ctx, variavel1: str, variavel2: str):
    # Lista de IDs permitidos
    allowed_ids = ["816633063147569162", "863502898041061397"]
    if str(ctx.author.id) in allowed_ids:
        citação_aleatória = random.choice(citações)
        texto = f"*Boa tarde amigos, como estamos?*\nComo estamos? Todos bem?\n\n{citação_aleatória}\n\n**Não esqueçam de clicar no “tenho interesse”.**\n{variavel1}\n@here\n\n> Mandem nas suas g10 queridos Assessores, vamos manter nossos staffs ativos, sejam espertos evitem advertências vocês tem até as {variavel2}h para mandar o print, lembrando que se não postar o print e não deixar ausência levará advertência da mesma forma."
        await ctx.send(texto)


@bot.command()
async def noite(ctx, variavel1: str, variavel2: str):
    # Lista de IDs permitidos
    allowed_ids = ["816633063147569162", "863502898041061397"]
    if str(ctx.author.id) in allowed_ids:
        citação_aleatória = random.choice(citações)
        texto = f"*Alô, boa noite, todos bem?\n\n{citação_aleatória}\n\n**Não esqueçam de clicar no “tenho interesse”.**\n{variavel1}\n@here\n\n> Mandem nas suas g10 queridos Assessores, vamos manter nossos staffs ativos, sejam espertos evitem advertências vocês tem até as {variavel2}h para mandar o print, lembrando que se não postar o print e não deixar ausência levará advertência da mesma forma."
        await ctx.send(texto)

