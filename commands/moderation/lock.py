import disnake
from disnake.ext import commands


class lock(commands.Cog, name='lock', description="locks the mentioned channel"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name="lock", description="Lock the current channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def Lock(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel = None):
        channel = channel or inter.channel
        overwrite = channel.overwrites_for(inter.guild.default_role)
        if overwrite.send_messages or overwrite.send_messages is None:
            await channel.set_permissions(inter.guild.default_role, send_messages=False)
            lockEmbed = disnake.Embed(title="Command `*lock` => executed", color=disnake.Color.green())
            lockEmbed.add_field(name="The command executed", value=f"{channel.mention} is now locked")
            await inter.channel.send(embed=lockEmbed, delete_after=5)
            await channel.send(embed=lockEmbed)
        else:
            lockEmbed = disnake.Embed(title="Command `*lock` => unaffected", color=disnake.Color.yellow())
            lockEmbed.add_field(name="The command probably didn't work because:", value="1. Channel is already unlocked")
            await inter.response.send_message(embed=lockEmbed, delete_after=5)
            await channel.send(embed=lockEmbed)

    @Lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = disnake.Embed(title="Command => `*lock` => Fail", description="You dont have permissions to manage channels", color=disnake.Color.red())
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = disnake.Embed(title="Command => `*lock` => Fail", description="The bot doesnt have permissions to manage channels", color=disnake.Color.red())
            await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = disnake.Embed(title="Command `*lock` => Fail", description="Some error occurred", color=disnake.Color.red())
            await ctx.channel.send(embed=errorEmbed)


def setup(client: commands.Bot):
    client.add_cog(lock(client))
