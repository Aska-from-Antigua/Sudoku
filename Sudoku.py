####################################
##
##Jerry Aska
##
##Grid Click
##
####################################
import pygame, pygame.gfxdraw, sys, random, math
from pygame.locals import *

pygame.init()

# colours        R    G    B

WHITE          = (255, 255, 255)
GREY           = (125, 125, 125)
OFF_WHITE      = (125, 125, 125)
BLACK          = (  0,   0,   0)
RED            = (255,   0,   0)
ORANGE         = (255, 125,   0)
YELLOW         = (255, 255,   0)
GREEN          = (  0, 255,   0)
BLUE           = (  0,   0, 255)
PURPLE         = (255,   0, 255)
DARK_BLUE      = (  0,   0, 125)

list_of_colors         = [RED, ORANGE, YELLOW, GREEN, PURPLE, BLACK, WHITE, DARK_BLUE]
list_of_colors_names   = ["RED", "ORANGE", "YELLOW", "GREEN", "PURPLE", "BLACK", "WHITE", "DARK BLUE"]
scr_height             = 600
scr_width              = 600
DISPLAYSURF            = pygame.display.set_mode((scr_width, scr_height),pygame.RESIZABLE)


FPS = 60
fpsClock = pygame.time.Clock()

SCREEN_COLOR     = GREEN
SCREEN_COLUMNS   = 9
SCREEN_ROWS      = 9
SCREEN_RATIO     = SCREEN_COLUMNS/SCREEN_ROWS
GRID_FACTOR      = SCREEN_ROWS


TEXT_COLOR                 = WHITE
TRUE_TEXT_COLOR            = GREEN

FONT_STYLE                 = "calibri"
FONT_SIZE_PERCENT          = 1/(SCREEN_ROWS/100)

###########################################################################################################################
##                                                  Classes Definition
###########################################################################################################################

class nothing:
    """
    Place Holder Object

    This object is simply to be used as a default for relational operators for when there is no object to relate to.
    It contains all the attributes necessary for relational operators in this program set to 0 indicating to other objects
    that there is nothing there.
    """
    def __init__(self, pos_x = 0, pos_y = 0, height = 0, width = 0, space_above = 0, space_to_the_left = 0, columns = 0, rows = 0, grid_size = 0, is_nothing = True):
        self.pos_x              = pos_x
        self.pos_y              = pos_y
        self.height             = height
        self.width              = width
        self.space_above        = space_above
        self.space_to_the_left  = space_to_the_left
        self.columns            = columns
        self.rows               = rows
        self.grid_size          = grid_size
        self.is_nothing         = is_nothing

###########################################################################################################################

class screen:
    """
    Screen Object

    This object contains attributes to allow for a miniature screen within the display surface. This object can be given a
    specific ratio and will maintain this ratio even when the display surface is resized. It can also be given items to
    share the display surface with and can be resized to allow space for those objects while still maintaining the ratio.
    """
    def __init__(self, width = scr_width, height = scr_height, item_above = nothing(), item_to_the_left = nothing(), space_to_the_left = 0, space_above = 0, color = SCREEN_COLOR, ratio = SCREEN_RATIO, grid_factor = GRID_FACTOR, screen_columns = SCREEN_COLUMNS, screen_rows = SCREEN_ROWS):
        self.pos_x              = item_to_the_left.pos_x + item_to_the_left.width + item_to_the_left.space_to_the_left
        self.pos_y              = item_above.pos_y + item_above.height + item_above.space_above
        self.space_to_the_left  = space_to_the_left
        self.space_above        = space_above
        self.width              = width - item_to_the_left.width
        self.height             = height - item_above.height
        self.item_to_the_left   = item_to_the_left
        self.item_above         = item_above
        self.color              = color
        self.ratio              = ratio
        self.is_nothing         = False
        self.grid_size          = self.height / grid_factor
        self.grid_factor        = grid_factor
        self.columns            = screen_columns
        self.rows               = screen_rows


    def display(self):
        DISPLAYSURF.fill(self.color, ((self.pos_x + self.space_to_the_left, self.pos_y + self.space_above), (self.width, self.height)))


    def resize(self, new_width, new_height, item_above = nothing(), item_to_the_left = nothing()):
        if not item_to_the_left.is_nothing:
            self.item_to_the_left = item_to_the_left
        if not item_above.is_nothing:
            self.item_above = item_above
        new_width   = new_width - (self.item_to_the_left.pos_x + self.item_to_the_left.width)
        new_height  = new_height - (self.item_above.pos_y + self.item_above.height)
        ratio       = new_width / new_height
        if ratio == self.ratio:
            self.width             = new_width
            self.height            = new_height
            self.space_above       = 0
            self.space_to_the_left = 0
        if ratio > self.ratio:
            self.width              = int(new_height * self.ratio)
            self.height             = new_height
            self.space_to_the_left  = (new_width - self.width) // 2
            self.space_above        = 0
        if ratio < self.ratio:
            self.width              = new_width
            self.height             = int(new_width / self.ratio)
            self.space_to_the_left  = 0
            self.space_above        = (new_height - self.height) // 2
        self.grid_size        = self.height / self.grid_factor

###########################################################################################################################

class sector:
    """
    
    """
    def __init__(self, sector_pos, screen, color = WHITE, Type = "None", text_color = TEXT_COLOR, true_text_color = TRUE_TEXT_COLOR, font_style = FONT_STYLE, font_size_percent = FONT_SIZE_PERCENT, true_value = " ", setable = True):
        self.sector_pos       = sector_pos
        self.row              = sector_pos // screen.rows
        self.column           = sector_pos % screen.rows
        self.quadrant         = self.column // 3 + 3 * (self.row // 3)
        self.pos_x            = (sector_pos % screen.columns) * screen.grid_size + screen.space_to_the_left + screen.pos_x
        self.pos_y            = (sector_pos // screen.columns) * screen.grid_size + screen.space_above + screen.pos_y
        self.width            = screen.width // screen.columns
        self.height           = screen.height // screen.rows
        self.mid_x            = self.pos_x + self.width // 2
        self.mid_y            = self.pos_y + self.height // 2
        self.radius           = min(self.width,self.height) // 2
        self.state            = False
        self.color            = color
        self.screen           = screen
        self.type             = Type
        self.text             = ""
        self.is_nothing       = False
        self.highlight        = False
        self.t_highlight      = False
        self.displayed        = False
        self.t_displayed      = False
        self.r_highlight      = False
        self.setable          = setable 
        self.text_color       = text_color
        self.true_value       = true_value
        self.true_text_color  = true_text_color
        self.style            = font_style
        self.size             = font_size_percent / 100
        self.font             = pygame.font.SysFont(self.style, int(screen.height * self.size))

            
    def reset(self, text = "", true_value = "", setable = True): 
        self.state       = False
        self.setable     = setable
        self.true_value  = true_value
        self.text        = text

        
    def resize(self, screen = nothing()):  
        if not screen.is_nothing:
            self.screen = screen
        self.pos_x   = (self.sector_pos % self.screen.columns) * self.screen.grid_size + self.screen.space_to_the_left + self.screen.pos_x
        self.pos_y   = (self.sector_pos // self.screen.columns) * self.screen.grid_size + self.screen.space_above + self.screen.pos_y
        self.width   = self.screen.width // self.screen.columns
        self.height  = self.screen.height // self.screen.rows
        self.mid_x   = self.pos_x + self.width // 2
        self.mid_y   = self.pos_y + self.height // 2
        self.radius  = min(self.width, self.height) // 2
        self.font    = pygame.font.SysFont(self.style, int(self.screen.height * self.size))

        
    def set_state(self, sector_list, text):
        if self.setable:
            self.state     = True
            self.displayed = True
            self.text      = str(text)
        
            
    def is_clicked(self, mouse_pos_x, mouse_pos_y):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                return True
        return False


    def is_highlighted(self, mouse_pos_x, mouse_pos_y, sectors):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                self.t_highlight  = True
            else:
                self.highlight    = True
                self.t_highlight  = False
        elif mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
            self.highlight    = True
            self.t_highlight  = False
        else:
            self.highlight    = False
            self.t_highlight  = False
        if self.t_highlight:               
            if not self.setable or (self.setable and not self.text == ""):
                for x in range(len(sectors.list)):
                    if not x == self.sector_pos:
                        if self.setable:
                            if sectors.list[x].setable:
                                if sectors.list[x].text == self.text:
                                    sectors.list[x].r_highlight = True
                                else:
                                    sectors.list[x].r_highlight = False                            
                            else:
                                if sectors.list[x].true_value == self.text:
                                    sectors.list[x].r_highlight = True
                                else:
                                    sectors.list[x].r_highlight = False
                        else:
                            if sectors.list[x].setable:
                                if sectors.list[x].text == self.true_value:
                                    sectors.list[x].r_highlight = True
                                else:
                                    sectors.list[x].r_highlight = False                            
                            else:
                                if sectors.list[x].true_value == self.true_value:
                                    sectors.list[x].r_highlight = True
                                else:
                                    sectors.list[x].r_highlight = False
            else:
                for x in range(len(sectors.list)):
                    sectors.list[x].r_highlight = False
                            
##            if sectors.are_displayed:
##                for x in range(len(sectors.list)):
##                    if sectors.list[x].true_value == self.true_value:
##                        sectors.list[x].r_highlight = True
##                    else:
##                        sectors.list[x].r_highlight = False
##            else:
##                for x in range(len(sectors.list)):
##                    sectors.list[x].r_highlight = False
                
                            


    def display(self):
        color = None
        if not self.setable:
            self.t_displayed = True
        if self.highlight:
            color = DARK_BLUE
        if self.t_highlight:
            color = BLUE
        if self.r_highlight:
            if self.highlight:
                color = RED
            else:
                color = PURPLE
        if not color == None:
            pygame.draw.rect(DISPLAYSURF, color, (self.pos_x, self.pos_y, self.width, self.height))
        if not self.t_displayed:
            TEXT = pygame.font.Font.render(self.font, self.text, True, self.text_color)
        if self.t_displayed:
            TEXT = pygame.font.Font.render(self.font, str(self.true_value), True, self.true_text_color)
            
        DISPLAYSURF.blit(TEXT, (self.pos_x + int(3/12*self.width), self.pos_y))

###########################################################################################################################

class object_list:
    """
    
    """
    def __init__(self):
        self.list           = []
        self.is_nothing     = False
        self.are_displayed  = False

        
    def append(self, item):
        self.list.append(item)
        

    def clear(self):
        for z in range(len(self.list)):
            self.list[z].text = ""


    def are_active(self):
        active = True
        for x in self.list:
            if (not x.setable and not x.text == "") or (x.setable and x.text == ""):
                active = False
                b = x.sector_pos
                break    
##        print(b, active)


    def are_set_true(self):
        active = True
        for x in range(len(self.list)):
            if not self.list[x].true_value == "":
                continue
            else:
                active = False
                break
        return active

        
    def resize(self, item_to_follow = nothing()):
        for y in range(len(self.list)):
            self.list[y].resize(item_to_follow)

        
    def set_true_value(self):
        list_of_values = [9,1,7,8,2,6,4,5,3,2,4,8,1,3,5,6,7,9,3,5,6,9,4,7,8,1,2,1,8,2,7,6,3,5,9,4,4,3,9,5,8,2,1,6,7,6,7,5,4,9,1,2,3,8,5,9,3,2,1,4,7,8,6,8,2,1,6,7,9,3,4,5,7,6,4,3,5,8,9,2,1]
##        [5,7,2,8,4,6,1,9,3,8,9,1,5,7,3,2,4,6,3,4,6,9,1,2,7,5,8,6,5,4,7,8,9,3,1,2,2,3,9,1,6,5,8,7,4,7,1,8,2,3,4,5,6,9,4,6,5,3,2,1,9,8,7,1,8,3,4,9,7,6,2,5,9,2,7,6,5,8,4,3,1]
        for x in range(len(list_of_values)):
            self.list[x].true_value = str(list_of_values[x])
##        p = 2
##        all_assignments = list(range(len(self.list)))
##        for x in range(1,10):
##            rows = list(range(9))
##            columns = list(range(9))
##            quadrants = list(range(9))
##            assignments = 0
##            assignment_list = [[]]
##            possible_assignments =list(all_assignments)
##            for y in range(9):
####                print(y,"should be equal to",assignments)
##                not_set = True
##                while not_set:
##                    try:
##                        if x == p:
##                            raise KeyboardInterrupt
##                        row = rows[random.randrange(len(rows))]
##                        column = columns[random.randrange(len(columns))]
##                        quadrant    = (column // 3) + 3 * (row // 3)
##                        if not quadrant in quadrants:
##                            continue
##                        for z in possible_assignments:
##                            if not self.list[z].true_value == " ":
##                                print("'",self.list[z].true_value,"'", sep =  "")
##                                print(z,"is misbehaving")
##                                possible_assignments.remove(z)
##                                break     
##                            if self.list[z].true_value == " ":                       
####                                print("Row:",row)
####                                print("Column:",column)
####                                print("Quadrant:",quadrant)
##                                if self.list[z].row == row or self.list[z].column == column or self.list[z].quadrant == quadrant:
##                                    if self.list[z].true_value == x:
##                                        print(column * 9 + row,"cannot have",x)
##                                        print(x,"is already taken by",z,":",self.list[z].true_value)
##                                        print("Assignments =",assignments)
##                                        possible_assignments.remove(z)
##                                        break
##                        else:
##                            if column * 9 + row in all_assignments:
##                                not_set = False
##                                assignments += 1
##                                print(column * 9 + row,"is assigned",x)
##                                print("Assignments =",assignments)
##                                self.list[column * 9 + row].true_value = x
##                                all_assignments.remove(column * 9 + row)                            
##                                assignment_list.insert(-1,[assignments, column * 9 + row, x])
##                                rows.remove(row)
##                                columns.remove(column)
##                                quadrants.remove(quadrant)
##                            else:
##                                not_set = True
##                    except KeyboardInterrupt:
##                        p = x + 1
##                        print("\n\n\n\n",assignment_list)
##                        print("", end = "[")
##                        for a in range(len(sectors.list)):
##                            if not sectors.list[a].column == 8:
##                                print(sectors.list[a].true_value,end = ", ")
##                            else:
##                                print(sectors.list[a].true_value,end = "]\n\n\n[")
##                        input()
                            
                        


        
##        for x in range(len(self.list)):
##            if self.list[x].true_value == "":
##                value = random.randrange(1,10)
##                for y in range(len(self.list)):
##                    if not x == y:
##                        if self.list[x].row == self.list[y].row or self.list[x].column == self.list[y].column or self.list[x].quadrant == self.list[y].quadrant:
##                            if value == self.list[y].true_value and not self.list[y].true_value == 0:
##                                break
##                else:
##                    self.list[x].true_value = value



                

            
    def reset(self, color = WHITE):                
        for x in range(len(self.list)):
            self.list[x].reset(true_value = "")

    
    def check_if_clicked(self, mouse_pos_x, mouse_pos_y, button, text):
        for x in range(len(self.list)):
            if self.list[x].is_clicked(mouse_pos_x, mouse_pos_y):
                if button == 1:
                    self.list[x].set_state(self, text)
                    self.check_if_highlighted(mouse_pos_x, mouse_pos_y)
                if button == 3:
                    if self.are_displayed:
                        self.hide()
                    else:
                        self.make_displayed()
                    self.are_displayed = not self.are_displayed
                if button == 0:
                    return x

                    
    def check_if_highlighted(self, mouse_pos_x, mouse_pos_y):
        for x in range(len(self.list)):
            self.list[x].is_highlighted(mouse_pos_x, mouse_pos_y, self)
        x = self.check_if_clicked(mouse_pos_x, mouse_pos_y, 0, "")
        if not x == None:
            for y in range(len(sectors.list)):
                if self.list[y].quadrant == self.list[x].quadrant:
                    self.list[y].highlight = True     


    def display(self):
        for y in range (len(self.list)):
            self.list[y].display()
            
            
    def make_displayed(self):
        for y in range(len(self.list)):
            self.list[y].t_displayed = True

    def hide(self):
        for y in range(len(self.list)):
            self.list[y].t_displayed = False

###########################################################################################################################
 
def draw_grid(game_screen):
    for x in range(round(game_screen.width/game_screen.grid_size) + 1):
        if x % 3 == 0:
            width = 9
        else:
            width = 1
        pygame.draw.line(DISPLAYSURF,WHITE,(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.pos_y),(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.height + game_screen.pos_y), width)
    for y in range(round(game_screen.height/game_screen.grid_size) + 1):
        if y % 3 == 0:
            width = 9
        else:
            width = 1
        pygame.draw.line(DISPLAYSURF,WHITE,(game_screen.space_to_the_left + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y), (game_screen.space_to_the_left + game_screen.width + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y), width)

###########################################################################################################################

             
game_screen = screen(color = BLACK)

        
sectors     = object_list()
for y in range(game_screen.rows * game_screen.columns):
    sectors.append(sector(y, game_screen))
    
sectors.set_true_value()

##while not sectors.are_set_true():
##    sectors.reset()
##    sectors.set_true_value()
##    print("", end = "[")
##    for x in range(len(sectors.list)):
##        if not sectors.list[x].column == 8:
##            print(sectors.list[x].true_value,end = ", ")
##        else:
##            print(sectors.list[x].true_value,end = "]\n\n\n[")
##    print("\n\n\n\n\n\n\n")
    

view = []
for x in range(30):
    while True:
        y = random.randrange(81)
        if not y in view:
            view.append(y)
            break
        
for x in range(len(sectors.list)):
    setable = True
    if x in view:
        setable = False
    sectors.list[x].setable = setable
    
while True:
    sectors.are_active()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == 8:
                text = ""
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, 1, text)
            if event.key == 27:
                sectors.clear()
            if event.key >= 257 and event.key <= 265:
                text = str(event.key - 256)
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, 1, text)
            if event.key >=  49 and event.key <=  57:
                text = str(event.key - 48)
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, 1, text)
            if event.key == K_c:
                key_i = pygame.key.get_pressed()
                if key_i[K_LCTRL] or key_i[K_RCTRL]:
                    pygame.quit()
                    sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, event.button, "")
        if event.type == MOUSEMOTION:
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            sectors.check_if_highlighted(mouse_pos_x, mouse_pos_y)
        if event.type == VIDEORESIZE:
            DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)            
            game_screen.resize(event.w, event.h)
            sectors.resize()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    DISPLAYSURF.fill(GREY)
    game_screen.display()
    sectors.display()
    draw_grid(game_screen)
    pygame.display.update()
    fpsClock.tick(FPS)

