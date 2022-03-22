# Pre-Poke Framework
# Implements a general game template for games with animation
# You must use this template for all your graphical lab assignments
# and you are only allowed to inlclude additional modules that are part of
# the Python Standard Library; no other modules are allowed
# Poke Version 2 - end of game condition and drawing of score
# Poke Version 3 - draw Game over, handle events
import pygame, random, math


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

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

        # === game specific objects
        self.score = 0  # next mini-project
        self.create_dots()

        # self.max_frames = 150
        # self.frame_counter = 0

    def create_dots(self):
        self.small_dot = Dot('red', 30, [0, 0], [1, 2], self.surface)
        self.big_dot = Dot('blue', 40, [0, 0], [2, 1], self.surface)
        while self.small_dot.collide(self.big_dot):
            self.small_dot.randomize()
            self.big_dot.randomize()

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
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:  # mouse click
                self.handle_mouse_up()


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.small_dot.draw()
        self.big_dot.draw()
        self.draw_score()
        if not self.continue_game:
            self.draw_game_over()
        pygame.display.update()  # make the updated surface appear on the display

    def draw_game_over(self):
        string = 'Game Over'
        # Incorrect way
        # fg_color = self.small_dot.color  # violation of SW quality requirement Section 7.2
        # bg_color = self.big_dot.color  # violation of SW quality requirement Section 7.2

        # Reason
        # class is a black box
        # class encapsulates the behavior and properties of a a group of object
        # we should not access or change any of its instance attributes directly

        # Correct Way - call the getter method to get the color
        fg_color = self.small_dot.get_color()
        bg_color = self.big_dot.get_color()

        font = pygame.font.SysFont('', 70)
        text_box = font.render(string, True, fg_color, bg_color)
        c = self.surface.get_height()
        d = text_box.get_height()
        x = 0
        y = c - d
        location = (x, y)
        self.surface.blit(text_box, location)

    def draw_score(self):
        score_string = 'Time in secs:' + str(self.score)
        # step 1 create a font object
        font_size = 80
        fg_color = pygame.Color('white')
        font = pygame.font.SysFont('', font_size)
        # step 2 render the font
        text_box = font.render(score_string, True, fg_color, self.bg_color)
        # step 3  compute the location
        location = (0, 0)
        # code for drawing score in the top right corner of the window
        # y = 0
        # a = self.surface.get_size()[0]
        # a = self.surface.get_width()
        # b = text_box.get_size()[0]
        # b = text_box.get_width()
        # x = a -b
        # location = (x,y)
        # step 4 blit the source surface on the target surface at the specified location
        self.surface.blit(text_box, location)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.small_dot.move()
        self.big_dot.move()
        self.score = pygame.time.get_ticks() // 1000
        # self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        if self.small_dot.collide(self.big_dot):
            self.continue_game = False


class Dot:
    # An object in this class represents a Dot that moves

    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(dot_color)
        self.radius = dot_radius
        self.center = dot_center
        self.velocity = dot_velocity
        self.surface = surface

    def move(self):
        # Change the location of the Dot by adding the corresponding
        # speed values to the x and y coordinate of its center
        # - self is the Dot
        size = self.surface.get_size()  # get_size is a method in pygame.Surface class and it returns a tuple (width, height)
        for i in range(0, 2):
            self.center[i] = (self.center[i] + self.velocity[i])
            if self.center[i] < self.radius:  # left or the top edge
                self.velocity[i] = -self.velocity[i]
            if self.center[i] + self.radius > size[i]:  # right or bottom edge
                self.velocity[i] = - self.velocity[i]

    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)


main()