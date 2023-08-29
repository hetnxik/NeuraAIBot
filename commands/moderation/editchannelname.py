import disnake
import datetime
from disnake.ext import commands


class editChannelName(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="editchannelname", description="edit the name of the channel")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def editchannelname(self, inter: disnake.ApplicationCommandInteraction, name: str):
        await inter.channel.edit(name=name)
        edit_embed = disnake.Embed(title="Command `editchannelname`", description=f"The current channel name changed to {name}", color=disnake.Color.green())
        await inter.response.send_message(embed=edit_embed)

    @editchannelname.error
    async def editChannelName_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            error_embed = disnake.Embed(title=f"Slow it down bro!", description=f"Try again in {error.retry_after:.2f}s.\nCooldown is of 20s", colour=disnake.Colour.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=error_embed)
        elif isinstance(error, commands.MissingPermissions):
            error_embed = disnake.Embed(title="Command => `*editChannelName` => Fail", description="You dont have permissions to manage channels")
            await ctx.send(embed=error_embed)
        elif isinstance(error, commands.BotMissingPermissions):
            error_embed = disnake.Embed(title="Command => `*editChannelName` => Fail", description="The bot doesnt have permissions to manage channels")
            await ctx.send(embed=error_embed)
        else:
            error_embed = disnake.Embed(title="Command `*editChannelName` => Fail", description="Some error occurred")
            await ctx.channel.send(embed=error_embed)


def setup(client: commands.Bot):
    client.add_cog(editChannelName(client))
