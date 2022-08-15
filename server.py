import socket, threading, pickle, pygame, random,chatchat

chatchat.init(isClient = False)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 11102))
s.listen(5)
runing = True
players = {}
new_messages = {} #(author_name, author_sheet/color) : ["message", "message2", ...]

#message:      [color,      message        ]
join_message = [-1, "Joined to the server!"]
welcome_message = [-1, "Welcome on our ChatChat server!", "Have fun and be kind!"]
leave_message = [-1, "Left the server!"]

def get_message(message, sheet_id):
    if type(message) == str and message.strip() != "":
        return [player.sheet_id, message.strip()]
    elif type(data["message"]) == tuple and type(data["message"][0]) == str:
        return list(message).insert(0, player.sheet_id)
    else: return None

def receive(client, player : chatchat.Character):
    try:
        while True:
            data = pickle.loads(client.recv(1024))
            #print(data)
            if data.get("name") != None:
                player.name = data["name"]
                player.sheet_id = random.randint(0, 9)
                new_messages.update({player.name : join_message})
                print(player.name+" : "+join_message[1])
                client.send(pickle.dumps({"sheet":player.sheet_id, "new_messages":{"SERVER":welcome_message}}))
                print("MOTD sended to the client!")
            if data.get("key") != None: player.move(data["key"])
            if data.get("message") != None:
                message = get_message(data["message"], player.sheet_id)
                if message != None:
                    new_messages.update({player.name : message})
                    print(player.name+" : "+message[1])
            
            player.show()
            players.update({client: player})
    except (ConnectionResetError, EOFError, ConnectionAbortedError, BrokenPipeError, OSError):
        new_messages.update({player.name : leave_message})
        print(player.name+" : "+leave_message[1])
        players.pop(client)
        client.close()
        return
        
def accepting():
    while True:
        try:
            clientsocket, address = s.accept()
            temp_cat = chatchat.Character("L..")
            threading.Thread(target=receive, args=(clientsocket, temp_cat)).start()
        except KeyboardInterrupt:
            s.close()
            print("bye!")

threading.Thread(target=accepting).start()
while True:
    try:
        chatchat.onUpdate([])
        if chatchat.tick % 3 == 0:
            for c, player in players.items():
                others = []
                send_packet = player.any_updated
                for other in players.values():
                    if other.chunk_y == player.chunk_y and other.chunk_x == player.chunk_x and not (other.x == player.x and other.y == player.y):
                        others.append({"name": other.name,"x": other.x, "y": other.y, "image_index": other.image_index, "sheet":other.sheet_id})
                        if other.any_updated:
                            send_packet = True
                playerdata = {"me":{"x": player.x, "y": player.y, "image_index": player.image_index}, "others":others, "chunk_x":player.chunk_x, "chunk_y":player.chunk_y}
                if len(new_messages) > 0:
                    playerdata.update({"new_messages" : new_messages})
                    send_packet = True
                if send_packet: c.send(pickle.dumps(playerdata))
            new_messages = {}
            for c, player in players.items():
                player.any_updated = False
                if player.image_index % 2 > 0 and chatchat.tick - player.last_step_tick > 11:
                    player.image_index -= 1
                    player.any_updated = True
                    players.update({c:player})
    
    except (ConnectionResetError, EOFError,ConnectionAbortedError, BrokenPipeError, OSError) as e:
        c.close()

    except (RuntimeError): pass

    except (KeyboardInterrupt):
    	print("Goodbye Server!")
    	for client in players.keys(): client.close()
