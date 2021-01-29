async def doCens(message, client):
    await message.delete()
    print("Сообщение пользователся " + str(message.author) + " удалено.")
    channel = client.get_channel(message.channel.id)
    await channel.send("Сообщение пользователя " + str(message.author) + " удалено. \nПричина: нецензурная "
                                                                         "брань")


def unique(it):
    s = set()
    for x in it:
        if x not in s:
            s.add(x)
            yield x
