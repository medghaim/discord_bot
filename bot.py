'''
MAIN SCRIPT - Sets up and runs the bot, and defines how to handle events.
'''

import discord
import asyncio
from discord.ext import commands
from cogs.utils import initializer

description = '''A multi-purpose written to do bot things by its lazy master.'''

startup_extensions = [
	"cogs.administration",
	"cogs.discord_functionality",
	"cogs.internet",
	"cogs.utilities",
	"cogs.fun"
	]

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
	print('Logged in as: ' + bot.user.name)
	print('Active Servers: ')
	for s in bot.servers:
		print('\t'+s.name)
	print('-------------------')

@bot.event
async def on_command_error(error, ctx):
	'''
	if isinstance(error, commands.NoPrivateMessage):
		await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
	elif isinstance(error, commands.DisabledCommand):
		await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
	elif isinstance(error, commands.CommandInvokeError):
		print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
		traceback.print_tb(error.original.__traceback__)
		print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
	elif isinstance(error, commands.BadArgument):
		await bot.send_message(ctx.message.channel, '{0.__class__.__name__}: {0}'.format(error))
	'''
	if isinstance(error, commands.CommandError):
		await bot.send_message(ctx.message.channel, '```py\n{0.__class__.__name__}: {0}\n```'.format(error))


#if __name__ == 'main': ##only cally if the script is executed, not imported.
bot.credentials = initializer.get_credentials()
initializer.init_modules(bot, startup_extensions) ##Initialize all modules

###RUNS AND STARTS THE BOT
bot.run(bot.credentials.token)
