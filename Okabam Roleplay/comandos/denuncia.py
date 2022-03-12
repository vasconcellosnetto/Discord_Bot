import discord
from discord.ext import commands

class Denuncia(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  #Events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Classe Denuncia carregada.')

  #Commands
  @commands.command()
  @commands.has_any_role('DIRETOR')
  async def startreport(self, ctx):
    embed = discord.Embed(title = 'Denúncia Okabam Roleplay', description = 'Inicie sua denúncia reagindo no ⚠️ abaixo!', color = ctx.author.color)
    embed.set_thumbnail(url='https://i.imgur.com/ZnjxFKI.png')  
    embed.add_field(name = 'ㅤ', value = 'Esperamos ajudar!')
    embed.set_footer(text = '🦅 | Okabam Roleplay')
    my_msg = await ctx.send(embed = embed)
    await my_msg.add_reaction("⚠️")    
    await ctx.channel.fetch_message(my_msg.id)

def setup(client):
  client.add_cog(Denuncia(client))