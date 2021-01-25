import DSBOT


async def checkCens(message, client):
    msg = str(message.clean_content).lower()
    if msg in DSBOT.badwords or msg.count("оху") >= 1 or msg.count("аху") or msg.count("еба") >= 1 or msg.count(
            "ебл") >= 1 or msg.count("хуй") >= 1:
        await doCens(message, client)
    else:
        return True


async def doCens(message, client):
    await message.delete()
    print("Сообщение пользователся " + str(message.author) + " удалено.")
    channel = client.get_channel(message.channel.id)
    await channel.send("Сообщение пользователя " + str(message.author) + " удалено. \nПричина: нецензурная "
                                                                         "брань")
