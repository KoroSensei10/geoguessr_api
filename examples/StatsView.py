import discord
from discord.ui import Button, View

from models.user.stats import UserExtendedStats


class StatsView(View):
    def __init__(self, user, stats: UserExtendedStats, base_embed: discord.Embed, ctx):
        super().__init__(timeout=10.0)
        self.stats = stats
        self.user = user
        self.base_embed = base_embed
        self.ctx = ctx

    options = [
        discord.SelectOption(label="Stats de base", description="Les stats des parties classiques"),
        discord.SelectOption(label="Stats de Streak", description="Les stats des parties streaks"),
        discord.SelectOption(label="Stats battle royal", description="Les stats des battle royal"),
    ]

    async def interaction_check(self, interaction) -> bool:
        return interaction.user == self.ctx.author

    @discord.ui.select(placeholder="Choisi les stats que tu veux voir", min_values=1, max_values=1, options=options)
    async def select_callback(self, select, interaction):
        if select.values[0] == "Stats de base":
            embed = discord.Embed(title="Stats des parties classiques",
                                  color=discord.Color.nitro_pink(),
                                  description=f"Les statisitques pour {self.user.nick}")

            embed.add_field(name="Nombre de partie jouée : ",
                            value=f"{self.stats.games_played}", inline=False)
            embed.add_field(name="Nombre de round joué : ",
                            value=f"{self.stats.rounds_played}", inline=False)
            embed.add_field(name="Meilleur score : ",
                            value=f"{self.stats.max_game_score.amount} {self.stats.max_game_score.unit}", inline=False)

            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "Stats battle royal":
            countries = self.stats.battle_royale_stats[0]
            distance = self.stats.battle_royale_stats[1]
            embed = discord.Embed(title="Stats parties battle royale",
                                  color=discord.Color.dark_red(),
                                  description=f"Les statisitques pour {self.user.nick}")

            embed.add_field(name="Nombre de partie countries jouée : ",
                            value=f"{countries.value.games_played}", inline=False)
            embed.add_field(name="Nombre de partie countries gagnée : ",
                            value=f"{countries.value.wins}", inline=False)
            embed.add_field(name="Position moyenne : ",
                            value=f"{countries.value.average_position}", inline=False)
            # embed.add_field(name="Nombre de guess : ",
            # value=f"{countries.num_guesses} ", inline=False)

            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "Stats de Streak":
            embed = discord.Embed(title="Stats des parties classiques",
                                  color=discord.Color.nitro_pink(),
                                  description=f"Les statisitques pour {self.user.nick}")

            embed.add_field(name="Nombre de partie jouée : ",
                            value=f"{self.stats.streak_games_played}", inline=False)
            embed.add_field(name="records : ",
                            value=f"{self.stats.streak_records}", inline=False)
            # embed.add_field(name="Meilleur score : ",
            #                 value=f"{self.stats.max_game_score.amount} {self.stats.max_game_score.unit}", inline=False)

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.danger)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=self.base_embed, view=self)
