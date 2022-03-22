import pygame

class Game:
    def __init__(self, surface):
        # initializing
        self.close_clicked = False
        self.continue_game = True
        self.game_clock = pygame.time.Clock()
        self.FPS = 60
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.score1 = 0
        self.score2 = 0

        # create two rectangles
        self.rect_left = pygame.Rect(60, 170, 15, 55)
        self.rect_right = pygame.Rect(420, 170, 15, 55)

        # create ball
        self.ball = Ball(pygame.Color('white'), [250, 200], 5, [-8, 3], self.surface)

        # create two paddles
        self.paddle_left = Paddle(pygame.Color('white'), self.rect_left, self.surface)
        self.paddle_right = Paddle(pygame.Color('white'), self.rect_right, self.surface)

    def play(self):
        # main game loop
        while not self.close_clicked:
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.move_paddles()
                self.update()
                self.decide_continue()
            self.game_clock.tick(self.FPS)

    def move_paddles(self):
        # assigning keys to move the paddles as well as to set a condition so that the paddles do not travel out of the
        # screen
        list_of_keys = pygame.key.get_pressed()
        size = self.surface.get_size()

        # check left paddle hitting top of screen
        if list_of_keys[pygame.K_w]:
            if self.rect_left.top < 8:
                self.rect_left.move_ip(0, -self.rect_left.top)
            else:
                self.rect_left.move_ip(0, -8)

        # check left paddle hitting bottom of screen
        if list_of_keys[pygame.K_s]:
            if size[1] - self.rect_left.bottom < 8:
                self.rect_left.move_ip(0, size[1] - self.rect_left.bottom)
            else:
                self.rect_left.move_ip(0, 8)

        # check if the right paddle hitting top of screen
        if list_of_keys[pygame.K_UP]:
            if self.rect_right.top < 8:
                self.rect_right.move_ip(0, -self.rect_right.top)
            else:
                self.rect_right.move_ip(0, -8)
        # check if the right paddle hitting bottom of screen

        if list_of_keys[pygame.K_DOWN]:
            if size[1] - self.rect_right.bottom < 8:
                self.rect_right.move_ip(0, size[1] - self.rect_right.bottom)
            else:
                self.rect_right.move_ip(0, 8)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True

    def draw(self):
        # draw all the game objects
        self.surface.fill(self.bg_color)  # clear the display surface first
        self.ball.draw()
        self.paddle_left.draw()
        self.paddle_right.draw()
        # draw the score for both players
        self.draw_score1()
        self.draw_score2()
        pygame.display.update()  # make the updated surface appear on the display

    def draw_score1(self):
        # set color
        fg_color = pygame.Color('white')
        # create font object
        font = pygame.font.SysFont('', 70)
        # create text box by rendering the font
        text_string = str(self.score1)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        # compute location of text box
        location = (20, 20)
        # blit text box on surface
        self.surface.blit(text_box, location)

    def draw_score2(self):
        # set color
        fg_color = pygame.Color('white')
        # create font object
        font = pygame.font.SysFont('', 70)
        # create text box by rendering the font
        text_string = str(self.score2)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        # compute location of text box
        location = (440, 20)
        # blit text box on surface
        self.surface.blit(text_box, location)

    def update(self):
        # move the ball and update the score when ball hits either side of the  screen
        self.ball.move(self.rect_left, self.rect_right)
        size = self.surface.get_size()
        if self.ball.center[0] < self.ball.radius:  # left or top
            self.score2 += 1
        elif self.ball.center[0] + self.ball.radius > size[0]:
            self.score1 += 1  # right or bottom

    def decide_continue(self):
        # set conditions so game ends when either score reaches 11
        if self.score1 == 11:
            self.continue_game = False
        elif self.score2 == 11:
            self.continue_game = False

class Ball:
    # an object in this class represents a Ball that moves
    def __init__(self, color, center, radius, velocity, surface):
        # initialize the instance attributes of the Ball object
        self.color = color
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.surface = surface

    def draw(self):
        # draw the Ball object
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    def move(self, paddle_left, paddle_right):
        # moves the ball by changing its center by the value of the velocity
        # also checks if there is collision between the ball and the paddles
        size = self.surface.get_size()
        for index in range(0, 2):
            self.center[index] = self.center[index] + self.velocity[index]
            if self.center[index] < self.radius:  # left or top
                self.velocity[index] = -self.velocity[index]

            if self.center[index] + self.radius > size[index]:  # right or bottom
                self.velocity[index] = -self.velocity[index]

        if paddle_left.collidepoint(self.center) and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]

        if paddle_right.collidepoint(self.center) and self.velocity[0] > 0:
            self.velocity[0] = -self.velocity[0]

class Paddle:
    def __init__(self, color, rect, surface):
        # initializes the instance attributes of the Paddle object
        self.color = color
        self.rect = rect
        self.surface = surface

    def draw(self):
        # draws the Paddle object
        pygame.draw.rect(self.surface, self.color, self.rect)


def main():
    # initialize all pygame modules
    pygame.init()
    # create pygame display window and set the title
    size = (500, 400)
    title = 'Pong'
    pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


main()
