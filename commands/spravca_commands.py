from discord.ext import commands
import config
from core.attendance import calculate_user_stats
from core.performance import calculate_performance


class SpravcaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # INTERNÁ FUNKCIA – CEO CHECK
    # =========================
    def is_ceo(self, member):
        return any(role.id == config.ROLE_CEO for role in member.roles)

    # =========================
    # !zamestnanec @meno
    # =========================
    @commands.command()
    async def zamestnanec(self, ctx, member: commands.MemberConverter):
        if not self.is_ceo(ctx.author):
            await ctx.send("⛔ Tento príkaz môže používať iba CEO.")
            return

        uid = str(member.id)

        # ŠTATISTIKY PRÁCE
        work = calculate_user_stats(uid)
        perf = calculate_performance(work)

        guild = ctx.guild

        # ROLE
        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)
        role_dov = guild.get_role(config.ROLE_DOVOLENKA)
        role_pn = guild.get_role(config.ROLE_PN)
        role_mimo = guild.get_role(config.ROLE_MIMO_SLUZBY)

        # AKTUÁLNY STAV PODĽA ROLÍ (JEDINÝ ZDROJ PRAVDY)
        if role_v in member.roles:
            status = "🟢 V práci"
        elif role_prest in member.roles:
            status = "☕ Prestávka"
        elif role_dov in member.roles:
            status = "🏖️ Dovolenka"
        elif role_pn in member.roles:
            status = "🤒 PN"
        elif role_mimo in member.roles:
            status = "🔴 Mimo práce"
        else:
            status = "⚠️ Neznámy stav"

        msg = (
            f"📊 **Report – {member.display_name}**\n"
            f"📍 Aktuálny stav: {status}\n\n"
            f"⏱️ Odpracované hodiny: {work['hours']}\n"
            f"📅 Počet smien: {work['shifts']}\n"
            f"☕ Prestávky: {work['breaks']}\n"
            f"📈 Priemer smeny: {work['avg_shift']} h\n"
            f"⭐ Úspešnosť: {perf} %"
        )

        await ctx.send(msg)

    # =========================
    # !tim
    # =========================
    @commands.command()
    async def tim(self, ctx):
        if not self.is_ceo(ctx.author):
            await ctx.send("⛔ Tento príkaz môže používať iba CEO.")
            return

        guild = ctx.guild

        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_mimo = guild.get_role(config.ROLE_MIMO_SLUZBY)
        role_dov = guild.get_role(config.ROLE_DOVOLENKA)
        role_pn = guild.get_role(config.ROLE_PN)

        total = 0
        v_praci = 0
        mimo = 0
        dovolenka = 0
        pn = 0

        total_hours = 0
        total_perf = []
        active_workers = 0

        for member in guild.members:
            if member.bot:
                continue

            total += 1

            if role_v in member.roles:
                v_praci += 1
                stats = calculate_user_stats(str(member.id))
                total_hours += stats["hours"]
                total_perf.append(calculate_performance(stats))
                active_workers += 1

            elif role_dov in member.roles:
                dovolenka += 1
            elif role_pn in member.roles:
                pn += 1
            elif role_mimo in member.roles:
                mimo += 1

        avg_perf = round(sum(total_perf) / active_workers, 2) if active_workers else 0

        msg = (
            f"🏢 **Tímový report**\n\n"
            f"👥 Zamestnanci: {total}\n"
            f"🟢 V práci: {v_praci}\n"
            f"🔴 Mimo práce: {mimo}\n"
            f"🏖️ Dovolenka: {dovolenka}\n"
            f"🤒 PN: {pn}\n\n"
            f"⏱️ Celkové hodiny tímu: {round(total_hours, 2)}\n"
            f"⭐ Priemerná úspešnosť tímu: {avg_perf} %"
        )

        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(SpravcaCommands(bot))
