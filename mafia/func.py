import discord
import db

global database, cur, game
database = db.con
cur = database.cursor()
game = "MAFIA"


async def cmd_make_room(message, channel, guild, command):
    if guild is None:
        await channel.send("서버에서만 사용할 수 있는 명령어입니다.")
        return None

    sql = "select * from server"
    cur.execute(sql)
    datas = cur.fetchall()
    database.commit()

    game_id = 0
    channel_id = 0
    for now in datas :
        if now[0] == guild.id :
            game_id = now[1]
            channel_id = now[2]
            break

    old_categories = set(guild.categories)

    if game_id != 0 :
        for now in old_categories :
            if now.id == game_id :
                for now2 in now.channels :
                    if now2.id == channel_id :
                        await channel.send("이미 대기실이 만들어진 서버입니다 : "+str(game_id))
                        return None
                sql = "delete from server where id = %s"
                cur.execute(sql, guild.id)
                database.commit()
                await make_wait(channel, guild, now)
                return None

        sql = "delete from server where id = %s"
        cur.execute(sql, guild.id)
        database.commit()

    await guild.create_category(game)
    new_categories = set(guild.categories)

    count = 0
    game_id = 0
    diff_categories = list(new_categories - old_categories)
    for now_category in diff_categories :
        if str(now_category) == game :
            count = count + 1
            game_id = now_category

    if count > 1 :
        await channel.send("카테고리가 생성되는 도중에 같은 이름의 카테고리가 만들어졌습니다.")
        return None

    await make_wait(channel, guild, game_id)


async def make_wait(channel, guild, category):
    old_channels = set(category.channels)
    await guild.create_voice_channel("대기실", category=category)
    new_channels = set(category.channels)
    diff_channels = list(new_channels - old_channels)

    channel_id = 0
    count = 0
    for now_channel in diff_channels:
        if str(now_channel) == "대기실":
            count = count + 1
            channel_id = now_channel

    if count > 1:
        await channel.send("대기실이 생성되는 도중에 같은 이름의 대기실이 만들어졌습니다.")
        return None

    await channel.send("성공적으로 대기실을 만들었습니다.")
    sql = "insert into server(id,game,wait) values (%s, %s, %s)"
    cur.execute(sql, (guild.id, category.id, channel_id.id))
    database.commit()

    return None


async def cmd_spec(message, channel, guild, command):
    author = message.author

    sql = "select * from player"
    cur.execute(sql)
    datas = cur.fetchall()
    database.commit()

    for now in datas:
        if now[0] == author.id :
            if now[2] == -1 :
                sql = "delete from player where id = %s"
                cur.execute(sql,(now[0]))
                database.commit()
                await channel.send(author.mention+"님이 관전 상태에서 벗어납니다.")
            else :
                await channel.send(author.mention+"님은 이미 게임 중입니다.")

            return None

    sql = "insert into player(id,team) values (%s, %s)"
    cur.execute(sql, (author.id, -1))
    database.commit()

    await channel.send(author.mention+"님이 이제 관전 상태입니다.")


