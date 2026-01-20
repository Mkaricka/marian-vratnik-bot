from discord.ext import commands
import config


class InfoCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # !info – ZOZNAM PRÍKAZOV
    # =========================
    @commands.command()
    async def info(self, ctx):
        if ctx.channel.id != config.INFO_CHANNEL_ID:
            return

        msg = (
            "👮‍♂️ **Vrátnik Marián – prehľad príkazov**\n\n"

            "🟢 **PRÁCA**\n"
            "`!pracujem` – nástup do práce\n"
            "`!prestávka` – začiatok prestávky\n"
            "`!pokračujem` – návrat z prestávky\n"
            "`!koniec` – odchod z práce\n\n"

            "🏖️ **DOVOLENKA**\n"
            "`!dovolenka` – nahlásenie dovolenky\n"
            "`!koniecdovolenky` – ukončenie dovolenky\n\n"

            "🤒 **PN**\n"
            "`!pn` – nahlásenie PN\n"
            "`!koniecpn` – ukončenie PN\n\n"

            "ℹ️ **INFORMÁCIE**\n"
            "`!info` – tento prehľad príkazov\n\n"

            "⚠️ **POZNÁMKY**\n"
            "• Príkazy používaj iba v správnom kanáli\n"
            "• Počas PN alebo dovolenky nie je možné pracovať\n"
            "• Všetko eviduje Vrátnik Marián\n"
        )

        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
