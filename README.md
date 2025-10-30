# Build-Server
Projeto de bot Discord 3-em-1. main.py é o produto: cria templates de servidor (!serverlive, !servershop, !serverresenha). minhamain.py é o portfólio: usa !serverportfolio para criar um servidor para o dev anunciar e vender esses templates.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Projeto: Bot de Templates de Servidor Discord
Este projeto é uma solução "dois em um" para um desenvolvedor (neste caso, Matheus B) que deseja vender serviços de configuração de servidores Discord.

Ele é composto por dois bots independentes:

main.py (O Bot "Produto"): Este é o bot principal que contém a lógica para criar três tipos de servidores-modelo (Live, Shop, Resenha). Este é o bot que o desenvolvedor usaria no servidor de um cliente para configurá-lo instantaneamente.

minhamain.py (O Bot "Portfólio"): Este bot é usado para configurar o próprio servidor do desenvolvedor. Ele cria um servidor de portfólio completo, com canais para descrever os pacotes (!serverlive, !servershop, etc.), feedbacks e informações de contato.

Bots Explicados
1. main.py (Bot Produto)
Este bot foi projetado para ser convidado para um servidor (idealmente um servidor novo e vazio) e configurá-lo de acordo com um template pré-definido.

Comandos:

!ajuda: Lista todos os comandos de criação de servidor.

!Developer: Exibe as informações do criador (Matheus B).

!oi: Um comando simples de "Olá".

!serverlive: (Admin) Cria uma estrutura completa de servidor para Streamers, incluindo cargos (Streamer, Staff, Subs, Membros), categorias (Info, Ao Vivo, Comunidade, Conteúdo) e canais exclusivos para Subscribers.

!servershop: (Admin) Cria uma estrutura completa de servidor para E-commerce/Lojas, incluindo cargos (CEO, Afiliado, Cliente), categorias (Info, Vitrine, Comunidade, Afiliados, Gestão) e canais com permissões de "somente leitura" para clientes na vitrine.

!serverresenha: (Admin) Cria uma estrutura completa de servidor para Comunidades/Amigos, incluindo cargos (Soberano, Moderação, Fiel, Membro), categorias (Info, Conversa, Música & Chill, Jogatina) e um canal AFK automático.

2. minhamain.py (Bot Portfólio)
Este bot foi projetado para ser executado uma vez no próprio servidor do desenvolvedor para construir sua "loja" ou "portfólio" de serviços.

Comandos:

!ajuda: Lista os comandos específicos do portfólio.

!Developer: Exibe as informações do criador.

!oi: Um comando simples de "Olá".

!serverportfolio: (Admin) O comando principal. Ele cria toda a estrutura do servidor de portfólio, incluindo:

Cargos (Dono/Dev, Cliente, Membro).

Categorias (Bem-Vindo, Meus Serviços, Comunidade, Contrate, Admin).

Canais de texto que já vêm com mensagens postadas explicando os pacotes (que são os comandos do main.py), como contratar e onde ver o portfólio.

🚀 Como Usar o Projeto
Siga estes passos para configurar e executar qualquer um dos bots.

1. Pré-requisitos
Python 3.8 ou superior

Uma conta no Discord e um servidor onde você tenha permissões de Administrador.

2. Instalação
Clone ou baixe este repositório.

Crie um Bot no Portal de Desenvolvedores do Discord:

Vá para o Portal de Desenvolvedores do Discord.

Crie uma "Nova Aplicação".

Vá para a aba "Bot".

Clique em "Add Bot".

Em "Privileged Gateway Intents", ative MESSAGE CONTENT INTENT e SERVER MEMBERS INTENT (embora guilds já esteja no código, message_content é a mais essencial para ler comandos).

Clique em "Reset Token" e copie o seu token. Não compartilhe este token com ninguém.

Crie um arquivo .env: Na mesma pasta dos arquivos .py, crie um arquivo chamado .env (exatamente assim) e adicione seu token:

DISCORD_TOKEN=SEU_TOKEN_SECRETO_DO_BOT_VAI_AQUI
Instale as dependências: Você precisará das bibliotecas discord.py e python-dotenv.

Bash

pip install discord.py python-dotenv
Adicione as Imagens: Os bots tentam definir o ícone do servidor após a execução. Para funcionar, você precisa ter os seguintes arquivos de imagem na mesma pasta que os scripts:

Para main.py:

ServerLiveFotoPerfil.png

ServerShopFotoPerfil.png

ServerResenhaFotoPerfil.png

Para minhamain.py:

DevTM19FotoPerfil.png

Convide seu Bot:

No Portal de Desenvolvedores, vá para "OAuth2" -> "URL Generator".

Selecione bot e applications.commands.

Em "Bot Permissions", marque Administrator. Isso é essencial, pois os bots precisam criar cargos, canais e gerenciar permissões.

Copie a URL gerada, cole no seu navegador e adicione o bot ao seu servidor de testes.

3. Executando o Bot
Você só pode executar um arquivo de cada vez, pois eles competirão pelo mesmo token se executados juntos.

Para executar o Bot "Produto":

Bash

python main.py
Para executar o Bot "Portfólio":

Bash

python minhamain.py
4. Testando
Depois de executar o script, você verá uma mensagem no seu terminal, como Logamos como SeuBot#1234.

Vá para qualquer canal de texto no servidor onde o bot está.

Digite o comando que deseja testar (ex: !ajuda ou !serverportfolio).

Importante: Os comandos de criação de servidor (!serverlive, !servershop, !serverresenha, !serverportfolio) só podem ser executados por um Administrador do servidor.
