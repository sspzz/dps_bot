from dps import PirateFactory
from discord.ext import commands
import discord
import logging
import logging.config

# Utilities related to Discord
class DiscordUtils:
	@staticmethod
	async def embed(ctx, title, description, thumbnail=None, image=None):
		embed = discord.Embed(title=title, description=description)
		if thumbnail is not None:
			embed.set_thumbnail(url=thumbnail)
		if image is not None:
			embed.set_image(url=image)
		await ctx.send(embed=embed)

	@staticmethod
	async def embed_image(ctx, title, file, filename, description=None, footer=None, url=None):
		embed = discord.Embed(title=title)
		file = discord.File(file, filename=filename)
		embed.set_image(url="attachment://{}".format(filename))
		if description is not None:
			embed.description = description
		if footer is not None:
			embed.set_footer(text=footer)
		if url is not None:
			embed.url = url
		await ctx.send(file=file, embed=embed)

	@staticmethod
	async def embed_fields(ctx, title, fields, inline=True, thumbnail=None, url=None):
		embed = discord.Embed(title=title)
		if thumbnail is not None:
			embed.set_thumbnail(url=thumbnail)
		for field in fields:
			embed.add_field(name=field[0], value=field[1], inline=inline)
		if url is not None:
			embed.url = url
		await ctx.send(embed=embed)


#
# Setup
#
bot = commands.Bot(command_prefix="!")

logging.basicConfig(filename='wizz_bot.log',
                    filemode='a',
                    format='[%(asctime)s] %(name)s - %(message)s',
                    datefmt='%d-%m-%Y @ %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('wizz_bot')



#
# Animated walk cycles
#
@bot.command(name="walk", aliases=["gif"])
async def walkcycle(ctx, token_id):
	logger.info("WALKCYCLE %s", token_id)
	pirate = PirateFactory.get_pirate(token_id)
	if pirate is not None:
		await DiscordUtils.embed_image(ctx, "Pirate {}".format(pirate.token_id), pirate.walkcycle, "{}.gif".format(token_id))
	else:
		await ctx.send("Could not load pirate {}".format(wiz_id))

#
# Run bot
#
bot.run(config.dicord_access_token)
