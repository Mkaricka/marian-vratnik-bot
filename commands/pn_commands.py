from discord.ext import commands
import config
from core.absences import (
    has_active_absence,
    start_absence,
    end_absence
)
from core.roles import set_pn, set_mimo_prace
from datetime import datetime


class PNCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # !pn – NAHLÁSENIE PN
    # =========================
    @commands.command()
    async def pn(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        member = ctx.author
        uid = str(member.id)

        if has_active_absence(uid):
            await ctx.send("👮‍♂️ Už máš aktívnu PN alebo dovolenku.")
            return

        def check(m):
            return m.author == member and m.channel == ctx.channel

        # ---- OD KEDY ----
        await ctx.send("📅 **Od kedy máš PN?** (YYYY-MM-DD)")

        try:
            msg_from = await self.bot.wait_for("message", check=check, timeout=60)
            date_from = datetime.strptime(
                msg_from.content.strip(), "%Y-%m-%d"
            ).date().isoformat()
        except:
            await ctx.send("❌ Nesprávny dátum. PN zrušená.")
            return

        # ---- DO KEDY ----
        await ctx.send("📅 **Do kedy máš PN?** (YYYY-MM-DD alebo `neviem`)")

        try:
            msg_to = await self.bot.wait_for("message", check=check, timeout=60)
            content = msg_to.content.strip().lower()

            if content == "neviem":
                date_to = None
            else:
                date_to = datetime.strptime(
                    content, "%Y-%m-%d"
                ).date().isoformat()
        except:
            await ctx.send("❌ Nesprávny dátum. PN zrušená.")
            return

        # ---- ZÁPIS PN ----
        start_absence(uid, "PN", date_from, date_to)
        await set_pn(member)

        await ctx.send("👮‍♂️ PN bola úspešne zaznamenaná.")

        # ---- OZNAM DO #pn ----
        pn_channel = ctx.guild.get_channel(config.PN_CHANNEL_ID)
        if pn_channel:
            await pn_channel.send(
                "🚑 **PN nahlásená**\n"
                f"👤 {member.display_name}\n"
                f"📅 Od: {date_from}\n"
                f"📅 Do: {date_to if date_to else 'neurčené'}"
            )

    # =========================
    # !koniecpn – UKONČENIE PN
    # =========================
    @commands.command()
    async def koniecpn(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        member = ctx.author
        uid = str(member.id)

        result = end_absence(uid)

        if not result or result["type"] != "PN":
            await ctx.send("👮‍♂️ Nemáš aktívnu PN.")
            return

        await set_mimo_prace(member)

        await ctx.send("👮‍♂️ PN bola ukončená. Vitaj späť.")

        # ---- OZNAM DO #pn ----
        pn_channel = ctx.guild.get_channel(config.PN_CHANNEL_ID)
        if pn_channel:
            await pn_channel.send(
                "✅ **PN ukončená**\n"
                f"👤 {member.display_name}\n"
                f"📅 Ukončené: {result['end']}"
            )


async def setup(bot):
    await bot.add_cog(PNCommands(bot))
