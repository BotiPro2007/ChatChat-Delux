import pygame, chatchat, pickle, socket, threading

chatchat.init()

icon = pygame.image.load("logo.png")
name = "Szörme"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 11102))
s.send(pickle.dumps({"name":name}))
pygame.display.set_caption("ChatChat // DELUX //")
pygame.display.set_icon(icon)
playing = True

me = chatchat.ClientCharacter(name)
chat_input = chatchat.Input("Itt lesz majd a chat", (chatchat.window.get_width(), chatchat.window.get_height()), (1000,50), (255,255,255))
updateables = [chat_input]

def receive():
    global playing
    while playing:
        data = pickle.loads(s.recv(50000))
        me.playspace = chatchat.map_img.subsurface(pygame.Rect((320*me.chunk_x, 192*me.chunk_y), (320, 192))).copy()
        if data.get("me") != None:
            d = data["me"]
            if d.get("sheet") != None: me.sheet = chatchat.id_to_sheet(d["sheet"])
            if d.get("x") != None: me.x = d["x"]
            if d.get("y") != None: me.y = d["y"]
            if d.get("image_index") != None: me.image_index = d["image_index"]
        if data.get("chunk_x") != None: me.chunk_x = data["chunk_x"]
        if data.get("chunk_y") != None: me.chunk_y = data["chunk_y"]
        others = []
        if data.get("others") != None:
            for d in data["others"]:
                other = chatchat.ClientCharacter(d["name"])
                other.playspace = me.playspace
                if d.get("sheet") != None: other.sheet = chatchat.id_to_sheet(d["sheet"])
                if d.get("x") != None: other.x = d["x"]
                if d.get("y") != None: other.y = d["y"]
                if d.get("image_index") != None: other.image_index = d["image_index"]
                if data.get("chunk_x") != None: other.chunk_x = data["chunk_x"]
                if data.get("chunk_y") != None: other.chunk_y = data["chunk_y"]
                other.onUpdate()
                me.playspace = other.playspace
                others.append(other)
        me.onUpdate()
        for other in others:
            name_pos = (other.rect.centerx-(me.rect.centerx-80) - (len(other.name) * 1.2)+(me.rect.centerx - me.fov_rect.centerx), other.rect.centery-(me.rect.centery-48)+10+((me.rect.centery - me.fov_rect.centery)))
            other.show_name(me.resized_playspace, name_pos)
                
threading.Thread(target=receive).start()

try:
    while playing:
        if chatchat.onUpdate(updateables): playing = False
        keys = pygame.key.get_pressed()
        if keys[me.up]: s.send(pickle.dumps({"key":0}))
        elif keys[me.down]: s.send(pickle.dumps({"key":1}))
        elif keys[me.left]: s.send(pickle.dumps({"key":2}))
        elif keys[me.right]: s.send(pickle.dumps({"key":3}))
        chatchat.window.blit(me.resized_playspace, (0,0))
except KeyboardInterrupt: playing = False

print("Bye!")
