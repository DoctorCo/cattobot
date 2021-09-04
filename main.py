import discord
import os
import json
import random
from gtts import gTTS
import requests

from discord.ext import commands
import asyncio
from replit import db
from keep_alive import keep_alive
import datetime
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from discord.utils import get

from discord.ext import tasks
import aiohttp

#The intents for bot 

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), intents=intents, case_insensitive=True)

#removes the help command

bot.remove_command('help')

#Prints name when ready

@bot.event
async def on_ready():
    print(f"{bot.user} is ready for some pets")
    print("----------------------")
    print(f"ID : {bot.user.id}")
    
async def ch_pr():
  await bot.wait_until_ready()

  statuses = ["hello", "yo"]
  while not bot.is_closed():

    status = random.choice(statuses)
    await bot.change_presence(activity=discord.Game(name=status))
    await asyncio.sleep(69)

#error handling
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    await ctx.reply("There is a missing argument in the command..")
    return

  if isinstance(error,commands.MemberNotFound):
    await ctx.send("I can't find any such member..")
    return


#commands


@bot.command()
async def ping(ctx):
  message = await ctx.send("calculating...")
  await asyncio.sleep(1)
  await message.edit(content=f"{round(bot.latency*1000)} ms is my lattency")

@bot.command(aliases=['av'])
async def avatar(ctx, *, avamember : discord.Member=None):
  if avamember == None:
    avamember = (ctx.author)
  userAvatarUrl = avamember.avatar_url_as(size = 256)
  embed = discord.Embed(title="Avatar")
  embed.set_image(url=f"{userAvatarUrl}")
  embed.set_author(name=f"{avamember.name}#{avamember.discriminator}", icon_url= userAvatarUrl)
  await ctx.send(embed=embed)


#warn dictionary
with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []


#warn command
@bot.command(aliases = ['inform', 'w'] , pass_context = True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'guild': ctx.guild_id,
      'reasons': [reason]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)
    em = discord.Embed(title="Warn",description=f"You have been warned in {ctx.guild.name}")
    em.add_field(name="for:-",value=f"{reason}")
    em.set_thumbnail(url=user.avatar_url)
    await user.send(embed=em)
    await ctx.send(f"{user.name} has been warned!")
    await asyncio.sleep(0.5)
    await ctx.purge(limit=2)

@bot.command(pass_context = True)
async def warnings(ctx, user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"**{user.name} has been reported {len(current_user['reasons'])} times :**\n{','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")  


@bot.command()
async def poll(ctx, *, message):
  """Creates a Poll"""
  author = ctx.message.author
  channel = ctx.message.channel(808042140969205760)
  emb=discord.Embed(title=f"Poll by @{author}", description=F"{message}")
  msg=await channel.send(embed=emb)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')
  await ctx.channel.send(f"Your poll has been added to the {channel.mention} channel")


@bot.command()
async def invites(ctx, member:discord.Member=None):
  if member == None:
    member = ctx.author

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(f"{member.name} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to {ctx.guild.name}")

@bot.command() 
async def clear(ctx, amount=500 ):
  if amount > 500:
    await ctx.send("Cannot purge over 500")
    return
  
  else:
      await ctx.channel.purge(limit=amount)
      await ctx.send(f"cleared {amount}")


@bot.command(description="change status")
async def status(ctx,*,arg):
  await bot.change_presence(activity=discord.Game(name=arg))

@bot.command()
async def dm(ctx, member: discord.Member, *, message : str):
  if member:
    await member.send(f"**{ctx.author.name} :**\n{message}")
    await ctx.send(f"✉️ Sent a DM to **{member}**")
    await asyncio.sleep(0.5)
    await ctx.channel.purge(limit = 2)
  else:
    await ctx.send(f"Could not find any User called **{member}**")


@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="", color=0XEFF9)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=nsfw') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def cute(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/aww/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


keep_alive()
bot.loop.create_task(ch_pr())
bot.run(os.getenv('TOKEN'))
