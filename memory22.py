# Mini-project 3 Memeroy Xingyang Zheng

import pygame, random, time

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 
    
class Game:

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        
        # time
        self.score = 0

        # === game specific objects
        self.board_size = 4
        self.image_list=[]
        self.load_images()
        self.board = [] # will be represented by a list of lists
        self.tile_width = self.surface.get_width()//self.board_size
        self.tile_height = self.surface.get_height()//self.board_size
        self.create_board()
        
        # compare tile
        self.compare_list = []

    def load_images(self):
        # load the images from the files into the image list
        for i in range(1,9):
            filename = "image" + str(i) + ".bmp"
            image = pygame.image.load(filename)
            #image = pygame.transform.scale(image, 尺寸)
            self.image_list.append(image)
        
        #after loading all the 16 imgaes
        self.image_list = self.image_list +self.image_list
        random.shuffle(self.image_list)
    
    def create_board(self):

        for row_index in range(0,self.board_size):
            row = []
            for col_index in range(0,self.board_size):
                    image = self.image_list[0]
                    self.image_list.remove(image)
                    width = image.get_width()
                    height = image.get_height()
                    x = col_index * width
                    y = row_index * height
                    tile = Tile(x,y,width,height,image,self.surface)
                    row.append(tile)
            self.board.append(row)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                for tile_lists in self.board:
                    for tile in tile_lists:
                        if tile.clickable(event.pos):
                            tile.flip()
                            self.compare_list.append(tile)
            

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        # draw the board
        for tile_lists in self.board:
            for tile in tile_lists:
                tile.draw()
                self.draw_score()
        pygame.display.update() # make the updated surface appear on the display
    
    def draw_score(self):
        score = str(self.score)
        font = pygame.font.SysFont('',80)
        text_box = font.render(score,True,pygame.Color('white'))
        width_text = text_box.get_width()
        surface_width = self.surface.get_width()
        location = [surface_width - width_text, 0]
        self.surface.blit(text_box, location)
    
    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.score = pygame.time.get_ticks() // 1000
        
        if len(self.compare_list) == 2:
            if self.compare_list[0] != self.compare_list[1]:
                time.sleep(1)
                for tile in self.compare_list:
                    tile.flip()
            self.compare_list =[ ]

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        self.continue_game = False
        for tile_lists in self.board:
            for tile in tile_lists:
                if tile.check_hidden() == True:
                    self.continue_game = True
            

class Tile:

    def __init__(self,x,y,width,height,image,surface):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color('white')
        self.border_width= 1
        self.hidden_image = pygame.image.load('image0.bmp')
        self.hidden = True
        self.content = image
        self.surface = surface
        self.image = image

    def draw(self):
        # draw the coordinates of each Tile objects
        #string = str(self.rect.x) + ','+ str(self.rect.y)
        #font = pygame.font.SysFont('',40)
        #text_box = font.render(string,True, self.color)
        #location = (self.rect.x,self.rect.y)
        #self.surface.blit(text_box,location)
        location = (self.rect.x, self.rect.y)
        if self.hidden == True:
            self.surface.blit(self.hidden_image, location)
        else:
            self.surface.blit(self.content, location)
        pygame.draw.rect(self.surface,self.color,self.rect, self.border_width)
        #self.draw_content()
    
    def clickable(self, position):
        return self.rect.collidepoint(position) and self.hidden 
    def check_hidden(self):
        return self.hidden
    def flip(self):
        self.hidden = not self.hidden
    
    def get_image(self):
        return self.image
    
    def __eq__(self, other):
        return self.image == other.image
    
main()