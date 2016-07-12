import asyncio
import discord
from discord.ext import commands

async def ban_dispenser(bot, ctx, time, members, **kwargs):

	if time == 0:	# INDEFINITE BAN
		for member in members:
			await bot.send_message(member, 'You have been indefinitely banned from the server. _Jah praise_.')
			await bot.ban(member)
		await bot.say_block('Indefinitely Banned: \n\t{}'.format(", ".join(m.name for m in members)))

	else:			# TEMP BAN
		banstr = ''
		inv = (await bot.create_invite(ctx.message.server)).url

		# send messages to all the members specified and ban then
		for member in members:
			banstr += '\t{}\n'.format(member.name)
			await bot.send_message(member, 'You have been banned for {} mins.\nYou will be able to use the link below to rejoin the server when your ban is automatically lifted.\n{}'.format(time, inv))
			await bot.ban(member)

		# wait out the duration of the ban
		await bot.say_block('Banned for {} mins:\n{}'.format(time, banstr))
		await asyncio.sleep(time*60) # `time` minutes
		
		# unban all the members
		for member in members:	
			await bot.unban(ctx.message.server, member)
			await bot.say_block('{}\'s ban has been lifted.'.format(member.name))

async def ban_hammer(bot, ctx, time, members, **kwargs):
	for member in members:
		await bot.ban(member)

	if time > 0: # temp ban
		await asyncio.sleep(time*60)

		for member in members:
			await bot.unban(member)

async def voice_state_changer(bot, ctx, time, members, **kwargs):
	names = ", ".join([m.name for m in members])
	for member in members:
		await bot.server_voice_state(member, mute=kwargs.get('mute', False), deafen=kwargs.get('deafen', False))

	if time == 0:
		await bot.say_block('Muted:\n\t {}'.format(names))

	elif time > 0:
		await bot.say_block('Temporarily muted ({} mins):\n\t {}'.format(time, names))
		await asyncio.sleep(time*60)

		for member in members:
			await bot.server_voice_state(member, mute=False, deafen=False)

		await bot.say_block('Mutes lifted:\n\t {}'.format(names))

async def permission_changer(bot, ctx, time, members):
	pass


###
### ADMINISTRATOR - 
###

administrator = {
	'ban' : ban_dispenser,
	'mute' : voice_state_changer,
	'deafen' : voice_state_changer,
	'chatmute' : None,
}

deadministrator = {
	'unban' : None,
	'unmute' : None,
	'undeafen' : None,
	'chatunmute' : None
}

async def administrate(func_key, self, ctx, time, members, **kwargs):
	""" Parse arguments (check for optional int, convert to member as necessary)
		and use the administrator dict to call the appropriate administrative function """
	try:
		time = int(time)
	except ValueError:
		converter = commands.MemberConverter(ctx, time)
		members = list(members)
		members.insert(0, converter.convert())
		time = 0

	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specify member(s) to {}.'.format(func_key))
	
	await administrator[func_key](self.bot, ctx, time, members, **kwargs)

async def deadministrate(func_key, self, members, **kwargs):
	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specifiy member(s) to {}.'.format(func_key))

	for member in members:
		await deadministrator[func_key](self.bot, members, **kwargs)
