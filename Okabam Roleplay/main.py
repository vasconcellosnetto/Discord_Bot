import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all(), help_command=None)

load_dotenv()

@client.event
async def on_ready():
  print('Bot carregado.')
  await client.change_presence(activity = discord.Game(name = 'Okabam Roleplay'))

@client.command()
@commands.has_role('DIRETOR')
async def load(ctx, extension):
  client.load_extension(f'comandos.{extension}')
  print(f'{extension} carregado.')

@client.command()
@commands.has_role('DIRETOR')
async def unload(ctx, extension):
  client.unload_extension(f'comandos.{extension}')
  print(f'{extension} descarregado.')

@client.command()
@commands.has_role('DIRETOR')
async def reload(ctx, extension):
  client.unload_extension(f'comandos.{extension}')
  client.load_extension(f'comandos.{extension}')
  print(f'{extension} recarregado.')

@client.event
async def on_raw_reaction_add(payload):

  def check_ticket(reaction, user_ticket):
    return (discord.utils.get(guild.roles, name="STAFF") in user_ticket.roles or discord.utils.get(guild.roles, name="SUPORTE") in user_ticket.roles or discord.utils.get(guild.roles, name="DIRETOR") in user_ticket.roles or user == user_ticket) and my_msg == reaction.message
    #return user == user_ticket and my_msg == reaction.message

  def check_report(reaction, user_report):
    return (discord.utils.get(guild.roles, name="STAFF") in user_report.roles or discord.utils.get(guild.roles, name="SUPORTE") in user_report.roles or discord.utils.get(guild.roles, name="DIRETOR") in user_report.roles or user == user_report) and my_msg == reaction.message
    #return user == user_report and my_msg == reaction.message

  channel = await client.fetch_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = await client.fetch_user(payload.user_id)
  guild = client.get_guild(payload.guild_id)
  ticket = discord.utils.get(guild.text_channels, name='❓┃ᴛɪᴄᴋᴇᴛ')

  if user != message.author and channel == ticket:
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, manage_channels=False, add_reactions=False),
        payload.member: discord.PermissionOverwrite(read_messages=True),
        message.author: discord.PermissionOverwrite(read_messages=True)
    } 

    if str(reaction) == "🆘":
      channel_ticket = await guild.create_text_channel(f'🎫│𝚃𝚒𝚌𝚔𝚎𝚝 {user.name}', overwrites = overwrites, category = discord.utils.get(guild.categories, name='Tickets'))
      
      await reaction.remove(payload.member)
      embed = discord.Embed(description = '〽️ Para adicionar outra pessoa no ticket, use o comando !add <id>\n\n〽️ Para remover uma pessoa do ticket, use o comando !rem <id>\n\n〽️ Para finalizar o ticket, clique no ❌ abaixo.', color = discord.Color.orange())
      embed.set_footer(text = '🦅 | Okabam Roleplay')
      my_msg = await channel_ticket.send(user.mention, embed = embed)

      await channel_ticket.set_permissions(discord.utils.get(guild.roles, name="STAFF"), read_message=True)
      await channel_ticket.set_permissions(discord.utils.get(guild.roles,  name="SUPORTE"), read_message=True)
      await my_msg.add_reaction('❌')
      await client.wait_for('reaction_add', check=check_ticket)    
      await client.wait_until_ready()
      await channel_ticket.delete() 

    if str(reaction) == "⚠️":
      repN = len(discord.utils.get(guild.categories, name='Denúncias').channels) + 1

      channel_report = await guild.create_text_channel(f'🛑│𝙳𝚎𝚗𝚞𝚗𝚌𝚒𝚊 n° {repN}', overwrites = overwrites, category = discord.utils.get(guild.categories, name='Denúncias'), sync_permissions=True)
      
      await reaction.remove(payload.member)
      embed = discord.Embed(description = '〽️ Com detalhes, explique o ocorrido/motivo da denúncia.\n\n〽️ Encaminhe todas as provas possíveis do ocorrido. Ao finalizar, clique no ✅ abaixo. ', color = discord.Color.gold())
      embed.set_footer(text = '🦅 | Okabam Roleplay')    
      my_msg = await channel_report.send(user.mention, embed = embed)

      await channel_report.set_permissions(discord.utils.get(guild.roles, name="STAFF"), read_message=True)
      await channel_report.set_permissions(discord.utils.get(guild.roles,  name="SUPORTE"), read_message=True)
      await my_msg.add_reaction('✅')
      await client.wait_for('reaction_add', check=check_report)    
      await client.wait_until_ready()
      await channel_report.set_permissions(payload.member, read_messages=False, send_messages=False)
    
@client.event
async def on_message(message):
  suggestion = discord.utils.get(message.guild.text_channels, name='📝┃sᴜɢᴇsᴛᴏᴇs')

  if message.channel == suggestion and message.author.id != client.user.id:    
    embed = discord.Embed(description = f'ㅤ\n {message.content}\nㅤ', color = discord.Color.teal())
    embed.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')

    if len(message.attachments) > 0:
      embed.set_image(url = message.attachments[0].url)
        
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    msg = await suggestion.send(embed = embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

    await message.delete()

  await client.process_commands(message)

for filename in os.listdir('./comandos'):
  if filename.endswith('.py'):
    client.load_extension(f'comandos.{filename[:-3]}')   

client.run("ODAzNjUyMDk1NTE2ODY4Njg5.YBA5Vg.bwq-ztgtS3qaVGZTSyI_IEhVRlg")