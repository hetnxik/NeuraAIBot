import disnake, datetime
from disnake.ext import commands


class Clear(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="clear", description="purge messages")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.ApplicationCommandInteraction, amt: int = 1):
        await inter.channel.purge(limit=amt + 1)
        purge_embed = disnake.Embed(title="Command `*purge`", description=f"Deleted {amt} messages.", color=disnake.Colour.green())
        await inter.response.send_message(embed=purge_embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            purge_embed = disnake.Embed(title=f"Slow it down bro!", description=f"Try again in {error.retry_after:.2f}s.\nCooldown is of 4s", colour=disnake.Colour.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=purge_embed)
        elif isinstance(error, commands.MissingPermissions):
            purge_embed = disnake.Embed(title="Command => `*clear` => Fail", description="You dont have permissions to delete messages", color=disnake.Colour.red())
            await ctx.send(embed=purge_embed)
        elif isinstance(error, commands.BotMissingPermissions):
            purge_embed = disnake.Embed(title="Command => `*clear` => Fail", description="The bot doesnt have permissions to delete messages", color=disnake.Colour.red())
            await ctx.send(embed=purge_embed)


def setup(client: commands.Bot):
    client.add_cog(Clear(client))
