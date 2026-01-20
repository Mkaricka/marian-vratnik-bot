from datetime import date
from core.attendance import calculate_user_stats
import config

async def check_inactivity(bot):
    for guild in bot.guilds:
        role_v = guild.get_role(config.ROLE_V_SLUZBE)
        role_pn = guild.get_role(config.ROLE_PN)
        role_dov = guild.get_role(config.ROLE_DOVOLENKA)

        for m in guild.members:
            if m.bot:
                continue

            if role_pn in m.roles or role_dov in m.roles:
                continue

            stats = calculate_user_stats(str(m.id), mode="today")

            if stats["shifts"] == 0:
                try:
                    await m.send(
                        "⚠️ **Upozornenie**\n"
                        "Dnes nemáš evidovanú žiadnu pracovnú aktivitu.\n"
                        "Ak pracuješ, nezabudni použiť `!pracujem`."
                    )
                except:
                    pass
