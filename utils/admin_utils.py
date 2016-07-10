import asyncio
import discord
from discord.ext import commands

async def ban_dispenser(bot, ctx, time, members):
	if time == 0:	# INDEFINITE BAN
		for member in members:
			await bot.send_message(member, 'You have been indefinitely banned from the server. _Jah praise_.')
			await bot.ban(member)
		await bot.say('Indefinitely Banned: \n\t{}'.format(", ".join(m.name for m in members)))

	else:			# TEMP BAN
		banstr = ''
		inv = (await bot.create_invite(ctx.message.server)).url

		# send messages to all the members specified and ban then
		for member in members:
			banstr += '\t{}\n'.format(member.name)
			await bot.send_message(member, 'You have been banned for {} mins.\nYou will be able to use the link below to rejoin the server when your ban is automatically lifted.\n{}'.format(time, inv))
			await bot.ban(member)

		# wait out the duration of the ban
		await bot.say('Banned for {} mins:\n{}'.format(time, banstr))
		await asyncio.sleep(time*60) # `time` minutes
		
		# unban all the members
		for member in members:	
			await bot.unban(ctx.message.server, member)
			await bot.say('{}\'s ban has been lifted.'.format(member.name))

async def mute_dispenser(bot, ctx, time, members):
	pass
