# modules used:
# os, discord, 
#discord.ext, json
#random, itertools, cycle
# asyncio, sys, keep_alive
import os
import discord
from discord.ext import commands
import json
import random
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
import keep_alive

client = commands.Bot(command_prefix = "cs" , activity = discord.Game(name="cshelp for help"))
status = cycle(['Bot is online'])
client.remove_command('help')


@client.event
async def onready(ctx):

  print("The cricket stars bot#1749 is online. Bot id is: 921233592443625524")



@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def commandcount(ctx):
  await open_account(ctx.author)
  user = ctx.author

  users = await get_bank_data()
  count = users[str(user.id)]["count"]
  em = discord.Embed(title=f"{ctx.author.name}'s command count",
                       color=discord.Color.orange())
  em.add_field(name="Command Count", value=count)
  await ctx.send(embed=em)

@commandcount.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Take a breather bro....",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=16776960)
        await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def bal(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    em = discord.Embed(title=f"{ctx.author.name}'s balance",
                       color=discord.Color.orange())
    em.add_field(name="Wallet balance", value=wallet_amt)
    em.add_field(name="Bank balance", value=bank_amt)
    users[str(user.id)]["xp"] += 1
    users[str(user.id)]["count"] += 1
    await ctx.send(embed=em)
    
@bal.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Take a breather bro....",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=16776960)
        await ctx.send(embed=em)


@client.command()
async def kick(ctx, member:discord.Member, * , reason):
    await member.kick(reason = reason)
    kickembed = discord.Embed(title=f"{member.name}#{member.discriminator}has been kicked. By {ctx.message.author}")
    kickembed.set_footer(text=f'Reason:{reason}')
    await ctx.send(embed=kickembed)
    await member.send(embed = discord.Embed(title=f"{member.name}{member.discriminator} has been banned by {ctx.message.author}"))


@client.command()
async def ban(ctx, member:discord.Member, *, reason):
  await member.ban(reason=reason)
  banembed = discord.Embed(title=f"{member.name}#{member.discriminator} has been banned by {ctx.message.author}")
  banembed.set_footer(text=f'Reason:{reason}')
  await ctx.send(embed=banembed)
  await member.send(embed = discord.Embed(title=f"{member.name}{member.discriminator} has been banned by {ctx.message.author}"))


@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans() 
  member_name, member_discriminator = member.split('#')
  for ban_entry in banned_users:
    user = ban_entry.user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user) 
      await ctx.send(f"Successfully unbanned {user.mention}")
      return

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change

    with open("economy.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)  #This is a cooldown
async def gamble(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    earnings = random.randrange(-5000, 5000)
    if earnings < 0:
        embedVar = discord.Embed(
            title=f"You lost {earnings}",
            description="lol, YOU LOST MONEY **Get Good**",
            color=0x00ff00)
    else:
        embedVar = discord.Embed(title=f"You earned {earnings}",
                                 description="So lucky, **you WON MONEY**",
                                 color=0x00ff00)
    users[str(user.id)]["wallet"] += earnings
    await ctx.send(embed=embedVar)
    users[str(user.id)]["xp"] += 1
    users[str(user.id)]["count"] += 1
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return users


@gamble.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(
            title=f"Spam Isn't cool Fam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=71)
        await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)  #This is a cooldown
async def fact(ctx):
    facts = random.choice(fun_facts)

    embedVar = discord.Embed(
        title=f"Here You Go, now learn something which u dont know",
        description=facts,
        color=100)
    await ctx.send(embed=embedVar)


@fact.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Spam Isn't cool Fam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=65535)
        await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    workEarnings = random.randrange(100, 5000)
    embedVar = discord.Embed(
        title="You have worked",
        description=f'You have earned {workEarnings} from working',
        color=100)
    await ctx.send(embed=embedVar)
    users[str(user.id)]["wallet"] += workEarnings
    users[str(user.id)]["xp"] += 1
    users[str(user.id)]["count"] += 1
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return users


@work.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Hold your Horses.....",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=65439)
        await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    dailyEarnings = 5000
    embedVar = discord.Embed(
        title="You have earned your daily prize",
        description=
        f'You have earned {dailyEarnings} as a daily reward, now get lost , **DAB**',
        color=100)
    await ctx.send(embed=embedVar)
    users[str(user.id)]["wallet"] += dailyEarnings
    users[str(user.id)]["xp"] += 7
    users[str(user.id)]["count"] += 1
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return users


@daily.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Spam isnt cool. It leads to ban",
            description=
            f"Try again in {error.retry_after:.2f}s.  Now since u know when to get ur money, get lost **DAB**",
            color=65439)
        await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 2592000, commands.BucketType.user)
async def monthly(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    monthlyEarnings = 150000
    embedVar = discord.Embed(
        title="You have earned your monthly prize",
        description=
        f'You have earned {monthlyEarnings} as a monthly reward, now get lost , **DAB**',
        color=100)
    await ctx.send(embed=embedVar)
    users[str(user.id)]["wallet"] += monthlyEarnings
    users[str(user.id)]["xp"] += 7
    users[str(user.id)]["count"] += 1
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return users


@monthly.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Come back after a month bruhhhhh",
            description=
            f"Try again in {error.retry_after:.2f}s.  Now since u know when to get ur money, get lost **DAB**",
            color=65439)
        await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)  #This is a cooldown
async def dep(ctx):
    user = ctx.author
    await open_account(ctx.author)
    users = await get_bank_data()
    users[str(user.id)]['bank'] += users[str(user.id)]['wallet']
    users[str(user.id)]['wallet'] = 0
    embedVar = discord.Embed(
        title="Money shifted from wallet to bank",
        description='Money is transferred from wallet to bank successfully',
        color=100)
    await ctx.send(embed=embedVar)
    users[str(user.id)]["xp"] += 0.25
    users[str(user.id)]["count"] += 1
    with open("economy.json", "w") as f:
        json.dump(users, f)

        return users


@dep.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=
            f"Woah There, Way too Spicy. You are sending messages too quickly",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
        await ctx.send(embed=em)
#-----------------------------------------
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def play(ctx):
    await open_account(ctx.author)
    #-------------
    randruns = random.randrange(0, 200)
    randballs = random.randrange(50, 300)
    randruns1 = str(randruns)
    randballs2 = str(randballs)

    randruns3 = random.randrange(15, 200)
    randballs4 = random.randrange(50, 300)
    randruns5= str(randruns3)
    randballs6 = str(randballs4)

    randruns7 = random.randrange(15, 100)
    randballs8 = random.randrange(50, 200)
    randruns9= str(randruns7)
    randballs10 = str(randballs8)

    randruns11 = random.randrange(15, 100)
    randballs12 = random.randrange(15, 200)
    randruns13= str(randruns11)
    randballs14 = str(randballs12)


    randruns15 = random.randrange(10, 100)
    randballs16 = random.randrange(30, 200)
    randruns17= str(randruns15)
    randballs18 = str(randballs16)

    randruns19 = random.randrange(4, 75)
    randballs20 = random.randrange(1, 150)
    randruns21= str(randruns19)
    randballs22 = str(randballs20)

    randruns23 = random.randrange(5, 60)
    randballs24 = random.randrange(1, 120)
    randruns25= str(randruns23)
    randballs26 = str(randballs24)

    randruns27 = random.randrange(5, 50)
    randballs28 = random.randrange(1, 100)
    randruns29= str(randruns27)
    randballs30 = str(randballs28)

    randruns31 = random.randrange(0, 25)
    randballs32 = random.randrange(1, 50)
    randruns33= str(randruns31)
    randballs34 = str(randballs32)

    randruns35 = random.randrange(0, 15)
    randballs36 = random.randrange(1, 30)
    randruns37= str(randruns35)
    randballs38 = str(randballs36)

    randruns39 = random.randrange(0, 5)
    randballs40 = random.randrange(1, 10)
    randruns41= str(randruns39)
    randballs42 = str(randballs40)

    total = randruns + randruns3 + randruns7 + randruns11 +   randruns15 + randruns19+randruns23 + randruns27 +         randruns31 + randruns35 + randruns39
    total_str = str(total) #concatenation error

    total_balls = randballs + randballs4 + randballs8+randballs12 + randballs16 + randballs20 + randballs24 + randballs28 + randballs32 + randballs36 + randballs40

    total_balls_str = str(total_balls)




    embed = discord.Embed(title=f"Player     Runs    Balls\n Rohit      " + randruns1 + "    " + randballs2 + "\nKL Rahul  " + randruns5 + "   " + randballs6 + "\nPujara     " + randruns9 + "   " + randballs10 + "\nKohli      " + randruns13 + "   " + randballs14 + "\nVihari      " + randruns17 + "   " + randballs18+ "\nSaha       " +randruns21 + "   " + randballs22 + "\nAshwin   " + randruns25 + "   " + randballs26 + "\nThakur    " + randruns29 + "     " + randballs30 + "\nShami     " + randruns33 + "      " + randballs34 + "\nBumrah   " + randruns37 + "     " +  randballs38 + "\nSiraj        " + randruns41 + "     " + randballs42, color=10944767)

    embed2 = discord.Embed(title="Runs scored : " + total_str)
    embed3 = discord.Embed(title="Balls consumed:" + total_balls_str)
    #-----------

    user = ctx.author
    users = await get_bank_data()
    earnings = random.randrange(100, 10000)
    if earnings < 5000:
        loss_margin = random.randrange(1, 250)
        skorkerd = embed
        totruns = embed2
        totballs = embed3
        await ctx.send("\n**The players are playing!**")
        msg = await ctx.send('.')
        await asyncio.sleep(1)
        await msg.edit(content="..")
        await asyncio.sleep(1)
        await msg.edit(content="...")
        await asyncio.sleep(1)
        await msg.edit(content=".")
        await asyncio.sleep(1)
        await msg.edit(content="..")
        await asyncio.sleep(1)
        await msg.edit(content="...")
        await asyncio.sleep(1)
        await ctx.send(embed=skorkerd)
        await asyncio.sleep(1)
        await ctx.send(embed = totruns)
        await asyncio.sleep(1)
        await ctx.send(embed=totballs)
        await ctx.send(embed=discord.Embed(title="You lost!", description=f"You lost the match and earned {earnings}"))
        embedbar = discord.Embed(title="Loss Margin", description=loss_margin, color = 54)
        await ctx.send(embed=embedbar)
        users[str(user.id)]["losses"] += 1

    if earnings >= 5000:
        win_margin = random.randrange(1, 175)
        skorkerd = embed
        totruns = embed2
        totballs = embed3
        await ctx.send("\n**The players are playing!**")
        msg = await ctx.send('.')
        await asyncio.sleep(1)
        await msg.edit(content="..")
        await asyncio.sleep(1)
        await msg.edit(content="...")
        await asyncio.sleep(1)
        await msg.edit(content=".")
        await asyncio.sleep(1)
        await msg.edit(content="..")
        await asyncio.sleep(1)
        await msg.edit(content="...")
        await asyncio.sleep(1)
        await ctx.send(embed=skorkerd)
        await asyncio.sleep(1)
        await ctx.send(embed=skorkerd)
        await asyncio.sleep(1)
        await ctx.send(embed = totruns)
        await asyncio.sleep(1)
        await ctx.send(embed=totballs)
        await ctx.send(embed=discord.Embed(title="You won!", description=f"You won the match and earned {earnings}"))
        embedbar = discord.Embed(title="Win Margin", description=win_margin, color = 54)
        await ctx.send(embed=embedbar)
        users[str(user.id)]["wins"] += 1

    users[str(user.id)]["count"] += 1
    users[str(user.id)]["xp"] += 10
    users[str(user.id)]["wallet"] += earnings
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return users


@play.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"The players are tired. 'DND'~Ms Dhoni",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
        await ctx.send(embed=em)

#------
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def version(ctx):
  await ctx.send('v1.0.8\n snapshot: 21w40a \n update: caves & cliffs\n(yes you found an easter egg made by AMJDev(the person who u might see as a  big minecraft fan))')

  
@version.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"The players are tired. 'DND'~Ms Dhoni",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
        await ctx.send(embed=em)
#-------
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stats(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()
    wins = users[str(user.id)]["wins"]
    losses = users[str(user.id)]["losses"]
    em = discord.Embed(title=f"{ctx.author.name}'s Stats",
                       color=discord.Color.orange())
    em.add_field(name="wins", value=wins)
    em.add_field(name="losses", value=losses)
    users[str(user.id)]["xp"] += 1
    users[str(user.id)]["count"] += 1
    await ctx.send(embed=em)


@stats.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Take a breather bro....",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=16776960)
        await ctx.send(embed=em)


#-------
#---- not clientcommand
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def xp(ctx):
  user = ctx.author
  await open_account(ctx.author)
  users = await get_bank_data()
  user_xp = users[str(user.id)]["xp"]
  em = discord.Embed(title=f"{ctx.author.name}'s xp",
                       color=discord.Color.orange())
  em.add_field(name="User xp", value=user_xp)
  users[str(user.id)]["count"] += 1
  await ctx.send(embed=em)

@xp.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Take a breather bro....",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=16776960)
        await ctx.send(embed=em)
#----

@client.command(aliases = ["with"])
@commands.cooldown(1, 15, commands.BucketType.user)
async def withdraw(ctx, amount=None):
    user = ctx.author
    await open_account(ctx.author)
    users = await get_bank_data()
    users[str(user.id)]['wallet'] += users[str(user.id)]['bank']
    users[str(user.id)]['bank'] = 0
    embedVar = discord.Embed(
        title="Money shifted from bank to wallet",
        description=
        'Money has been transferred from bank to wallet successfully',
        color=107)
    users[str(user.id)]["xp"] += 0.25
    users[str(user.id)]["count"] += 1
    await ctx.send(embed=embedVar)

    with open("economy.json", "w") as f:
        json.dump(users, f)

        return users


@withdraw.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Spam leads to mute. Spam leads to ban",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
        await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def dab(ctx):
    embedVar = discord.Embed(
        title="Click this link for fun",
        description="https://www.thisworldthesedays.com/freenitro17.html",
        color=71)
    await ctx.send(embed=embedVar)


@dab.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"Spam leads to mute. Spam leads to ban",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def help(ctx):
    embedVar = discord.Embed(
        title="Bot commands:",
        description=
        "1.csbal : shows your **BANK AND WALLET** balance\n2.csgamble : You get some coins or **even lose some ** Good luck!\n3.csdab : Check it out yourself\n4.csdaily : get a good sum of coins daily, **YAY**\n5.csdep: deposit ur money into the bank **yay**\n6.csfact: LEARN A NEW CRICKET FACT **WOW**!\n7.cshelp: shows this **message**\n8.cswith: it is used to withdraw money to buy stuff **yay**\n9.cswork: it is used to work and earn some money **yay**\n10.csshop : You find an amazing shop. **yay**\n 11.csbuy: buy players use csbuy 'player name' \n12.cshack:check it urself\n type `cshelp2` for the second page of commands!",
        color=189)
    await ctx.send(embed=embedVar)


@help.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"sudo stop spam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)

@client.command()
async def hack(ctx, member:discord.Member):
  if ctx.author == member:
    await ctx.send("Dumbo, you cant hack yourself")
  else:
      msg = await ctx.send('H')
      await asyncio.sleep(1)
      await msg.edit(content="Ha")
      await asyncio.sleep(1)
      await msg.edit(content="Hac")
      await asyncio.sleep(1)
      await msg.edit(content="Hack")
      await asyncio.sleep(1)
      await msg.edit(content="Hacki")
      await asyncio.sleep(1)
      await msg.edit(content="Hackin")
      await asyncio.sleep(1)
      await msg.edit(content="Hacking")
      await asyncio.sleep(1)
      await msg.edit(content=f'Well this is not easy {ctx.author}, have some patience! {ctx.author}')
      await asyncio.sleep(1)
      await msg.edit(content=f"Hacked {member}")


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def help2(ctx):
    embedVar = discord.Embed(
        title="Bot commands:",
        description=
        "12.csplay: play a match of cricket\n 13.csstats: You get to know ur amazing stats\n 14.cscommandbuyhelp: get some help about buy command\n 15.csjarvo : check it out urself\n 16.csrob @user : U CAN ROB SOME COINS FROM A USER ONLY ONCE IN 2 HRS\n 17.csxp: It shows your xp\n 18.csinfo: It shows the bot info\n19.csversion:lol\n20.csbag: Nothing but your inventory, which u can only see if u buy a player from the store\n21.cscommandcount: shows the number of commands executed by u\n22.csmonthly: Get some money monthly.\n 23.cssell playername 1 : it sells a player for some money",
        color=189)
    await ctx.send(embed=embedVar)


@help2.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"sudo stop spam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 15)
@commands.has_permissions(administrator = True)
async def adminhelp(ctx):
  embedVar = discord.Embed(title="ADMIN ONLY COMMANDS", description="1.cskick @user reason: **It kicks a user from the server**\n 2.csban @user reason : **bans a user from the server**\n 3.csunban username#id : **Unbans a banned user**\n `USERS PLS DONT USE THESE COMMANDS`")
  await ctx.send(embed=embedVar)


@adminhelp.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"sudo stop spam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def commandbuyhelp(ctx):
  embedVar = discord.Embed(title="Help for buy command", description=" How to buy a player\n We kept underscores between player name and surname for easy reference.\n This is how u need to use the command\n csbuy Deepak_Chahar 1\n where Deepak_Chahar is the name and 1 is the quantity which is just for reference.\n Do csbag to see ur players", color= 21)
  await ctx.send(embed=embedVar)

@commandbuyhelp.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"sudo stop spam!",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 2)
async def jarvo(ctx):
  await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMMB88mhCEVGgt5vZv1NCwTo_euwzzkoCWJQ&usqp=CAU")


@jarvo.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title=f"IDIOT, STOP SPAMMING ",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def rob(ctx, member:discord.Member):
  await open_account(ctx.author)
  await open_account(member)

  user = ctx.author
  await open_account(ctx.author)
  users = await get_bank_data()
  bal = await update_bank(member)
  
  if bal[0]<100:
    await ctx.send("Its nat warth it!")
    return
  
  earnings = random.randrange(0, 10000)
  embedrobVar = discord.Embed(title=f"Robbery results for {ctx.author}", description=f"{ctx.author} robbed {earnings} from {member}. \n Im calling polis")

  await update_bank(ctx.author, earnings)
  await update_bank(member, -1*earnings)
  msg = await ctx.send('.')
  await asyncio.sleep(1)
  await msg.edit(content="..")
  await asyncio.sleep(1)
  await msg.edit(content="...")
  await asyncio.sleep(1)
  await msg.edit(content=".")
  await asyncio.sleep(1)
  await msg.edit(content="..")
  await asyncio.sleep(1)
  await msg.edit(content="...")
  await asyncio.sleep(1)
  await ctx.send(embed=embedrobVar)


  users[str(user.id)]["xp"] += 5
  users[str(user.id)]["count"] += 1

@rob.error
async def command_name_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(
            title=f"IDIOT, STOP SPAMMING ",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)
    
  

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def info(ctx):
  await ctx.send("@everyone")
  embedVar = discord.Embed(title="Update", description="@everyone\nPlease use cshalp for the bot command help\n Invite bot to ur server: \nhttps://discord.com/api/oauth2/authorize?client_id=921233592443625524&permissions=534723950656&scope=bot\n Bot Creators and Owners: Anonymous Sloth, Anonymous Dog")
  await ctx.send(embed=embedVar)

@info.error
async def command_name_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(
            title=f"IDIOT, STOP SPAMMING ",
            description=f"Try again in {error.retry_after:.2f}s.",
            color=10944767)
    await ctx.send(embed=em)



mainshop = [
    {
        "name": "Ajit_Agarkar",
        "price": 1000000,
        "description": "Legend Player",
    },
    {
        "name": "Khaleel_Ahmed",
        "price": 15000,
        "description": "Indian Bowler",
    },
    {
        "name": "Ravichandran_Ashwin",
        "price": 2500000,
        "description": "Amazing Indian Allrounder",
    },
    {
  
        "name":"Sreesanth Arvind",
        "price": 500000,
        "description": "Legend Player",
    },
    {
        "name": "S_Badrinath",
        "price": 1500000,
        "description": "Legend Player",
    },
    {
        "name": "Jasprit_Bumrah",
        "price": 3500000,
        "description": "Indian Specialist bowler",
    },
    {
        "name": "Stuart_Binny",
        "price": 1700000,
        "description": "Legend Player",
    },
    {
        "name": "Lakshmipathy_Balaji",
        "price": 1200000,
        "description": "Legend Player",
    },
    {
        "name": "Yuzvendra_Chahal",
        "price": 800000,
        "description": "Indian Bowler",
    },
    {
        "name": "Deepak_Chahar",
        "price": 200000,
        "description": "Indian Bowler",
    },
    {
        "name": "Rahul_Chahar",
        "price": 200000,
        "description": "Indian Bowler",
    },
    {
        "name": "Harbhajan_Singh",
        "price": 7500000,
        "description": "Legend Player",
    },
    {
        "name": "Piyush_Chawla",
        "price": 30000,
        "description": "Indian Bowler",
    },
    {
        "name": "Sachin_Tendulkar",
        "price": 15000000,
        "description": "Legend Player",
    },
    {
        "name": "Shikhar_Dhawan",
        "price": 1000000,
        "description": "Indian Special Opener",
    },
    {
        "name": "MS_Dhoni",
        "price": 25000000,
        "description": "Legend Player",
    },
    {
        "name": "Kapil_Dev",
        "price": 10000000,
        "description": "Legend Player",
    },
    {
        "name": "Sunil_Gavaskar",
        "price": 17000000,
        "description": "Legend Player",
    },
    {
      "name": "Vijay_Hazare",
      "price": 1000000,
      "description":"Legend Player",
    },
    {
      "name":"Ashish_Nehra",
      "price":1000000,
      "description":"Legend bowler"
    },
    {
      "name":"KL_Rahul",
      "price": 1200000,
      "description":"Wicketkeeper + Captain + Opener"
    },
    {
      "name":"Virat_Kohli",
      "price":7000000,
      "description" : "Amazing batter and captain"
    },
    {
      "name":"Rishabh_Pant",
      "price":1752000,
      "description": "Wickerkeeper Batter"
    },
    {
      "name":"Prithvi_Shaw",
      "price":500000,
      "description":"Amazing Opener"
    },
    {
      "name":"Rohit_Sharma",
      "price":5000000,
      "description":"amazing opener"
    }
]

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.6* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("economy.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt <0:
                  return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
          return [False, 3]
    except:
      return [False, 3]


    await update_bank(user, cost * -1, "wallet")
    with open("economy.json", "w") as f:
        json.dump(users, f)
    return [True, "Worked"]

    


@client.command()
async def shop(ctx):
    em = discord.Embed(title="Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}")

    await ctx.send(embed=em)
    embadberiabul = discord.Embed(title="Whatever u sell will be sold at 60% of object's original price", color=198)
    await ctx.send(embed=embadberiabul)


@client.command()
async def buy(ctx, item, amount):
    amount = 1
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            embedVar = discord.Embed(title="error", description="Player not found.", color=183)
            await ctx.send(embed=embedVar)
            return
        if res[1] == 2:
            embedVar = discord.Embed(title="error", description=f"You don't have enough money in your wallet to buy {amount} {item}", color=198)
            await ctx.send(embed=embedVar)
            return
    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("economy.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


async def open_account(user):
    with open("economy.json", "r") as f:
        users=json.load(f)

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["bag"] = []
        users[str(user.id)]["wins"] = 0
        users[str(user.id)]["losses"] = 0
        users[str(user.id)]["xp"] = 0
        users[str(user.id)]["count"] = 0
                

    with open("economy.json", "w") as f:
        json.dump(users, f)

    return True

async def get_bank_data():
    with open("economy.json", "r") as f:
        users = json.load(f)
        return users

fun_facts = [
    'The king Kohli hasn"t scored a single century since last 2 years. seems like he will stay without any more centuries till the end of his career',
    'The highest number of runs scored in an over is not 36. It’s 77!',
    'Anil Kumble, a legendary indian spinner has achieved a remarkable feat.He took 10 wickets in an innings against Pakistan.',
    'After Virat Kohli’s debut, India has chased down 300 targets five times!',
    'Saurav Ganguly is the only player to win four consecutive Man of the Match awards in ODIs!',
    'India won the 1983 World Cup and won their first ever Test at Lord’s three years later in 1986.',
    'Can you imagine Sachin Tendulkar playing for Pakistan before India? This happened during a practice match between India and Pakistan at the Brabourne Stadium in 1987 where Tendulkar came on the field as a substitute fielder for Pakistan.',
    'Virat Kohli is the only bowler to have got the wicket off the 0th ball of his T20I career. (Virat Kohli dismissed Kevin Pietersen off his very first delivery in T20 Internationals at Manchester in 2011. The ball was called a wide so it was not a legitimate delivery. )',
    " After claiming Sachin's wicket, Brad Hogg asked him to sign a photograph of the dismissal. Sachin signed and wrote it will never happen again. And it never did.",
    'India is the only country to win the 60-Over, 50-Over and 20-Over World Cup',
    'Mohammad Azharuddin is the only batsman on the planet to score three centuries in the first three Test matches he played.',
    'On the morning of 11/11/11 South Africa needed 111 runs to win at 11:11!(Which the developers like to call the 1 coincidence)',
    'Sachin Tendulkar played for Pakistan before India!?',
    'Sanath Jayasuriya has more ODI wickets than Shane Warne.',
    'Adam Gilchrist holds the record for playing the most number of Tests straight after debut',
    'The only batsman in the whole world to have scored ODI century after coming to bat post 30 overs is AB De Villiers. And he did not achieve this once, but twice. The first one came in 2010 when he came to bat in the 33rd over against India and the second one came against West Indies when he came to bat in the 39th over in 2015.'
]

keep_alive.keep_alive()

client.run(os.getenv('TOKEN')) 
