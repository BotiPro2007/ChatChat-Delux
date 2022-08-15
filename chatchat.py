import pygame
import os

hitmap_img = pygame.image.load("hitmap.png")
hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))))

map_img = pygame.image.load("map.png")
sheets = [pygame.image.load("greencatwalk.png"),#1
          pygame.image.load("bluecatwalk.png"),#2
          pygame.image.load("browncatwalk.png"),#3
          pygame.image.load("cyancatwalk.png"),#4
          pygame.image.load("greycatwalk.png"),#5
          pygame.image.load("orangecatwalk.png"),#6
          pygame.image.load("pinkcatwalk.png"),#7
          pygame.image.load("redcatwalk.png"),#8
          pygame.image.load("whitecatwalk.png"),#9
          pygame.image.load("yellowcatwalk.png"),#10
          pygame.image.load("greendogwalk.png")#11
          ]

playspace = map_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))).copy()
tick = 0
scale = 2
window = None
name_font = None
chat_font = None
resized_playspace = None
false_keys = None

def init(isClient : bool = True):
    global window, name_font, client, false_keys, chat_font
    if not isClient: os.environ["SDL_VIDEODRIVER"] = "dummy" # the server doesn't have to have a videodriver (for example: Linux server)
    pygame.init()
    client = isClient
    false_keys = pygame.key.get_pressed()
    if client:
        window = pygame.display.set_mode((playspace.get_width()*scale, playspace.get_height()*scale*2), pygame.RESIZABLE)
        name_font = pygame.font.SysFont("flixel", 32, bold=False, italic=False)
        chat_font = pygame.font.SysFont("flixel", 26, bold=False, italic=False)

class MapComponent(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((50,50)) #texture
        
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect()

    def show(self):
        self.rect = playspace.blit(self.image, (self.x, self.y))

# default is cat
class Character(pygame.sprite.Sprite):
    def __init__(self, name : str):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.sheet_id = 4
        self.sheet = sheets[self.sheet_id]
        self.image_index = 4
        self.image = self.sheet.subsurface(pygame.Rect((16*self.image_index, 0), (16, 18))) #texture
        self.rect = self.image.get_rect()
        self.any_updated = True

        self.chunk_y = 2
        self.chunk_x = 2
        self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
        self.x = 160
        self.y = 128
        self.last_step_tick = 6
        self.playspace = map_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))).copy()

    def action(self):
        pass

    def move(self, key):
        if tick - self.last_step_tick >= 6:
            if key == 0:
                if not self.rect.collidepoint((self.rect.topleft[0], 0)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery - 16] == 65280):
                    self.y -= 16
                    if self.image_index == 1: self.image_index = 0
                    elif self.image_index == 0: self.image_index = 1
                    else: self.image_index = 0
                elif self.rect.collidepoint((self.rect.topleft[0], 0)):
                    self.chunk_y -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = self.playspace.get_height()-16
            elif key == 1:
                if not self.rect.collidepoint((self.rect.bottomleft[0], self.playspace.get_height()-16)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery + 16] == 65280):
                    self.y += 16
                    if self.image_index == 2: self.image_index = 3
                    elif self.image_index == 3: self.image_index = 2
                    else: self.image_index = 2
                elif self.rect.collidepoint((self.rect.bottomleft[0], self.playspace.get_height()-16)):
                    self.chunk_y += 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = 0
            elif key == 2:
                if not self.rect.collidepoint((0, self.rect.topleft[1])) and not (self.hitmap_array[self.rect.centerx - 16][self.rect.centery] == 65280):
                    self.x -= 16
                    if self.image_index == 4: self.image_index = 5
                    elif self.image_index == 5: self.image_index = 4
                    else: self.image_index = 4
                elif self.rect.collidepoint((0, self.rect.topleft[1])):
                    self.chunk_x -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.x = self.playspace.get_width()-16
            elif key == 3:
                if not self.rect.collidepoint((self.playspace.get_width()-4, self.rect.topright[1])) and not (self.hitmap_array[self.rect.centerx + 16][self.rect.centery] == 65280):
                    self.x += 16
                    if self.image_index == 6: self.image_index = 7
                    elif self.image_index == 7: self.image_index = 6
                    else: self.image_index = 6
                elif self.rect.collidepoint((0+self.playspace.get_width()-4, self.rect.topright[1])):
                    self.chunk_x += 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.x = 0
            else:
                return

            #finaly:
            self.any_updated = True
            self.last_step_tick = tick

    def show(self):
        self.image = self.sheet.subsurface(pygame.Rect((16*self.image_index, 0), (16, 18)))
        self.rect = self.playspace.blit(self.image, (self.x, self.y-2))

class ClientCharacter(Character):
    def __init__(self, name : str, id : int = 0):
        Character.__init__(self, name)

        posx = min(max(self.rect.centerx-80, 8), 152)
        posy = min(max(self.rect.centery-48, 8), 88)
        self.fov_rect = pygame.Rect((posx, posy), (160, 96))
        self.fov = self.playspace.subsurface(self.fov_rect)
        self.nameX = self.rect.centerx-posx - (len(self.name) * 1.2)
        self.nameY = self.rect.centery-posy+7.5
        self.resized_playspace = pygame.transform.scale(self.fov, (320*scale, 192*scale))
        
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

        
    def onUpdate(self):
        self.show()
        posx = min(max(self.rect.centerx-80, 8), 152)
        posy = min(max(self.rect.centery-48, 8), 88)
        self.fov_rect = pygame.Rect((posx, posy), (160, 96))
        self.fov = self.playspace.subsurface(self.fov_rect)
        self.nameX = self.rect.centerx-posx - name_font.size(self.name)[0]/7.5
        self.nameY = self.rect.centery+1-posy+7.5
        self.resized_playspace = pygame.transform.scale(self.fov, (320*scale, 192*scale))
        self.show_name(self.resized_playspace, (self.nameX, self.nameY))

    def show_name(self, surface : pygame.Surface, at : tuple):
        surface.blit(name_font.render(self.name, False, (255,255,255)), (at[0]*(scale*2), (at[1]*(scale*2))))

class Component(pygame.sprite.Sprite):
    def __init__(self, text : str, pos, size, color, hovering : bool =True, outline : tuple = (127, 127,127)):
        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]+5
        self.y = pos[1]+5
        self.text = text
        self.image = pygame.Surface((size[0]-5, size[1]-5)) #texture
        self.image.fill(color)
        self.outline = pygame.Surface(size)
        self.outline.fill(outline) 
        self.use_hovering = hovering
        self.hoverSurf = pygame.Surface((size[0]-5, size[1]-5))
        self.hoverSurf.fill((min(color[0] - 50, 255), min(color[1] - 50, 255), min(color[2] - 50,255)))
        self.hovering = False

        self.clicking = False
        self.rect = self.image.get_rect()

    def onUpdate(self):
        if client: self.show()
        m = pygame.mouse.get_pos()
        size = self.image.get_size()
        if m[0] <= self.x+size[0] and m[0] >= self.x and m[1] <= self.y + size[1] and m[1] >= self.y:
            self.onHover()
            self.hovering = True
            if pygame.mouse.get_pressed()[0]:
                self.clicking = True
            if not pygame.mouse.get_pressed()[0] and self.clicking:
                self.clicking = False
                self.onClick()
        else: self.hovering = False

    def onHover(self):
        pass

    def onClick(self):
        pass

    def show(self):
        window.blit(self.outline, (self.x-5, self.y-5))
        if self.hovering and self.use_hovering: self.rect = window.blit(self.hoverSurf, (self.x, self.y))
        else: self.rect = window.blit(self.image, (self.x, self.y))
        window.blit(chat_font.render(self.text, True, (0,0,0)), (self.x, self.y))

class Input(Component):

    def __init__(self, text : str, pos, size, color):
        Component.__init__(self, text, pos, size, color)

        self.text = ""

    def onUpdate(self):
        Component.onUpdate(self)

        for event in pygame.event.get(eventtype=pygame.KEYUP):
            if event.key == pygame.K_RETURN:
                self.onSend()
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0: self.text = self.text[:-1]
            else:
                self.onTypeing(event.unicode)

    def onSend(self):
        pass # client send here

    def onTypeing(self, key):
        self.text += key

class ChatMessage:
    def __init__(self, author : str, content : str, author_color = (0,0,0)):

        self.content = content
        self.author = author
        self.author_color = author_color
        self.formatted_content = f"{author} : {content}"

class Chat(Component):
    def __init__(self, title : str, pos, size, title_color):
        Component.__init__(self, title, pos, size, title_color, False)
        self.messages = [] #contains ChatMessage
        self.font_size = 13
        self.space_btw_msgs = 5

    def add_message(self, message : ChatMessage):
        self.messages.append(message)

    def show(self):
        Component.show(self)

        y = self.y + self.font_size * 3 #space from title
        for message in self.messages[-16:]: # top 16 msgs
            window.blit(chat_font.render(message.author, True, message.author_color), (self.x, y))
            window.blit(chat_font.render(" : "+message.content, True, (0,0,0)), (self.x+(chat_font.size(message.author)[0]), y))
            y += self.font_size + self.space_btw_msgs

def onUpdate(update_list : list):
    global playspace, tick
    for event in pygame.event.get(eventtype=pygame.QUIT): return True
        
    for component in update_list:
        if isinstance(component,Component) and client: component.onUpdate()

    if client: pygame.display.update()
    pygame.time.Clock().tick(60)
    tick +=1
    if client: window.fill((0,0,100))
    return False

def color_by_sheet_id(id : int):
    color = (0,0,0)
    if id == 0: color = (143, 180, 42)
    elif id == 1: color = (54, 139, 230)
    elif id == 2: color = (137, 91, 33)
    elif id == 3: color = (165, 206, 230)
    elif id == 4: color = (135, 135, 135)
    elif id == 5: color = (215, 210, 53)
    elif id == 6: color = (137, 91, 33)
    elif id == 7: color = (198, 98, 118)
    elif id == 8: color = (159, 38, 52)
    elif id == 9: color = (255, 255, 255)
    elif id == 10: color = (241, 205, 101)
    
    return color
