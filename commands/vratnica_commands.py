from discord.ext import commands
import config
from storage.json_store import load_json, save_json
from datetime import datetime
from core.absences import has_active_absence


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class VratnicaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # !pracujem
    # =========================
    @commands.command()
    async def pracujem(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        guild = ctx.guild
        member = ctx.author
        uid = str(member.id)

        # ⛔ blok PN / dovolenka
        if has_active_absence(uid):
            await ctx.send("👮‍♂️ Nemôžeš nastúpiť – máš PN alebo dovolenku.")
            return

        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_mimo = guild.get_role(config.ROLE_MIMO_SLUZBY)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)

        users = load_json("users.json", {})
        sessions = load_json("sessions.json", {})

        users[uid] = {"name": member.display_name}

        # ochrana proti dvojitej smene
        if uid in sessions and sessions[uid]:
            if sessions[uid][-1]["end"] is None:
                await ctx.send("👮‍♂️ Už máš otvorenú pracovnú smenu.")
                return

        sessions.setdefault(uid, []).append({
            "start": now(),
            "end": None,
            "breaks": []
        })

        save_json("users.json", users)
        save_json("sessions.json", sessions)

        # ROLE – tvrdý prepis
        await member.remove_roles(role_mimo, role_prest)
        await member.add_roles(role_v)

        await ctx.send(f"👮‍♂️ Nástup zaznamenaný v {now()}")

    # =========================
    # !prestávka
    # =========================
    @commands.command()
    async def prestavka(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        guild = ctx.guild
        member = ctx.author
        uid = str(member.id)

        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)

        sessions = load_json("sessions.json", {})

        if uid not in sessions or not sessions[uid]:
            await ctx.send("👮‍♂️ Nemáš aktívnu smenu.")
            return

        session = sessions[uid][-1]

        if session["end"] is not None:
            await ctx.send("👮‍♂️ Nemáš aktívnu smenu.")
            return

        if session["breaks"] and session["breaks"][-1]["end"] is None:
            await ctx.send("👮‍♂️ Už si na prestávke.")
            return

        session["breaks"].append({
            "start": now(),
            "end": None
        })

        save_json("sessions.json", sessions)

        await member.remove_roles(role_v)
        await member.add_roles(role_prest)

        await ctx.send("👮‍♂️ Prestávka zaznamenaná.")

    # =========================
    # !pokračujem
    # =========================
    @commands.command()
    async def pokracujem(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        guild = ctx.guild
        member = ctx.author
        uid = str(member.id)

        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)

        sessions = load_json("sessions.json", {})

        if uid not in sessions or not sessions[uid]:
            await ctx.send("👮‍♂️ Nemáš aktívnu smenu.")
            return

        session = sessions[uid][-1]

        if not session["breaks"] or session["breaks"][-1]["end"] is not None:
            await ctx.send("👮‍♂️ Nie si na prestávke.")
            return

        session["breaks"][-1]["end"] = now()
        save_json("sessions.json", sessions)

        await member.remove_roles(role_prest)
        await member.add_roles(role_v)

        await ctx.send("👮‍♂️ Pokračovanie v práci zaznamenané.")

    # =========================
    # !koniec
    # =========================
    @commands.command()
    async def koniec(self, ctx):
        if ctx.channel.id != config.VRATNICA_CHANNEL_ID:
            return

        guild = ctx.guild
        member = ctx.author
        uid = str(member.id)

        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)
        role_mimo = guild.get_role(config.ROLE_MIMO_SLUZBY)

        sessions = load_json("sessions.json", {})

        if uid not in sessions or not sessions[uid]:
            await ctx.send("👮‍♂️ Nemáš aktívnu smenu.")
            return

        session = sessions[uid][-1]

        if session["end"] is not None:
            await ctx.send("👮‍♂️ Nemáš aktívnu smenu.")
            return

        # zavri otvorenú prestávku
        if session["breaks"] and session["breaks"][-1]["end"] is None:
            session["breaks"][-1]["end"] = now()

        session["end"] = now()
        save_json("sessions.json", sessions)

        await member.remove_roles(role_v, role_prest)
        await member.add_roles(role_mimo)

        await ctx.send("👮‍♂️ Odchod z práce zaznamenaný.")


async def setup(bot):
    await bot.add_cog(VratnicaCommands(bot))
