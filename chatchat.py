import pygame

pygame.init()

map_img = pygame.image.load("map.png")
hitmap_img = pygame.image.load("hitmap.png")
"""
walls = [[(21, 28), 0], [(0, 28), 1], [(0, 28), 2], [(0, 28), 3]]

Image.frombuffer("RGBX", (16,16),map_img.subsurface(pygame.Rect((1825, 1), (16, 16))).get_buffer().raw).show()

for row in walls:
    for cube in range(row[0][0], row[0][1]):
        cube = cube*16
        map_img.subsurface(pygame.Rect((1602+cube, 2+row[1]*16), (16, 16)))
        #pyscreeze.locateAll()
"""

scale = 2
cat = pygame.image.load("greencat.png")
icon = pygame.image.load("logo.png")
#icon = pygame.transform.scale(cat.subsurface(pygame.Rect((16*4, 0+2), (8, 8))), (35, 35))
playspace = map_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))).copy() #(156, 96)

hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*2, 192*2), (320, 192))))
#playspace.fill((0,0,0))
d = pygame.display.set_mode((playspace.get_width()*scale, playspace.get_height()*scale), pygame.RESIZABLE)
pygame.display.set_caption("ChatChat // DELUX //")
pygame.display.set_icon(icon)
playing = True
start_x = 0
tick = 0
#globalFont = pygame.font.Font("fixedsys.fon", 260)
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
        self.rect = playspace.blit(self.image, (self.x + start_x, self.y))

class Wall(MapComponent):
    def __init__(self, pos):
        MapComponent.__init__(self, pos)

class Character(pygame.sprite.Sprite):
    def __init__(self, name : str):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.jumping = False
        self.image_index = 4
        self.image = cat.subsurface(pygame.Rect((16*self.image_index, 0), (16, 16))) #texture

        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

        self.rect = self.image.get_rect()

        self.chunk_y = 2
        self.chunk_x = 2
        self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
        self.x = 160
        self.nameX = self.rect.centerx - (len(self.name) * 5)
        self.y = 128

    def onUpdate(self):
        self.move()
        self.show()

    def action(self):
        pass

    def move(self):
        if tick % 3 == 0:
            keys = pygame.key.get_pressed()
            if keys[self.up]:
                if not self.rect.collidepoint((self.rect.topleft[0], 0)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery - 16] == 65280):
                    self.y -= 16
                    if self.image_index == 1: self.image_index = 0
                    elif self.image_index == 0: self.image_index = 1
                    else: self.image_index = 0
                    return
                elif self.rect.collidepoint((self.rect.topleft[0], 0)):
                    self.chunk_y -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = playspace.get_height()-16
                    return
            if keys[self.down]:
                if not self.rect.collidepoint((self.rect.bottomleft[0], playspace.get_height()-16)) and not (self.hitmap_array[self.rect.centerx][self.rect.centery + 16] == 65280):
                    self.y += 16
                    if self.image_index == 2: self.image_index = 3
                    elif self.image_index == 3: self.image_index = 2
                    else: self.image_index = 2
                    return
                elif self.rect.collidepoint((self.rect.bottomleft[0], playspace.get_height()-16)):
                    self.chunk_y += 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.y = 0
                    return
            if keys[self.left]:
                if not self.rect.collidepoint((start_x, self.rect.topleft[1])) and not (self.hitmap_array[self.rect.centerx - 16][self.rect.centery] == 65280):
                    self.x -= 16
                    if self.image_index == 4: self.image_index = 5
                    elif self.image_index == 5: self.image_index = 4
                    else: self.image_index = 4
                    return
                elif self.rect.collidepoint((start_x, self.rect.topleft[1])):
                    self.chunk_x -= 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.x = start_x+playspace.get_width()-16
                    return
            if keys[self.right]:
                if not self.rect.collidepoint((start_x+playspace.get_width()-4, self.rect.topright[1])) and not (self.hitmap_array[self.rect.centerx + 16][self.rect.centery] == 65280):
                    self.x += 16
                    if self.image_index == 6: self.image_index = 7
                    elif self.image_index == 7: self.image_index = 6
                    else: self.image_index = 6
                    return
                elif self.rect.collidepoint((start_x+playspace.get_width()-4, self.rect.topright[1])):
                    self.chunk_x += 1
                    self.hitmap_array = pygame.surfarray.array2d(hitmap_img.subsurface(pygame.Rect((320*self.chunk_x, 192*self.chunk_y), (320, 192))))
                    self.x = start_x
                    return
            if self.image_index % 2 > 0: self.image_index -= 1

    def show(self):
        self.image = cat.subsurface(pygame.Rect((16*self.image_index, 0), (16, 16)))
        self.rect = playspace.blit(self.image, (self.x + start_x, self.y))

    def show_name(self):
        posx = min(max(self.rect.centerx-80, 8), 152)
        posy = min(max(self.rect.centery-48, 8), 88)
        fr = pygame.Rect((posx, posy), (160, 96))
        self.nameX = self.rect.centerx-fr.topleft[0] - (len(self.name) * 1.2)
        self.nameY = self.rect.centery-fr.topleft[1]+10
        resized_playspace.blit(globalFont.render(self.name, True, (255,255,255)), (self.nameX*4, (self.nameY*4)))
    
class Dog(Character):
    def __init__(self,name : str):
        Character.__init__(self, name)
        
class Cat(Character):
    def __init__(self,name : str):
        Character.__init__(self, name)
        #self.image.fill((0, 255, 0))

        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

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
        self.show()
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
        if self.hovering: self.rect = d.blit(self.hoverSurf, (self.x, self.y))
        else: self.rect = d.blit(self.image, (self.x, self.y))
        d.blit(globalFont.render(self.text, True, (0,0,0)), (self.x, self.y))

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

me = Cat("Csacsi")
#notme = Dog("Someone else")

chat_input = Input("Itt lesz majd a chat", (playspace.get_width()*scale, playspace.get_height()*scale), (1000,50), (255,255,255))

while playing:
    #playspace.fill((0,0,0))
    playspace = map_img.subsurface(pygame.Rect((320*me.chunk_x, 192*me.chunk_y), (320, 192))).copy()
    for event in pygame.event.get(eventtype=pygame.QUIT): playing = False
    me.onUpdate()
    posx = min(max(me.rect.centerx-80, 8), 152)
    posy = min(max(me.rect.centery-48, 8), 88)
    fov_rect = pygame.Rect((posx, posy), (160, 96))
    fov = playspace.subsurface(fov_rect)
    #notme.onUpdate()
    chat_input.onUpdate()
    tick +=1
    pygame.display.update()
    pygame.time.Clock().tick(60)
    resized_playspace = pygame.transform.scale(fov, (320*scale, 192*scale))
    me.show_name()
    
    d.fill((0,0,100))
    d.blit(resized_playspace, (start_x,0))
    #d.blit(playspace, (start_x,0))

print("Bye!")
