import discord
from discord.ext import commands

class Ticket(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  #Events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Classe Ticket carregada.')

  #Commands
  @commands.command()
  @commands.has_any_role('DIRETOR', 'SERVIDOR | DISCORD MASTER')
  async def startticket(self, ctx):
    embed = discord.Embed(title = 'Ticket Okabam Roleplay', description = 'Selecione:\n\n🆘 - Suporte\n\n⚠️ - Denúncia\n\n💰 - Vendas', color = ctx.author.color)
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'Esperamos ajudar!')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await ctx.send(embed = embed)
    await my_msg.add_reaction("🆘")
    await my_msg.add_reaction("⚠️")     
    await ctx.channel.fetch_message(my_msg.id)  

  @commands.command()
  async def add(self, ctx, msg_ticket):
    def check_channel_ticket(message):
      msg = str((message.author.name).partition('#')[0]).lower()
      channel = discord.utils.get(ctx.guild.channels, name=f'🎫│𝚃𝚒𝚌𝚔𝚎𝚝-{msg}')            
      return message.channel == channel
    
    msg = str((ctx.author.name).partition('#')[0]).lower()
    channel = discord.utils.get(ctx.guild.channels, name=f'🎫│𝚃𝚒𝚌𝚔𝚎𝚝-{msg}')
    if channel == ctx.channel:
      member_add = ''
      for user in ctx.guild.members:
        if str(str(user.nick).partition('|')[0]).split() == msg_ticket.split():
          member_add=user
          break
      await ctx.channel.purge(limit = 1) 
      await ctx.channel.set_permissions(member_add, read_messages=True)
      embed_id = discord.Embed(description = f'{member_add.nick} adicionado com sucesso', color = discord.Color.orange())
      embed_id.set_footer(text = '🦅 | Okabam Roleplay')
      await ctx.send(member_add.mention, embed = embed_id)  

  @commands.command()
  async def rem(self, ctx, msg_ticket):
    def check_channel_ticket(message):
      msg = str((message.author.name).partition('#')[0]).lower()
      channel = discord.utils.get(ctx.guild.channels, name=f'🎫│𝚃𝚒𝚌𝚔𝚎𝚝-{msg}')            
      return message.channel == channel
    
    msg = str((ctx.author.name).partition('#')[0]).lower()
    channel = discord.utils.get(ctx.guild.channels, name=f'🎫│𝚃𝚒𝚌𝚔𝚎𝚝-{msg}')
    if channel == ctx.channel:
      member_add = ''
      for user in ctx.guild.members:
        if str(str(user.nick).partition('|')[0]).split() == msg_ticket.split():
          member_add=user
          break
      await ctx.channel.purge(limit = 1) 
      await ctx.channel.set_permissions(member_add, read_messages=False)
      embed_id = discord.Embed(description = f'{member_add.nick} removido com sucesso', color = discord.Color.orange())
      embed_id.set_footer(text = '🦅 | Okabam Roleplay')
      await ctx.send(embed = embed_id)   

def setup(client):
  client.add_cog(Ticket(client))