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

    # Comando !ajuda (para listar comandos)
    if message.content.startswith('!ajuda'):
        # --- ATUALIZADO AQUI ---
        await message.channel.send("Esses são os comandos que tenho até o momento: !oi, !serverlive, !servershop, !serverresenha, !Developer")
        return # Adiciona um 'return' para ele parar aqui

    # Comando !Developer (para mostrar o desenvolvedor do bot)
    if message.content.startswith('!Developer'):
        await message.channel.send("Desenvolvido por: Matheus B \n"
                                   "discord: https://discord.gg/DDHNZBGM8k \n"
                                   "Instagram: @matheus_b_dev \n")
        return 

    # Comando !oi (o que você já tinha)
    if message.content.startswith('!oi'):
        await message.channel.send('Olá!')
        return # Adiciona um 'return' para ele parar aqui

    # --- NOVO COMANDO !SERVERRESENHA ---
    if message.content.startswith('!serverresenha'):
        
        # 1. Verifica se quem digitou o comando é um Admin
        if not message.author.guild_permissions.administrator:
            await message.channel.send("Ops! Apenas administradores podem usar este comando.")
            return
        
        # 2. Se for Admin, continua. 'guild' é o servidor.
        guild = message.guild
        await message.channel.send("Iniciando configuração de cargos e permissões para Servidor de Resenhas...")

        try:
            # Pega o cargo @everyone para podermos restringi-lo
            everyone_role = guild.default_role 

            # 3. Criar os "Modelos" de Permissão para os CARGOS
            admin_permissions = discord.Permissions(administrator=True)
            
            # Permissões de Membro (com permissão para música e stream)
            member_permissions = discord.Permissions(
                view_channel=True,
                send_messages=True,
                connect=True,
                speak=True,
                read_message_history=True,
                change_nickname=True,
                stream=True, # <-- Essencial para "Assistindo Algo"
                use_application_commands=True # <-- Essencial para bots de música
            )

            # 4. Criar os Cargos (Roles) com essas permissões
            role_soberano = await guild.create_role(name="👑Soberano", color=discord.Color.gold(), permissions=admin_permissions)
            role_moderacao = await guild.create_role(name="🛠️Moderação", color=discord.Color.red(), permissions=admin_permissions)
            role_bots = await guild.create_role(name="🤖Bots", color=discord.Color.light_grey(), permissions=admin_permissions)
            
            role_fiel = await guild.create_role(name="⭐O Fiel", color=discord.Color.blue(), permissions=member_permissions)
            role_membro = await guild.create_role(name="🫂Membro", permissions=member_permissions)
            print("Cargos de Amigos criados.")

            # 5. Criar as "Regras de Visibilidade" para as CATEGORIAS
            friends_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                role_membro: discord.PermissionOverwrite(view_channel=True),
                role_fiel: discord.PermissionOverwrite(view_channel=True)
            }
            
            await message.channel.send("Configurando categorias e canais de Lazer...")

            # 6. Criar as Categorias e Canais
            # INFORMAÇÕES
            cat_info = await guild.create_category("📣 INFORMAÇÕES", overwrites=friends_overwrites)
            await guild.create_text_channel("👋regras-e-avisos", category=cat_info)

            # CONVERSA
            cat_conversa = await guild.create_category("💬 CONVERSA", overwrites=friends_overwrites)
            await guild.create_text_channel("💬geral", category=cat_conversa)
            await guild.create_text_channel("📸midias-e-memes", category=cat_conversa)
            await guild.create_voice_channel("🔊 Sala de Espera", category=cat_conversa)

            # MÚSICA & CHILL
            cat_musica = await guild.create_category("🎧 MÚSICA & CHILL", overwrites=friends_overwrites)
            await guild.create_text_channel("comandos-do-bot", category=cat_musica)
            await guild.create_voice_channel("🎶 Rádio (Música)", category=cat_musica)
            await guild.create_voice_channel("🎬 Assistindo Algo", category=cat_musica)

            # JOGATINA
            cat_jogatina = await guild.create_category("🎮 JOGATINA", overwrites=friends_overwrites)
            await guild.create_voice_channel("🕹️ Jogo 1", category=cat_jogatina)
            await guild.create_voice_channel("🕹️ Jogo 2", category=cat_jogatina)
            await guild.create_voice_channel("🕹️ Jogo 3 (Ocioso)", category=cat_jogatina)

            # AFK
            cat_afk = await guild.create_category("😴 AFK", overwrites=friends_overwrites)
            afk_channel = await guild.create_voice_channel("💤 Ausente", category=cat_afk)
            print("Canais de Amigos criados.")

            # 7. Configurar Canal AFK
            await guild.edit(afk_channel=afk_channel, afk_timeout=300) # 300 segundos = 5 min
            print(f"Canal AFK definido como '{afk_channel.name}' com 5 min de timeout.")
            
            # 8. Imagem do servidor
            # --- BLOCO CORRIGIDO ---
            try:
                with open("ServerResenhaFotoPerfil.png", "rb") as f: 
                    icon_data = f.read() 
                await guild.edit(icon=icon_data)
                print("Ícone da Resenha atualizado.") # <-- Mensagem corrigida
            
            except FileNotFoundError: # <-- Erro específico adicionado
                print("Aviso: 'ServerResenhaFotoPerfil.png' não encontrado.")
                await message.channel.send("Aviso: Não encontrei o arquivo `ServerResenhaFotoPerfil.png`, pulei a atualização do ícone.")
            except Exception as e: # <-- Erro genérico mantido
                print(f"Erro ao atualizar ícone: {e}")
                await message.channel.send(f"Aviso: Ocorreu um erro ao tentar mudar o ícone: {e}")
            # --- FIM DA CORREÇÃO ---

            # 9. Finaliza a configuração
            await message.channel.send("Configuração de Servidor de Amigos concluída!")

        except Exception as e:
            await message.channel.send(f"Ocorreu um erro durante a configuração: {e}")
            print(f"Erro: {e}")
            
        return # <-- Adiciona o return para finalizar o comando
    # --- FIM DO COMANDO !SERVERRESENHA ---

    # --- COMANDO !SERVERSHOP (EXISTENTE) ---
    if message.content.startswith('!servershop'):
        
        # 1. Verifica se quem digitou o comando é um Admin
        if not message.author.guild_permissions.administrator:
            await message.channel.send("Ops! Apenas administradores podem usar este comando.")
            return
        
        # 2. Se for Admin, continua. 'guild' é o servidor.
        guild = message.guild
        await message.channel.send("Iniciando configuração de cargos e permissões para Shop...")

        try:
            # Pega o cargo @everyone para podermos restringi-lo
            everyone_role = guild.default_role 

            # 3. Criar os "Modelos" de Permissão para os CARGOS
            admin_permissions = discord.Permissions(administrator=True)
            member_permissions = discord.Permissions(
                view_channel=True,
                send_messages=True,
                connect=True,
                speak=True,
                read_message_history=True,
                change_nickname=True
            )
            
            # Permissão especial para 'vitrine' (só leitura)
            readonly_permissions = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False, # <-- A CHAVE! Clientes não podem digitar
                read_message_history=True
            )

            # 4. Criar os Cargos (Roles) com essas permissões
            role_ceo = await guild.create_role(name="👑CEO", color=discord.Color.purple(), permissions=admin_permissions)
            role_bots_shop = await guild.create_role(name="🤖Bots", color=discord.Color.light_grey(), permissions=admin_permissions)
            role_afiliado = await guild.create_role(name="🔗Afiliado", color=discord.Color.orange(), permissions=member_permissions)
            role_cliente = await guild.create_role(name="🫂Cliente/Membro", permissions=member_permissions)
            print("Cargos da Shop criados.")

            # 5. Criar as "Regras de Visibilidade" para as CATEGORIAS
            
            # Regra para INFO e COMUNIDADE (visível para Clientes e Afiliados)
            public_shop_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                role_cliente: discord.PermissionOverwrite(view_channel=True),
                role_afiliado: discord.PermissionOverwrite(view_channel=True)
            }
            
            # Regra para VITRINE (read-only para Clientes, write para Afiliados/CEO)
            vitrine_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                role_cliente: readonly_permissions, # <-- Aplica a regra de "só leitura"
                role_afiliado: discord.PermissionOverwrite(view_channel=True), # Afiliados podem postar
                role_ceo: discord.PermissionOverwrite(view_channel=True) # CEOs podem postar
            }

            # Regra para AFILIADOS (visível SÓ para Afiliados)
            afiliado_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                role_cliente: discord.PermissionOverwrite(view_channel=False),
                role_afiliado: discord.PermissionOverwrite(view_channel=True)
            }

            # Regra para CEOs (visível SÓ para CEOs)
            ceo_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False),
                role_cliente: discord.PermissionOverwrite(view_channel=False),
                role_afiliado: discord.PermissionOverwrite(view_channel=False),
                role_ceo: discord.PermissionOverwrite(view_channel=True)
            }
            
            await message.channel.send("Configurando categorias e canais da Shop...")

            # 6. Criar as Categorias com as Regras de Visibilidade
            cat_info = await guild.create_category("🌐 INFO & REGRAS", overwrites=public_shop_overwrites)
            cat_vitrine = await guild.create_category("🛒 VITRINE DE PRODUTOS", overwrites=vitrine_overwrites)
            cat_comunidade = await guild.create_category("💬 COMUNIDADE & SUPORTE", overwrites=public_shop_overwrites)
            cat_afiliados = await guild.create_category("🔗 ÁREA AFILIADOS", overwrites=afiliado_overwrites)
            cat_gestao = await guild.create_category("🏢 GESTÃO EXCLUSIVA", overwrites=ceo_overwrites)
            print("Categorias da Shop criadas.")

            # 7. Criar os Canais de Texto (herdam as permissões da categoria)
            # Categoria: INFO
            await guild.create_text_channel("👋boas-vindas", category=cat_info)
            await guild.create_text_channel("📄regras-e-faq", category=cat_info)

            # Categoria: VITRINE (herda read-only para clientes)
            await guild.create_text_channel("📸produtos-e-preços", category=cat_vitrine)
            await guild.create_text_channel("✨novidades", category=cat_vitrine)
            
            # Categoria: COMUNIDADE
            await guild.create_text_channel("💬chat-geral", category=cat_comunidade)
            await guild.create_text_channel("🆘suporte-e-ajuda", category=cat_comunidade)

            # Categoria: AFILIADOS
            await guild.create_text_channel("📢avisos-afiliados", category=cat_afiliados)
            await guild.create_text_channel("📊relatórios-e-metas", category=cat_afiliados)
            await guild.create_text_channel("💡novas-ideias", category=cat_afiliados)
            
            # Categoria: GESTÃO
            await guild.create_text_channel("🔒ceo-lounge", category=cat_gestao)
            print("Canais da Shop criados.")

            # 8. Imagem do servidor (usando o novo arquivo)
            try:
                # --- USA A NOVA FOTO ---
                with open("ServerShopFotoPerfil.png", "rb") as f: 
                    icon_data = f.read() 
                await guild.edit(icon=icon_data)
                print("Ícone da Shop atualizado.")
            
            except FileNotFoundError:
                print("Aviso: 'ServerShopFotoPerfil.png' não encontrado.")
                await message.channel.send("Aviso: Não encontrei o arquivo `ServerShopFotoPerfil.png`, pulei a atualização do ícone.")
            except Exception as e:
                print(f"Erro ao atualizar ícone: {e}")
                await message.channel.send(f"Aviso: Ocorreu um erro ao tentar mudar o ícone: {e}")

            # 9. Finaliza a configuração
            await message.channel.send("Configuração da Shop concluída! Servidor pronto para vendas!")
        
        except Exception as e:
            await message.channel.send(f"Ocorreu um erro durante a configuração da Shop: {e}")
            print(f"Erro: {e}")
            
        return # <-- Adiciona o return para finalizar o comando

    # --- FIM DO COMANDO !SERVERSHOP ---


    # --- COMANDO !SERVERLIVE (EXISTENTE) ---
    if message.content.startswith('!serverlive'):
        
        # 1. Verifica se quem digitou o comando é um Admin
        if not message.author.guild_permissions.administrator:
            await message.channel.send("Ops! Apenas administradores podem usar este comando.")
            return

        # 2. Se for Admin, continua. 'guild' é o servidor.
        guild = message.guild
        await message.channel.send("Iniciando configuração de cargos e permissões...")

        try:
            # Pega o cargo @everyone para podermos restringi-lo
            everyone_role = guild.default_role 

            # 3. Criar os "Modelos" de Permissão para os CARGOS
            
            # Permissão de Administrador (para Staff, Streamer, Bots)
            admin_permissions = discord.Permissions(administrator=True)

            # Permissões de Membro (ver canais, enviar msgs, conectar/falar em voz)
            member_permissions = discord.Permissions(
                view_channel=True,
                send_messages=True,
                connect=True,
                speak=True,
                read_message_history=True,
                change_nickname=True # Um bônus útil
            )

            # 4. Criar os Cargos (Roles) com essas permissões
            
            streamer = await guild.create_role(name="👑Streamer👑", color=discord.Color.red(), permissions=admin_permissions)
            staff = await guild.create_role(name="🛡️Staff🛡️", color=discord.Color.orange(), permissions=admin_permissions)
            bots = await guild.create_role(name="🤖Bots🤖", color=discord.Color.light_grey(), permissions=admin_permissions)
            print("Cargos de Admin criados.")

            role_subs = await guild.create_role(name="💎Subscribers💎", color=discord.Color.purple(), permissions=member_permissions)
            membros = await guild.create_role(name="🌟Membros🌟", color=discord.Color.yellow(), permissions=member_permissions)
            print("Cargos de Membro criados.")

            # 5. Criar as "Regras de Visibilidade" para as CATEGORIAS
            
            # Regra para categorias PÚBLICAS (visível para Membros e Subs)
            public_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False), # @everyone NÃO VÊ
                membros: discord.PermissionOverwrite(view_channel=True),        # Membros VÊEM
                role_subs: discord.PermissionOverwrite(view_channel=True)       # Subs VÊEM
            }

            # Regra para categorias DE SUBS (visível SÓ para Subs)
            sub_only_overwrites = {
                everyone_role: discord.PermissionOverwrite(view_channel=False), # @everyone NÃO VÊ
                membros: discord.PermissionOverwrite(view_channel=False),       # Membros NÃO VÊEM
                role_subs: discord.PermissionOverwrite(view_channel=True)       # Subs VÊEM
            }
            
            await message.channel.send("Configurando categorias e canais (isso pode levar um momento)...")

            # 6. Criar as Categorias com as Regras de Visibilidade
            
            infoserver = await guild.create_category("📢 INFORMAÇÕES DO SERVIDO", overwrites=public_overwrites)
            aovivo = await guild.create_category("🔴 AO VIVO", overwrites=public_overwrites)
            comunidade = await guild.create_category("🌐 COMUNIDADE", overwrites=public_overwrites)
            conteudo = await guild.create_category("🎬 CONTEÚDO", overwrites=public_overwrites)
            categoria_subs = await guild.create_category("💎 SUBSCRIBERS", overwrites=sub_only_overwrites)
            print("Categorias e permissões de canal aplicadas.")

            # 7. Criar os Canais de Texto (eles vão HERDAR as permissões da categoria)
            # Categoria: INFORMAÇÕES DO SERVIDOR
            await guild.create_text_channel("👋boas-vindas", category=infoserver)
            await guild.create_text_channel("📋regras-e-info", category=infoserver)
            await guild.create_text_channel("🚨avisos-do-servidor", category=infoserver)
            print("Canais de Informação criados.")

            # Categoria: AO VIVO
            await guild.create_text_channel("🔔avisos-da-live", category=aovivo)
            print("Canais Ao Vivo criados.")

            # Categoria: COMUNIDADE
            await guild.create_text_channel("💬chat-geral", category=comunidade)
            await guild.create_text_channel("😂memes-e-humor", category=comunidade)
            await guild.create_text_channel("💡sugestões-e-ideias", category=comunidade)
            print("Canais da Comunidade criados.")

            # Categoria: CONTEÚDO
            await guild.create_text_channel("✂clips-da-live", category=conteudo)
            await guild.create_text_channel("📸fanarts-e-criações", category=conteudo)
            print("Canais de Conteúdo criados.")

            # Categoria: SUBSCRIBERS
            await guild.create_text_channel("👑chat-subs", category=categoria_subs)
            await guild.create_text_channel("🥳eventos-subs", category=categoria_subs)
            print("Canais de Subs criados.")

            # 8. Criar os Canais de Voz (também herdam as permissões)
            # Categoria voz: AO VIVO
            await guild.create_voice_channel("🔊 Em Live", category=aovivo)

            # Categoria voz: COMUNIDADE
            await guild.create_voice_channel("🔊 Bate-Papo", category=comunidade)
            await guild.create_voice_channel("🔊 Jogando com a galera", category=comunidade)

            # Categoria voz: SUBSCRIBERS
            await guild.create_voice_channel("🔊 Call Exclusiva", category=categoria_subs)
            print("Canais de Voz criados.")
            
            # 9. Imagem do servidor
            try:
                # --- USA A FOTO DE LIVE ---
                with open("ServerLiveFotoPerfil.png", "rb") as f:
                    icon_data = f.read() 
                await guild.edit(icon=icon_data)
                print("Ícone do servidor atualizado.")
            
            except FileNotFoundError:
                print("Aviso: 'ServerLiveFotoPerfil.png' não encontrado. Ícone não atualizado.")
                await message.channel.send("Aviso: Não encontrei o arquivo `ServerLiveFotoPerfil.png`, pulei a atualização do ícone do servidor.")
            except Exception as e:
                print(f"Erro ao atualizar ícone: {e}")
                await message.channel.send(f"Aviso: Ocorreu um erro ao tentar mudar o ícone do servidor: {e}")

            # 10. Finaliza a configuração
            await message.channel.send("Configuração concluída! Servidor pronto para uso!")

        except Exception as e:
            await message.channel.send(f"Ocorreu um erro durante a configuração do ServerLive: {e}")
            print(f"Erro: {e}")
            
        return # <-- CORREÇÃO: Adicionado o return aqui

# O bot agora usa o TOKEN lido do .env
client.run(TOKEN)