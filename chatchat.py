import pygame

hitmap_img = pygame.image.load("hitmap.png")
hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))))

map_img = pygame.image.load("map.png")
cat_img = pygame.image.load("greencat.png")
dog_img = pygame.image.load("greendog.png")

playspace = map_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))).copy()
tick = 0
scale = 2
window = None
globalFont = None
resized_playspace = None
false_keys = None

def init(window_default_size : tuple = None, isClient : bool = True):
    global window, globalFont, client, false_keys
    client = isClient
    pygame.init()
    false_keys = pygame.key.get_pressed()
    if client:
        if window_default_size == None: window = pygame.display.set_mode((playspace.get_width()*scale, playspace.get_height()*scale), pygame.RESIZABLE)
        else: window = pygame.display.set_mode((window_default_size*scale, window_default_size*scale), pygame.RESIZABLE)
        globalFont = pygame.font.SysFont("flixel", 24, bold=True, italic=False)

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

class Character(pygame.sprite.Sprite):
    def __init__(self, name : str, id : int = 0):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.name = name
        self.sheet = cat_img
        self.sheet_id = 0
        self.image_index = 4
        self.image = self.sheet.subsurface(pygame.Rect((16*self.image_index, 0), (16, 16))) #texture

        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.key = -1              #only used when it's on server

        self.rect = self.image.get_rect()
        fov_rect = pygame.Rect((min(max(self.rect.centerx-80, 8), 152), min(max(self.rect.centery-48, 8), 88)), (160, 96))
        self.fov = playspace.subsurface(fov_rect)

        self.chunk_y = 2
        self.chunk_x = 2
        self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
        self.x = 160
        self.y = 128
        self.last_step_tick = 6
        self.playspace = map_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))).copy()

    def onUpdate(self):
        self.move()
        self.show()

    def action(self):
        pass

    def move(self):
        if tick - self.last_step_tick >= 6:
            if self.key == 0:
                if not self.rect.collidepoint((self.rect.topleft[0], 0)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery - 16] == 65280):
                    self.y -= 16
                    if self.image_index == 1: self.image_index = 0
                    elif self.image_index == 0: self.image_index = 1
                    else: self.image_index = 0
                elif self.rect.collidepoint((self.rect.topleft[0], 0)):
                    self.chunk_y -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = self.playspace.get_height()-16
            elif self.key == 1:
                if not self.rect.collidepoint((self.rect.bottomleft[0], self.playspace.get_height()-16)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery + 16] == 65280):
                    self.y += 16
                    if self.image_index == 2: self.image_index = 3
                    elif self.image_index == 3: self.image_index = 2
                    else: self.image_index = 2
                elif self.rect.collidepoint((self.rect.bottomleft[0], self.playspace.get_height()-16)):
                    self.chunk_y += 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = 0
            elif self.key == 2:
                if not self.rect.collidepoint((0, self.rect.topleft[1])) and not (self.hitmap_array[self.rect.centerx - 16][self.rect.centery] == 65280):
                    self.x -= 16
                    if self.image_index == 4: self.image_index = 5
                    elif self.image_index == 5: self.image_index = 4
                    else: self.image_index = 4
                elif self.rect.collidepoint((0, self.rect.topleft[1])):
                    self.chunk_x -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.x = self.playspace.get_width()-16
            elif self.key == 3:
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
                self.key = -1
                return

            #finaly:
            self.key = -1
            self.last_step_tick = tick

    def show(self):
        self.image = self.sheet.subsurface(pygame.Rect((16*self.image_index, 0), (16, 16)))
        self.rect = self.playspace.blit(self.image, (self.x, self.y))

class ClientCharacter(Character):
    def __init__(self, name : str, id : int = 0):
        Character.__init__(self, name)
        self.resized_playspace = pygame.transform.scale(self.fov, (320*scale, 192*scale))
        self.fov_rect = pygame.Rect(0, 0, 0, 0)
        
    def onUpdate(self):
        self.show()
        posx = min(max(self.rect.centerx-80, 8), 152)
        posy = min(max(self.rect.centery-48, 8), 88)
        self.fov_rect = pygame.Rect((posx, posy), (160, 96))
        self.fov = self.playspace.subsurface(self.fov_rect)
        self.nameX = self.rect.centerx-posx - (len(self.name) * 1.2)
        self.nameY = self.rect.centery-posy+10
        self.resized_playspace = pygame.transform.scale(self.fov, (320*scale, 192*scale))
        self.show_name(self.resized_playspace, (self.nameX, self.nameY))

    def show_name(self, surface : pygame.Surface, at : tuple):
        surface.blit(globalFont.render(self.name, True, (255,255,255)), (at[0]*(scale*2), (at[1]*(scale*2))))
    
class Dog(ClientCharacter):
    def __init__(self,name : str, id : int = 0):
        Character.__init__(self, name, id)
        self.sheet = dog_img
        
class Cat(ClientCharacter):
    def __init__(self,name : str, id : int = 0):
        Character.__init__(self, name, id)
        

class Component(pygame.sprite.Sprite):
    def __init__(self, text : str, pos, size, color, fixed=True):
        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]
        self.y = pos[1]
        self.text = text
        self.isFixed = fixed
        self.image = pygame.Surface(size) #texture
        self.image.fill(color)
        self.hoverSurf = pygame.Surface(size)
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
        if self.hovering: self.rect = window.blit(self.hoverSurf, (self.x, self.y))
        else: self.rect = window.blit(self.image, (self.x, self.y))
        window.blit(globalFont.render(self.text, True, (0,0,0)), (self.x, self.y))

class Input(Component):

    def __init__(self, text : str, pos, size, color, fixed=True):
        Component.__init__(self, text, pos, size, color)

        self.typeing = False
        self.text = ""
        
    def onClick(self):
        self.typeing = not self.typeing
        if self.typeing: pygame.key.start_text_input()
        else: pygame.key.stop_text_input()
        print("I am clicked: "+str(self.typeing))

    def onUpdate(self):
        Component.onUpdate(self)

        for event in pygame.event.get(eventtype=pygame.TEXTINPUT): self.onTypeing(event.text)

    def onTypeing(self, key):
        if self.typeing: self.text += key

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

def id_to_sheet(id : int):
    if id == 0: return cat_img
    elif id == 1: return dog_img
    return
