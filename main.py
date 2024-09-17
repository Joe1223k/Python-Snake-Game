import pygame, sys, random
from pygame.math import Vector2

pygame.init()

# Font
title_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 30)

# Grid settings
cell_size = 20
number_of_cells = 25

# Window layout
OFFSET = 50
LINE_THICKNESS = 2

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect((self.position.x*cell_size)+OFFSET, (self.position.y*cell_size)+OFFSET, cell_size, cell_size)
        pygame.draw.ellipse(screen, "red", food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
    
class Snake:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = ((segment.x*cell_size)+OFFSET, (segment.y*cell_size)+OFFSET, cell_size, cell_size)
            pygame.draw.rect(screen, "green", segment_rect, 0, 6)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "TITLE"
        self.score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        self.final_score = self.score
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "GAME_OVER"
        self.score = 0

# Screen settings
screen = pygame.display.set_mode((OFFSET*2 + cell_size*number_of_cells, OFFSET*2 + cell_size*number_of_cells))
pygame.display.set_caption("Python Snake Game")
clock = pygame.time.Clock()

# The Game object
game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Snake move inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game.state == "TITLE":
                    game.state = "RUNNING"
                elif game.state == "STOPPED":
                    game.state = "RUNNING"
                elif game.state == "GAME_OVER":
                    game.state = "TITLE"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = (0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = (0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = (-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = (1, 0)
            # Debugging
            if event.key == pygame.K_ESCAPE and game.state == "RUNNING":
                game.state = "STOPPED"

    # Draw
    screen.fill("black")

    if game.state == "TITLE":
        title_surface = title_font.render("Python Snake Game", True, "green")
        press_enter_surface = font.render("PRESS ENTER", True, "white")
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(press_enter_surface, (screen.get_width() // 2 - press_enter_surface.get_width() // 2, screen.get_height() // 2 + 20))

    elif game.state == "RUNNING":
        pygame.draw.rect(screen, "white", (OFFSET-LINE_THICKNESS, OFFSET-LINE_THICKNESS, (number_of_cells*cell_size)+LINE_THICKNESS*2, (number_of_cells*cell_size)+LINE_THICKNESS*2), LINE_THICKNESS)
        game.draw()
        title_surface = font.render("Python Snake Game", True, "white")
        score_surface = font.render("Score: " + str(game.score), True, "white")
        screen.blit(title_surface, (OFFSET-LINE_THICKNESS, 15))
        screen.blit(score_surface, ((number_of_cells*cell_size)-OFFSET-LINE_THICKNESS+20, 15))
    
    elif game.state == "GAME_OVER":
        game_over_surface = title_font.render("GAME OVER", True, "red")
        final_score_surface = font.render(f"Final Score: {game.final_score}", True, "white")
        press_enter_surface = font.render("PRESS ENTER", True, "white")
        screen.blit(game_over_surface, (screen.get_width() // 2 - game_over_surface.get_width() // 2, screen.get_height() // 2 - 80))
        screen.blit(final_score_surface, (screen.get_width() // 2 - final_score_surface.get_width() // 2, screen.get_height() // 2))
        screen.blit(press_enter_surface, (screen.get_width() // 2 - press_enter_surface.get_width() // 2, screen.get_height() // 2 + 40))

    # Update
    pygame.display.update()
    clock.tick(60)