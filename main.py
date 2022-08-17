import pygame, chatchat, pickle, socket, threading, sys

chatchat.init()

icon = pygame.image.load("logo.png")
name = "asdasdasd"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("videohun.hu", 11102))
s.send(pickle.dumps({"name":name}))
pygame.display.set_caption("ChatChat // DELUX //")
pygame.display.set_icon(icon)

playing = True
fullscreen = False

me = chatchat.ClientCharacter(name)
chat_input = chatchat.Input("Placeholder", (0, chatchat.playspace.get_height()*chatchat.scale*2-50), (chatchat.playspace.get_width()*chatchat.scale,50), (255,255,255))
chat_input.onSend = lambda: s.send(pickle.dumps({"message" : chat_input.text}))
chat = chatchat.Chat("CHAT "+"."*50, (0, chatchat.playspace.get_height()*chatchat.scale), (chatchat.playspace.get_width()*chatchat.scale, chatchat.playspace.get_height()*chatchat.scale-50), (255,255,255))
#max 16 msg
updateables = [chat_input, chat]

def receive():
    global playing
    print("\n", end="\r")
    while playing:
        data = pickle.loads(s.recv(50000))
        print(data)
        if data.get("chunk_x") != None: me.chunk_x = data["chunk_x"]
        if data.get("chunk_y") != None: me.chunk_y = data["chunk_y"]
        me.playspace = chatchat.map_img.subsurface(pygame.Rect((320*me.chunk_x, 192*me.chunk_y), (320, 192))).copy()
        if data.get("sheet") != None: me.sheet = chatchat.sheets[data["sheet"]]
        if data.get("me") != None:
            d = data["me"]
            if d.get("x") != None: me.x = d["x"]
            if d.get("y") != None: me.y = d["y"]
            if d.get("image_index") != None: me.image_index = d["image_index"]
        if data.get("new_messages") != None:
            for author, contents in data["new_messages"].items():
                for content in contents[1:]:
                    message = chatchat.ChatMessage(author, content, chatchat.color_by_sheet_id(contents[0]))
                    chat.add_message(message)
        others = []
        if data.get("others") != None:
            for d in data["others"]:
                other = chatchat.ClientCharacter(d["name"])
                other.playspace = me.playspace
                if d.get("sheet") != None: other.sheet = chatchat.sheets[d["sheet"]]
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
            name_size = chatchat.name_font.size(other.name)[0]/7.5
            name_pos = (other.rect.centerx-(me.rect.centerx-80) - (name_size)+(me.rect.centerx - me.fov_rect.centerx), other.rect.centery+1-(me.rect.centery+1-48)+7.5+((me.rect.centery+1 - me.fov_rect.centery)))
            other.show_name(me.resized_playspace, name_pos)

threading.Thread(target=receive).start()

try:
    while playing:
        if chatchat.onUpdate(updateables):
            playing = False
            s.close()
        keys = pygame.key.get_pressed()
        if keys[me.up]: s.send(pickle.dumps({"key":0}))
        elif keys[me.down]: s.send(pickle.dumps({"key":1}))
        elif keys[me.left]: s.send(pickle.dumps({"key":2}))
        elif keys[me.right]: s.send(pickle.dumps({"key":3}))
        elif keys[pygame.K_F11]:
            chatchat.window = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.FULLSCREEN)
            
        chatchat.window.blit(me.resized_playspace, (0,0))
except (KeyboardInterrupt, ConnectionResetError, EOFError, ConnectionAbortedError, BrokenPipeError, OSError):
    playing = False
    s.close()
    
print("Bye!")
sys.exit()
