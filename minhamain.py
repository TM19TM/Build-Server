import discord
import os 
from dotenv import load_dotenv 

# --- Carrega as variáveis do .env ---
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN") 
# ------------------------------------

# VERIFICAÇÃO IMPORTANTE: Se o TOKEN não for encontrado, avisa o usuário.
if TOKEN is None:
    print("ERRO CRÍTICO: O 'DISCORD_TOKEN' não foi encontrado no arquivo .env.")
    print("Por favor, verifique se o arquivo .env existe e tem a linha: DISCORD_TOKEN=SEU_TOKEN")
    exit() # Encerra o script se não houver token

# Define as intenções (permissões) que seu bot precisa
intents = discord.Intents.default()
intents.message_content = True # Permite que o bot leia mensagens
intents.guilds = True # Permite que o bot veja informações do servidor (guilda)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logamos como {client.user}') # Avisa no terminal que o bot está online
    
    # --- NOVO: Define a Atividade do Bot ---
    # Tipos: playing, watching, listening, streaming
    activity = discord.Activity(type=discord.ActivityType.listening, name="!ajuda")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Atividade do bot definida como 'Ouvindo !ajuda'")
    # ------------------------------------

@client.event
async def on_message(message):
    # Impede que o bot responda a si mesmo
    if message.author == client.user:
        return
    
    # Comando !ajuda (SÓ COMANDOS DO PORTFÓLIO)
    if message.content.startswith('!ajuda'):
        await message.channel.send("Comandos deste bot:\n"
                                   "🔹 `!oi` - Eu te dou oi!\n"
                                   "🔹 `!Developer` - Vê quem me criou.\n"
                                   "🔸 `!serverportfolio` - Configura este servidor de Portfólio.")
        return 

    # Comando !Developer 
    if message.content.startswith('!Developer'):
        await message.channel.send("Desenvolvido por: Matheus B \n"
                                   "discord: https://discord.gg/DDHNZBGM8k \n"
                                   "Instagram: @matheus_b_dev \n")
        return 

    # Comando !oi
    if message.content.startswith('!oi'):
        await message.channel.send('Olá!')
        return 

    # --- COMANDO !SERVERPORTFOLIO ---
    if message.content.startswith('!serverportfolio'):
        
        if not message.author.guild_permissions.administrator:
            await message.channel.send("Ops! Apenas administradores podem usar este comando.")
            return
        
        guild = message.guild
        await message.channel.send("Iniciando configuração do seu servidor de Portfólio...")

        try:
            # (Todo o código do !serverportfolio vai aqui, exatamente como estava)
            everyone_role = guild.default_role 
            admin_permissions = discord.Permissions(administrator=True)
            member_permissions = discord.Permissions(
                view_channel=True, send_messages=True, connect=True, speak=True, 
                read_message_history=True, change_nickname=True, use_application_commands=True
            )
            role_dono = await guild.create_role(name="👑 Dono/Dev", color=discord.Color.gold(), permissions=admin_permissions)
            role_bots_portfolio = await guild.create_role(name="🤖 Bots", color=discord.Color.light_grey(), permissions=admin_permissions)
            role_cliente = await guild.create_role(name="🚀 Cliente", color=discord.Color.green(), permissions=member_permissions)
            role_membro = await guild.create_role(name="🫂 Membro", permissions=member_permissions)
            print("Cargos do Portfólio criados.")
            readme_overwrites = {everyone_role: discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True)}
            public_info_overwrites = {everyone_role: discord.PermissionOverwrite(view_channel=False), role_membro: discord.PermissionOverwrite(view_channel=True, send_messages=False), role_cliente: discord.PermissionOverwrite(view_channel=True, send_messages=False)}
            public_chat_overwrites = {everyone_role: discord.PermissionOverwrite(view_channel=False), role_membro: discord.PermissionOverwrite(view_channel=True, send_messages=True), role_cliente: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
            admin_only_overwrites = {everyone_role: discord.PermissionOverwrite(view_channel=False), role_dono: discord.PermissionOverwrite(view_channel=True)}
            
            await message.channel.send("Configurando categorias e canais do Portfólio...")

            cat_bemvindo = await guild.create_category("👋 BEM-VINDO", overwrites=readme_overwrites)
            canal_regras = await guild.create_text_channel("📜-regras-e-boas-vindas", category=cat_bemvindo)
            cat_info = await guild.create_category("🌐 MEUS SERVIÇOS", overwrites=public_info_overwrites)
            canal_servicos = await guild.create_text_channel("💼-serviços-e-pacotes", category=cat_info)
            canal_portfolio = await guild.create_text_channel("✨-portfólio", category=cat_info)
            canal_feedback = await guild.create_text_channel("⭐-feedback-clientes", category=cat_info)
            cat_comunidade = await guild.create_category("💬 COMUNIDADE", overwrites=public_chat_overwrites)
            canal_chat_geral = await guild.create_text_channel("💬-chat-geral", category=cat_comunidade)
            canal_duvidas = await guild.create_text_channel("💡-dúvidas-discord", category=cat_comunidade)
            cat_contrate = await guild.create_category("💰 CONTRATE", overwrites=public_info_overwrites)
            canal_orcamento = await guild.create_text_channel("📝-orçamento-e-contato", category=cat_contrate)
            cat_admin = await guild.create_category("🔒 ADMINISTRAÇÃO", overwrites=admin_only_overwrites)
            await guild.create_text_channel("🔑-comandos-bot", category=cat_admin)
            await guild.create_text_channel("🔒-logs", category=cat_admin)
            print("Canais do Portfólio criados.")

            await canal_regras.send(f"## 👋 Seja Bem-Vindo ao meu Portfólio!\n\n"
                                    f"Olá! Eu sou o **{message.author.mention}**, desenvolvedor deste bot.\n\n"
                                    f"Este servidor serve como meu portfólio profissional para serviços de configuração de servidores no Discord.\n\n"
                                    f"**Regras:**\n"
                                    f"1. Respeito acima de tudo.\n"
                                    f"2. Proibido SPAM ou divulgação sem permissão.\n"
                                    f"3. Use os canais corretos.\n\n"
                                    f"➡️ **Para começar,** dê uma olhada nos meus pacotes em {canal_servicos.mention} e veja meu trabalho em {canal_portfolio.mention}.")
            await canal_servicos.send(f"## 💼 Meus Pacotes de Serviço\n\n"
                                      f"Eu ofereço templates de servidores prontos para uso! Todos os pacotes incluem criação de cargos, canais e configuração completa de permissões.\n\n"
                                      f"**🚀 PACOTE 'LIVE STREAMER' (`!serverlive`)**\n"
                                      f"*Ideal para Streamers e Criadores de Conteúdo.*\n"
                                      f"Inclui: Canais de avisos de live, área de comunidade, canais de voz para jogos e área exclusiva para Subscribers.\n\n"
                                      f"**🛒 PACOTE 'E-COMMERCE' (`!servershop`)**\n"
                                      f"*Ideal para Lojas e Vendas.*\n"
                                      f"Inclui: Canal de vitrine (somente leitura), área de suporte, área privada para Afiliados e área de gestão para CEOs.\n\n"
                                      f"**🍻 PACOTE 'COMUNIDADE' (`!serverresenha`)**\n"
                                      f"*Ideal para servidores de amigos ou comunidades de jogos.*\n"
                                      f"Inclui: Canais de música (com permissões para bots), canais de voz para jogos e canal de AFK automático.\n\n"
                                      f"➡️ **Interessado?** Me chame em {canal_orcamento.mention}!")
            await canal_portfolio.send(f"## ✨ Portfólio em Ação\n\n"
                                       f"**(Aqui você, {message.author.mention}, deve postar os GIFs/vídeos de 30 segundos de cada comando (`!serverlive`, `!servershop`, `!serverresenha`) sendo executado em um servidor vazio!)**")
            await canal_feedback.send(f"## ⭐ Feedback de Clientes\n\n"
                                       f"**(Aqui você, {message.author.mention}, deve postar screenshots de clientes satisfeitos com o seu serviço!)**")
            await canal_orcamento.send(f"## 💰 Orçamento e Contato\n\n"
                                       f"Gostou do que viu? Me chame na **DM (Mensagem Direta)** ({message.author.mention}) para discutir seu projeto!\n\n"
                                       f"*(Dica: Você pode instalar um bot de Ticket neste canal para automatizar o primeiro contato!)*")
            # 8. Imagem do servidor
            try:
                # --- NOME DA IMAGEM ATUALIZADO ---
                with open("DevTM19FotoPerfil.png", "rb") as f: 
                    icon_data = f.read() 
                await guild.edit(icon=icon_data)
                print("Ícone do Portfólio atualizado.")
            
            except FileNotFoundError:
                # --- MENSAGEM DE ERRO ATUALIZADA ---
                print("Aviso: 'DevTM19FotoPerfil.png' não encontrado. Pulei a atualização do ícone.")
                await message.channel.send("Aviso: Não encontrei o arquivo `DevTM19FotoPerfil.png`, pulei a atualização do ícone.")
            except Exception as e:
                print(f"Erro ao atualizar ícone: {e}")
                await message.channel.send(f"Aviso: Ocorreu um erro ao tentar mudar o ícone: {e}")

            await message.channel.send("Configuração do Servidor de Portfólio concluída! As instruções foram postadas nos canais.")
        except Exception as e:
            await message.channel.send(f"Ocorreu um erro durante a configuração do Portfólio: {e}")
            print(f"Erro: {e}")
        return
    # --- FIM DO COMANDO !SERVERPORTFOLIO ---

# O bot agora usa o TOKEN lido do .env
print("Iniciando Bot do Portfólio...")
client.run(TOKEN)