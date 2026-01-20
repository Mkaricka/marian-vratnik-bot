import discord
from discord.ext import commands
import config
from storage.json_store import load_json

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# READY EVENT – JEMNÁ SYNC
# =========================
@bot.event
async def on_ready():
    print("===================================")
    print(f"Vrátnik Marián je online ako {bot.user}")
    print("Bot je pripravený.")
    print("===================================")

    for guild in bot.guilds:
        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_prest = guild.get_role(config.ROLE_PRESTAVKA)
        role_mimo = guild.get_role(config.ROLE_MIMO_SLUZBY)
        role_pn = guild.get_role(config.ROLE_PN)
        role_dov = guild.get_role(config.ROLE_DOVOLENKA)

        for member in guild.members:
            if member.bot:
                continue

            roles = member.roles

            # 🔒 ak má akýkoľvek vedomý stav, NEROB NIČ
            if (
                role_v in roles
                or role_prest in roles
                or role_pn in roles
                or role_dov in roles
            ):
                continue

            # ⚪ inak default: Mimo práce
            if role_mimo not in roles:
                await member.add_roles(role_mimo)
                print(f"{member.display_name} -> Mimo práce (sync)")

    print("✔️ Synchronizácia stavov dokončená.")

# =========================
# NEW MEMBER JOIN
# =========================
@bot.event
async def on_member_join(member):
    role_mimo = member.guild.get_role(config.ROLE_MIMO_SLUZBY)
    if role_mimo:
        await member.add_roles(role_mimo)
        print(f"{member.display_name} -> Mimo práce (join)")

# =========================
# LOAD COMMANDS (MODULÁRNE)
# =========================
@bot.event
async def setup_hook():
    await bot.load_extension("commands.vratnica_commands")
    await bot.load_extension("commands.pn_commands")
    await bot.load_extension("commands.dovolenka_commands")
    await bot.load_extension("commands.spravca_commands")
    await bot.load_extension("commands.info_commands")

# =========================
# TEST COMMAND
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("👮‍♂️ Vrátnik Marián: Som online a fungujem.")

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    bot.run(config.TOKEN)
