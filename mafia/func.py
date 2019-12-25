import discord


async def make_room(message, channel, guild, command):
    if guild is None:
        await channel.send("서버에서만 사용할 수 있는 명령어입니다.")
        return None

    categories = guild.categories
    okay_category = False
    for now in categories:
        if str(now) == "MAFIA":
            okay_category = True
            break

    if okay_category:
        await channel.send("MAFIA 카테고리가 이미 존재합니다.")
        return None

    await guild.create_category("MAFIA")

    categories = guild.categories
    count = 0
    category_id = 0
    for now in categories:
        if str(now) == "MAFIA":
            category_id = now
            count = count + 1

    if count != 1:
        await channel.send("MAFIA 카테고리가 이미 존재합니다.")
        return None

    await guild.create_voice_channel("대기방", category=category_id)
    await channel.send("성공적으로 방을 만들었습니다!!")
    return None


async def start_game(message, channel, guild, command):
