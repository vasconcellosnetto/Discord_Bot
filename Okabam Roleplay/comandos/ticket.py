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
    embed = discord.Embed(title = 'Ticket Okabam Roleplay', description = 'Selecione:\n\nπ - Suporte\n\nβ οΈ - DenΓΊncia\n', color = ctx.author.color)
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'γ€', value = 'Esperamos ajudar!')
    embed.set_footer(text = 'π¦ | Okabam Roleplay')
    my_msg = await ctx.send(embed = embed)
    await my_msg.add_reaction("π")
    await my_msg.add_reaction("β οΈ")      
    await ctx.channel.fetch_message(my_msg.id)  

  @commands.command()
  async def adc(self, ctx, msg_ticket):
    msg = str((ctx.author.name).partition('#')[0]).lower()
    channel = discord.utils.get(ctx.guild.channels, name=f'π«βππππππ-{msg}')
    if channel == ctx.channel:
      member_add = ''
      for user in ctx.guild.members:
        if str(str(user.nick).partition('|')[0]).split() == msg_ticket.split():
          member_add=user
          break
      await ctx.channel.purge(limit = 1) 
      await ctx.channel.set_permissions(member_add, read_messages=True)
      embed_id = discord.Embed(description = f'{member_add.nick} adicionado com sucesso', color = discord.Color.orange())
      embed_id.set_footer(text = 'π¦ | Okabam Roleplay')
      await ctx.send(member_add.mention, embed = embed_id)  

  @commands.command()
  async def rem(self, ctx, msg_ticket):
    msg = str((ctx.author.name).partition('#')[0]).lower()
    channel = discord.utils.get(ctx.guild.channels, name=f'π«βππππππ-{msg}')
    if channel == ctx.channel:
      member_add = ''
      for user in ctx.guild.members:
        if str(str(user.nick).partition('|')[0]).split() == msg_ticket.split():
          member_add=user
          break
      await ctx.channel.purge(limit = 1) 
      await ctx.channel.set_permissions(member_add, read_messages=False)
      embed_id = discord.Embed(description = f'{member_add.nick} removido com sucesso', color = discord.Color.orange())
      embed_id.set_footer(text = 'π¦ | Okabam Roleplay')
      await ctx.send(embed = embed_id)  
  
  @commands.command()
  async def fechar(self, ctx):
    msg = await ctx.channel.history(oldest_first=True, limit=1).flatten()
    for message in msg:
      msg = (str(self.client.get_user(int(message.content[2:-1]))).partition('#')[0]).lower()
      break
    channel = discord.utils.get(ctx.guild.channels, name=f'π«βππππππ-{msg}')
    if channel == ctx.channel:
      await channel.delete()

def setup(client):
  client.add_cog(Ticket(client))