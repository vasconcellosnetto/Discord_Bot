import discord
import asyncio
import mysql.connector
from discord.ext import commands
from discord.utils import get

class Whitelist(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  #Events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Classe Whitelist carregada.')

  #Commands
  @commands.command()
  @commands.has_any_role('DIRETOR', 'SERVIDOR | DISCORD MASTER')
  async def startwhitelist(self, ctx):
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = 'Inicie sua whitelist com o comando:\n```fix\n!whitelist```', color = ctx.author.color)
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'Boa sorte!')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await ctx.send(embed = embed)    
    await ctx.channel.fetch_message(my_msg.id)

  @commands.command()
  @commands.has_role('🛂 | Passageiro')
  async def whitelist(self, ctx):
    await ctx.channel.purge(limit = 1)
    await self.begin_whitelist(ctx, await self.make_channel(ctx))
    
  @commands.command()
  async def make_channel(self, ctx):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, manage_channels=False, add_reactions=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True)
    }    
    category = discord.utils.get(ctx.guild.categories, name='SERVIDOR | WHITELIST TEAM')
    channel = await guild.create_text_channel(f'📝│𝚆𝚑𝚒𝚝𝚎𝚕𝚒𝚜𝚝 {ctx.message.author.name}', overwrites = overwrites, category = category)
    return channel.id

  @commands.command()
  async def begin_whitelist(self, ctx, channel_id):
    guild = ctx.guild

    def check_channel(message):
      return message.channel == channel
    
    def check_user(reaction, user):
      return ctx.message.author == user

    async def success(answers):    
      await self.client.wait_until_ready()
      success = discord.utils.get(guild.text_channels, name="⚪┃ᴀᴘʀᴏᴠᴀᴅᴏꜱ")
      embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '\n✅ Aprovado ✅', color = discord.Color.green())
      embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')
      embed.add_field(name = 'ㅤ', value = f'O usuário {ctx.message.author.mention}, foi aprovado!')
      embed.set_footer(text = '🦅 | Okabam Roleplay')
      await success.send(embed = embed)

    async def failed():
      await self.client.wait_until_ready()
      failed = discord.utils.get(guild.text_channels, name="✅│𝚁𝚎𝚜𝚞𝚕𝚝𝚊𝚍𝚘")
      embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '🚫 Reprovado 🚫', color = discord.Color.red())
      embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
      embed.add_field(name = 'ㅤ', value = f'O usuário {ctx.message.author.mention} foi reprovado!\n')
      embed.set_footer(text = '🦅 | Okabam Roleplay')
      await failed.send(embed = embed)
    
    await self.client.wait_until_ready()
    channel = self.client.get_channel(channel_id)

    await channel.send(ctx.message.author.mention)

    # Pergunta 1
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#1**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = '```Digite seu ID```\n\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    await channel.send(embed = embed)

    try: 
      await self.client.wait_for('message', timeout=120, check=check_channel)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      id = channel.last_message.content
      user_wl = channel.last_message.author
    except asyncio.TimeoutError:      
      await failed()
      await channel.delete()
      return 
    await channel.purge(limit = 2)   
    # Fim Pergunta 1

    # Pergunta 2
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#2**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = '```Digite o nome completo do seu personagem```\n\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    await channel.send(embed = embed)

    try:
      await self.client.wait_for('message', timeout=120, check=check_channel)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      name = channel.last_message.content
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 2)
    # Fim Pergunta 2

    # Pergunta 3
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#3**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é PowerGaming?\n\n```1️⃣ É fazer no jogo algo que não pode ser feito na vida real.``````2️⃣ É intepretar um fisiculturista super forte.``````3️⃣ É matar um outro jogador utilizando apenas as mãos.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")   
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      answers = 0
      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 3

    # Pergunta 4
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#4**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é MetaGaming?\n\n```1️⃣ É usar poderes igual um mutante.``````2️⃣ É alcançar uma meta enquanto está na cidade.``````3️⃣ É trazer informações de fora do jogo para se beneficiar de alguma forma.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")   
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=1
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 4

    # Pergunta 5
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#5**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é ANTI RP?\n\n```1️⃣ É não seguir a interpretação de personagem conforme as regras e a vida real.``````2️⃣ É interpretar um anti-herói.``````3️⃣ É seguir a interpretação de personagem conforme as regras e a vida real.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")   
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 5

    # Pergunta 6
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#6**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é RP?\n\n```1️⃣ É intepretar um personagem sem seguir parâmetros da vida real.``````2️⃣ É interpretar um personagem seguindo parâmetros da vida real.``````3️⃣ É utilizar dinheiro real para obter benefícios dentro do jogo.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=1
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 6

    # Pergunta 7
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#7**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é Safezone?\n\n```1️⃣ É uma ou mais áreas em que você pode realizar qualquer ação sem riscos.``````2️⃣ É uma ou mais áreas onde ações ilegais são completamente liberadas.``````3️⃣ É uma ou mais áreas onde os jogadores estão seguros contra ações ilegais.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")   
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=1
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 7

    # Pergunta 8
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#8**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é VDM (Vehicle Deathmatch)?\n\n```1️⃣ É matar um jogador utilizando um veículo de forma proposital.``````2️⃣ É matar um jogador utilizando um veículo de forma acidental.``````3️⃣ É fazer uma corrida ilegal até que um dos jogadores morra.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣") 
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 8

    # Pergunta 9
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#9**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é RDM (Random Deathmatch)?\n\n```1️⃣ É jogar roleta-russa dentro da cidade.``````2️⃣ É matar um jogador com um motivo.``````3️⃣ É matar outro jogador sem qualquer motivo.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣") 
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=1
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 9

    # Pergunta 10
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#10**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é amor à vida?\n\n```1️⃣ É uma novela da Rede Globo.``````2️⃣ É sempre zelar pela própria integridade e de outras pessoas.``````3️⃣ É encontrar o amor verdadeiro dentro da cidade.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=1
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 10

    # Pergunta 11
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#11**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é Combat-Logging?\n\n```1️⃣ É desconectar-se durante uma ação para não sofrer consequências.``````2️⃣ É desconectar-se durante uma ação por problemas na internet.``````3️⃣ É analisar todas as ações realizadas em uma ação.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 11

    # Pergunta 12
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#12**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é Revenge Kill?\n\n```1️⃣ É matar alguém.``````2️⃣ É matar alguém por vingança após ter sido finalizado (morto).``````3️⃣ É testemunhar a morte de alguém por vingança.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=1
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 12

    # Pergunta 13
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#13**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é necessário para uma ação de assalto?\n\n```1️⃣ 2 PM em PTR e ser de noite na cidade.``````2️⃣ 2 PM em PTR, 1 SAMU em plantão e ser de noite na cidade.``````3️⃣ Apenas 2 PM em PTR.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 13

    # Pergunta 14
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#14**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'Caso você sofra um acidente e não haja SAMU na cidade, como você procederia?\n\n```1️⃣ Relizaria um chamado para os deuses.``````2️⃣ Aguardaria o tempo acabar e consideraria finalização (morte).``````3️⃣ Aguardar o tempo acabar e não consideraria finalização (morte).```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=1
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 14

    # Pergunta 15
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#15**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'Caso você sofra problemas com limbo, bugs ou similares, como você procederia?\n\n```1️⃣ Relizaria um chamado para os deuses.``````2️⃣ Abusaria dos bugs para benefício próprio.``````3️⃣ Aguardar o tempo acabar e não considerar morte.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=1
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=0
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 15

    # Pergunta 16
    embed = discord.Embed(title = 'Whitelist Okabam Roleplay', description = '_Pergunta_ **#16**', color = discord.Color.orange())
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'O que é finalização?\n\n```1️⃣ A morte do personagem, onde toda a vida é esquecida.``````2️⃣ A morte do personagem, onde o personagem é perdido.``````3️⃣ A morte do personagem, onde os últimos 15 minutos devem ser esquecidos.```\nVocê tem 2 minutos.')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("1️⃣")
    await my_msg.add_reaction("2️⃣")
    await my_msg.add_reaction("3️⃣")    
    await asyncio.sleep(1)

    try:
      await self.client.wait_for('reaction_add', timeout=120, check=check_user)
      await self.client.wait_until_ready()
      channel = self.client.get_channel(channel_id)
      new_msg = await channel.fetch_message(my_msg.id)
      users0 = await new_msg.reactions[0].users().flatten() 
      users1 = await new_msg.reactions[1].users().flatten()
      users2 = await new_msg.reactions[2].users().flatten()

      if len(users0) > 1:
        answers+=0
      elif len(users1) > 1:
        answers+=0
      elif len(users2) > 1:
        answers+=1
    except asyncio.TimeoutError:
      await failed()
      await channel.delete()
      return
    await channel.purge(limit = 1)
    # Fim Pergunta 16

    if answers >= 10:
      await success(answers)
      # Atualizar nome e cargo
      await user_wl.edit(nick=f'{id} | {name}')
      role = discord.utils.get(guild.roles, name='🙋🏼‍♂️ | Morador')
      await user_wl.add_roles(role)
      role = discord.utils.get(guild.roles, name='🛂 | Passageiro')
      await user_wl.remove_roles(role)
      # Fim atualizar nome e cargo

      # Libera na cidade
      conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="zirix"
      )

      crs = conn.cursor()

      sql = f'UPDATE vrp_users SET whitelisted = 1 WHERE id = {id}'
      crs.execute(sql)
      conn.commit()
      #Fim libera na cidade
    '''else:
      await failed()'''

    await channel.delete()

  '''@whitelist.error
  async def whitelist_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      author = ctx.message.author.name
      await ctx.channel.purge(limit = 1)
      time = '{:.0f}'.format(error.retry_after)
      msg = f'```{author}, você pode tentar fazer a whitelist novamente em {int(time)//60} minutos e {int(time)%60} segundos!```'

      await ctx.send(msg)
      await asyncio.sleep(10)
      await ctx.channel.purge(limit = 1)      
    else:
        raise error  '''

def setup(client):
  client.add_cog(Whitelist(client))
