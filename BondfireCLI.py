from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText, MessageDirection)
import maskpass

roomList = []
chatMessages = []
count = 1
inputHomeServer = "matrix.org"
inputUserID = input("Enter your user ID: ")
inputPasswordID = maskpass.askpass("Enter your password: ")

async_client = AsyncClient(
    "https://"+inputHomeServer, "@"+inputUserID+":"+inputHomeServer
)

async def round2():
        chatMessages.clear()
        print(*roomList, sep="\n")
        inputRoomID = input("Enter the room ID #: ")
        roomMessages = await async_client.room_messages(
            start="", room_id=roomList[int(inputRoomID)]["roomID"], limit=100
        )
        for each in roomMessages.chunk:
            if type(each) == RoomMessageText:
                chatMessages.append(each.body)

        chatMessages.reverse()
        print(*chatMessages, sep="\n")
                

        inputMessage = input("Enter message: ")
        
        await async_client.room_send(
            room_id=roomList[int(inputRoomID)]["roomID"],
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": inputMessage},
        )
        await async_client.close()
        print("sent: " + inputMessage)

async def main():
    response = await async_client.login(inputPasswordID)
    sync_response = await async_client.sync(30000)
    room = ""
    joins = sync_response.rooms.join
    count = 0
    for room_id in joins:
        room = async_client.rooms[room_id]
        if room_id not in roomList:
            roomList.append({"roomID#": count,"roomID": room_id,"Room Name": room.display_name})
            count += 1
    Running = True
    await round2()

    while Running:
        if input("do you want to send another message? (y/n) ") == "y":
            await round2()
        else:
            print("Goodbye!")
            await async_client.close()
            Running = False
            exit()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())