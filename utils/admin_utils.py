import asyncio
import discord
from discord.ext import commands

""" Keep in mind that any administrative function written here, 
	and added to do_dispatcher and undo_dispatcher, 
	CAN be called from both admin_do and admin_undo.
	ie, unban can be called by from admin_undo (ie, !unban x)
	or it can be called in admin_do, after a temp ban (ie, !ban 5 x <-- will call unban)
"""

async def ban(bot, ctx, members, time):
	inv = (await bot.create_invite(ctx.message.channel)).url
	msg = 'You have been banned for {} mins.\n. You will be able to use the following invite when your ban is lifted.\n{}'.format(time, inv)
	output = 'Temporarily banned ({} mins):\n\t'.format(time)
	if time == 0:
		msg = 'You have been indefinitely banned from {}. _Jah praise_'.format(ctx.message.server)
		output = 'Banned:\n\t'

	for member in members:
		await bot.send_message(member, msg)
		output += '{}\n\t'.format(member.name)
		await bot.ban(member)
	await bot.say_block(output.strip())

async def unban(bot, ctx, members):
	bans = await bot.get_bans(ctx.message.server)
	output = 'Unbanned:\n\t'
	for member in members:
		if isinstance(member, str): # member is str, unban was called from admin_undo, thus we must find member from bans list
			candidates = [m for m in bans if m.name.lower() == member.lower()]
			if len(candidates) <= 0:
				raise commands.BadArgument('"{}" member not found.'.format(member))
			elif len(candidates) > 1:
				raise commands.BadArgument('"{}" refers to more than one person. Please ban manually.'.format(member))
			member = candidates[0] # len(candidates) == 1
		await bot.unban(ctx.message.server, member)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())

async def disable_voice_state(bot, ctx, members, time, **kwargs):
	is_mute = kwargs.get('mute', False)
	verb = 'Muted'
	if not is_mute:
		verb = 'Deafened'

	output = '{}:\n\t'.format(verb)
	if time > 0:
		output = 'Temporarily {} ({} mins):\n\t'.format(verb.lower(), time)

	for member in members:
		await bot.server_voice_state(member, **kwargs)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())

async def enable_voice_state(bot, ctx, members, **kwargs):
	""" If kwargs has mute=True, that means we should UNMUTE it (if deafen=True, UNDEAFEN). 
	This is designed so that enable_voice_state can be called from admin_do as well.
	eg, in a temp mute, admin_do calls disable_voice_state with kwargs = {mute:True}. When the time is up,
	these same kwargs get passed to undo_dispatcher, which calls enable_voice_state with
	the same initial kwargs ({mute:True}).
	Therefore	- admin_do MUST be called with ONLY 1 kwarg (mute or deafen) 
				- that kwarg must be true to indicate it's what we want to alter the state of.
					- admin_do / admin_undo resolves _how_ we want to alter state
						- admin_do = mute
						- admin_undo = unmute
	"""
	is_deaf = kwargs.get('deafen', False)

	output = 'Unmuted:\n\t'
	t_kwargs = {'mute' : False} #constructing new kwargs
	if is_deaf:
		output = 'Undeafened:\n\t'
		t_kwargs = {'deafen' : False}

	for member in members:
		await bot.server_voice_state(member, **t_kwargs)
		output += '{}\n\t'.format(member.name)
	await bot.say_block(output.strip())


# ADMINISTRATIVE FUNCTION DISPATCHERS (dict of value->function)
do_dispatcher = {
	'ban' : ban,
	'mute' : disable_voice_state,
	'deafen' : disable_voice_state,
	'chatmute' : None,
}

undo_dispatcher = {
	'ban' : unban,
	'mute' : enable_voice_state,
	'deafen' : enable_voice_state,
	'chatmute' : None,
}


#Only functions that have the option of specifying time SHOULD call this
async def admin_do(func_key, bot, ctx, members, time, **kwargs):
	""" Parse arguments (check for optional int, convert to member as necessary)
	and use the admin_dispatcher dict to call the appropriate administrative function 

	Allows us to check for option time arg, which is common procedure for ban/mute/deafen
	"""
	# parsing arguments, determining if time was supplied argument or not
	try:
		time = int(time)
	except ValueError:
		converter = commands.MemberConverter(ctx, time)
		members = list(members)
		members.insert(0, converter.convert())
		time = 0

	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specify member(s) to {}.'.format(func_key))
	
	# the administration / temp administration (ie, ban / temp ban)
	await do_dispatcher[func_key](bot, ctx, members, time, **kwargs)
	if time > 0: # temp ban
		await asyncio.sleep(time)#*60)
		await undo_dispatcher[func_key](bot, ctx, members, **kwargs)

#Only functions that DON'T have the option to specify a time SHOULD call this
async def admin_undo(func_key, bot, ctx, members, **kwargs):
	if len(members) == 0:
		raise commands.MissingRequiredArgument('Must specifiy member(s) to {}.'.format(func_key))

	for member in members:
		await undo_dispatcher[func_key](bot, ctx, members, **kwargs)
