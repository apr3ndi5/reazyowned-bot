import discord
import secreto
import asyncio

client = discord.Client()

players = {}
COR = 0x690FC3
roxo = 0x690FC3
token = secreto.seu_token()
msg_id = None
msg_user = None


@client.event
async def on_ready():
    print('BOT ONLINE!')
    print(client.user.name)
    print(client.user.id)
    print('################')


@client.event

async def on_message(message):
    if message.content.lower().startswith(";verificar"):
     embed1 = discord.Embed(
        title="Verificar",
        color=roxo,
        description="Selecione o emoji para verificar!\nhttp://reazyowned.com/")

    botmsg = await client.send_message(message.channel, embed=embed1)

    await client.add_reaction(botmsg, "✅")


    global msg_id
    msg_id = botmsg.id

    global msg_user
    msg_user = message.author


@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message

    if reaction.emoji == "✅" and msg.id == msg_id: #and user == msg_user:
     role = discord.utils.find(lambda r: r.name == "Verificado", msg.server.roles)
     await client.add_roles(user, role)
     print("add")

@client.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message

@client.event
async  def on_member_join(member):
  canal = client.get_channel("493652449647656976")
  regras = client.get_channel("493652449647656976")
  msg = "Bem Vindo ao ReazyOwned {} leia as {}\nentre no forum http://reazyowned.com/".format(member.mention,regras.mention)
  await  client.send_message(member, msg)

@client.event
async def on_member_remove(member):
  canal = client.get_channel("493652449647656976")
  msg = "Adeus à ReazyOwned {}".format(member.mention)
  await  client.send_message(member, msg)

@client.event
async def on_message(message):
    if message.content.startswith(';entrar'):
        try:
            channel = message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            await client.send_message(message.channel, "O bot ja esta em um canal de voz")
        except Exception as error:
            await client.send_message(message.channel, "Ein Error: ```{error}```".format(error=error))

    if message.content.startswith(';sair'):
        try:
            mscleave = discord.Embed(
                title="\n",
                color=COR,
                description="Sai do canal de voz e a musica parou!"
            )
            voice_client = client.voice_client_in(message.server)
            await client.send_message(message.channel, embed=mscleave)
            await voice_client.disconnect()
        except AttributeError:
            await client.send_message(message.channel, "O bot não esta em nenhum canal de voz.")
        except Exception as Hugo:
            await client.send_message(message.channel, "Ein Error: ```{haus}```".format(haus=Hugo))

    if message.content.startswith(';play'):
        try:
            yt_url = message.content[6:]
            if client.is_voice_connected(message.server):
                try:
                    voice = client.voice_client_in(message.server)
                    players[message.server.id].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=COR
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb)
                except Exception as e:
                    await client.send_message(message.server, "Error: [{error}]".format(error=e))

            if not client.is_voice_connected(message.server):
                try:
                    channel = message.author.voice.voice_channel
                    voice = await client.join_voice_channel(channel)
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb2 = discord.Embed(
                        title="Música para tocar:",
                        color=COR
                    )
                    mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb2)
                except Exception as error:
                    await client.send_message(message.channel, "Error: [{error}]".format(error=error))
        except Exception as e:
            await client.send_message(message.channel, "Error: [{error}]".format(error=e))

    if message.content.startswith(';pause'):
        try:
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
            players[message.server.id].pause()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))
    if message.content.startswith(';resume'):
        try:
            mscresume = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscresume)
            players[message.server.id].resume()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))


client.run(token)