import discord
from env import load_env
import geoguessr_api
from StatsView import StatsView
from models.enums import Method, FriendStatus, SearchOption, MapBrowseOption, BadgeFetchType

username, password, token = load_env()

bot = discord.Bot()

guild_ids = [783759963981742100]


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=guild_ids, description="Affiche les events disponibles en ce moment")
async def events(ctx):
    async with geoguessr_api.AsyncClient(username, password, token) as client:
        competitions = await client.get_events()
        embCompetition = discord.Embed(title="Liste des events disponibles")

        for competition in competitions:
            results = await client.get_event_results(competition)  # id str / Event object
            if results.position != 0:
                embCompetition.add_field(name=f"{competition.name}",
                                         value=f"{competition.description}\n\tposition : {results.position}",
                                         inline=False)
            else:
                embCompetition.add_field(name=f"{competition.name}", value=f"{competition.description}", inline=False)

        await ctx.respond(embed=embCompetition)


@bot.slash_command(guild_ids=guild_ids, description="Stats de l'utilisateur")
async def stats(ctx, query: discord.Option(str,
                                           description="Entrez le nom de la personne que vous chercher, ou rien pour vous même !",
                                           required=False)):
    async with geoguessr_api.AsyncClient(username, password, token) as client:
        # searched_user = await client.search(query=user, search_type=SearchOption.USER) if user else None
        # stats = await client.get_stats(None if not user else client.search(query=user, search_type=SearchOption.USER))
        searched_user = None if not query else await client.search(query=query, search_type=SearchOption.USER)
        # searched_user = searched_user[0]
        stat = await client.get_stats(searched_user[0] if searched_user else None)
        user = client.me if not query else searched_user[0]

        embed = discord.Embed(title=f"Statistiques de {user.nick}",
                              url=f"https://geoguessr.com{user.url}",
                              # color=user.color)
                              )
        # profile.set_thumbnail(url=userRes.getPinUrl())
        # profile.url = userRes.getUrl()

        view = StatsView(user, stat, embed, ctx)
        embed.description = f"Voici le profil de {user.nick}\nUtiliser les boutons pour naviguer !"

        await ctx.respond(embed=embed, view=view)


@bot.slash_command(guild_ids=guild_ids)
async def test(ctx):
    await ctx.respond("お願いします")


def main():
    bot.run("NzgzNzQyMzg2NDE3MDQxNDI4.X8fK-g.4H4qtE0U-z_wg5zrQlWKttwOTwM")


if __name__ == "__main__":
    main()
