import config


async def set_mimo_prace(member):
    await member.remove_roles(
        member.guild.get_role(config.ROLE_V_SLUZBE),
        member.guild.get_role(config.ROLE_PRESTAVKA),
        member.guild.get_role(config.ROLE_PN),
        member.guild.get_role(config.ROLE_DOVOLENKA),
    )
    await member.add_roles(member.guild.get_role(config.ROLE_MIMO_SLUZBY))


async def set_pn(member):
    await set_clean(member)
    await member.add_roles(member.guild.get_role(config.ROLE_PN))


async def set_dovolenka(member):
    await set_clean(member)
    await member.add_roles(member.guild.get_role(config.ROLE_DOVOLENKA))


async def set_clean(member):
    await member.remove_roles(
        member.guild.get_role(config.ROLE_V_SLUZBE),
        member.guild.get_role(config.ROLE_PRESTAVKA),
        member.guild.get_role(config.ROLE_MIMO_SLUZBY),
        member.guild.get_role(config.ROLE_PN),
        member.guild.get_role(config.ROLE_DOVOLENKA),
    )
