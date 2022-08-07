import socket, threading, pickle, pygame, random,chatchat

chatchat.init(isClient = False)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 11102))
s.listen(5)
runing = True
players = {}

def receive(client, player : chatchat.Character):
    try:
        while True:
            data = pickle.loads(client.recv(1024))
            #print(data)
            if data.get("name") != None and data.get("name") != "L.." and player.name == "L..":
                player.name = data["name"]
                print(f"{data['name']} joined to the party!")
                client.send(pickle.dumps({"sheet":player.sheet_id}))
            if data.get("key") != None: player.key = int(data["key"])
            player.onUpdate()
            player.key = -1
            players.update({client: player})
    except (ConnectionResetError, EOFError, ConnectionAbortedError, BrokenPipeError):
        print(player.name + " left the server!")
        players.pop(client)
        client.close()
        return
        
def accepting():
    while True:
        try:
            clientsocket, address = s.accept()
            player_id = random.randint(0,30)+random.randint(0,30)
            temp_cat = chatchat.Character("L..", id = player_id)
            threading.Thread(target=receive, args=(clientsocket, temp_cat)).start()
        except KeyboardInterrupt:
            s.close()
            print("bye!")

threading.Thread(target=accepting).start()
try:
    while True:
        chatchat.onUpdate([])
        if chatchat.tick % 3 == 0:
            for c in players.keys():
                player = players[c]
                others = []
                for other in players.values():
                    if other.chunk_y == player.chunk_y and other.chunk_x == player.chunk_x and not (other.x == player.x and other.y == player.y):
                        others.append({"name": other.name,"x": other.x, "y": other.y, "image_index": other.image_index, "sheet":other.sheet_id})
                        if other.key != -1: have_to_send = True
                playerdata = {"me":{"x": player.x, "y": player.y, "image_index": player.image_index}, "others":others, "chunk_x":player.chunk_x, "chunk_y":player.chunk_y}
                c.send(pickle.dumps(playerdata))
        for c in players.keys():
            player = players[c]
            if player.key == -1 and player.image_index % 2 > 0 and chatchat.tick - player.last_step_tick > 6:
                player.image_index -= 1
                players.update({c:player})
    
except (ConnectionResetError, EOFError,ConnectionAbortedError, BrokenPipeError) as e:
    print(e)
    c.close()

except (RuntimeError): pass

except (KeyboardInterrupt):
    print("Goodbye Server!")
    for client in players.keys(): client.close()

        
