from discord.ext import commands
from cogs.utils import output

class Utilities():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def math(self, *args : str):
		""" Evaluates a math expression """
		await output.speak(self.bot, ", ".join(args))
		

def setup(bot):
	bot.add_cog(Utilities(bot))