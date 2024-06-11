# Jordan Netz
# EPS TICS/AIML
# Jan 16 2024
# The code for the actual game of pacman. This is the file to be run.

import pygame
import ghost_ai
import copy
class pacman_game:


    def __init__(self, old_game=None):
        self.map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0] 
        ]

        self.grid_size_x = len(self.map[0])
        self.grid_size_y = len(self.map)
        self.grid_square_size_x = 30
        self.grid_square_size_y = 30

    
        self.running = 1
        
        

        self.pacman_data = {
            "x": 0,
            "y": 0,
            "dir": 2,
            "prev_positions": []
        }

        self.score = 0
        self.game_tic = 250  # Milliseconds


        self.ghost_data = [
            {
                "x": 10,
                "y": 10,
                "dir": 2,
                "prev_positions": []
            },
            {
                "x": 9,
                "y": 10,
                "dir": 2,
                "prev_positions": []
            }
        ]

        self.dots = {(x, y): True for x in range(self.grid_size_x) 
                                for y in range(self.grid_size_y) 
                                if not self.is_wall(x, y)}  # Initialize all dots in spots that are not walls
        self.total_starting_dots = len(self.dots)
    

    # In your pacman_game module



        
    def is_wall(self, x, y):
        """Check if the given position is a wall."""
        return self.map[y][x]

    def check_win_loss(self):
        #Check if you lost:
        for ghost in self.ghost_data:
            if (self.pacman_data["x"], self.pacman_data["y"]) == (ghost["x"], ghost["y"]) or \
                self.pacman_data["prev_positions"][-1] == (ghost["x"], ghost["y"]) and ghost["prev_positions"][-1] == (self.pacman_data["x"], self.pacman_data["y"]):

                    self.running = 0  # End the game

                    return
        #Check if you won:
        if (self.pacman_data["x"], self.pacman_data["y"]) in self.dots and self.running != 0:
            del self.dots[(self.pacman_data["x"], self.pacman_data["y"])]
            self.score += 1
            if len(self.dots) == 0:
                self.running = 2

        

    def redraw_game(self):
        # Draw game
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player_image, (self.pacman_data["x"] * self.grid_square_size_x+2.5, self.pacman_data["y"] * self.grid_square_size_y+2.5))

        # Draw dots
        for dot_pos in self.dots:
            self.screen.blit(self.dot_image, (dot_pos[0] * self.grid_square_size_x+12.5, dot_pos[1] * self.grid_square_size_y+12.5))

        for ghost in range(len(self.ghost_data)):
            self.screen.blit(self.ghost_image, (self.ghost_data[ghost]["x"] * self.grid_square_size_x+2.5, self.ghost_data[ghost]["y"] * self.grid_square_size_y+2.5))


            wall_color = (0, 255, 0)  # Green color for walls

        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if self.is_wall(x, y):
                    pygame.draw.rect(self.screen, wall_color, pygame.Rect(x * self.grid_square_size_x, y * self.grid_square_size_y, self.grid_square_size_x, self.grid_square_size_y))

    def check_for_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pacman_data["dir"] = 4
                elif event.key == pygame.K_RIGHT:
                    self.pacman_data["dir"] = 2
                elif event.key == pygame.K_UP:
                    self.pacman_data["dir"] = 1
                elif event.key == pygame.K_DOWN:
                    self.pacman_data["dir"] = 3

    def setup_game_screen(self):
        # Set up the self.screen
        self.screen_width = self.grid_size_x * self.grid_square_size_x
        self.screen_height = self.grid_size_y * self.grid_square_size_y
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set the title and icon
        pygame.display.set_caption("Pac-Man")
        icon = pygame.image.load("pacman.png")  # Ensure this image is in your project directory
        pygame.display.set_icon(icon)

        # Load the player and dot images
        PACMAN_SIZE = (25, 25)
        self.player_image = pygame.image.load("pacman.png")  # Ensure this image is in your project directory
        self.player_image = pygame.transform.scale(self.player_image, PACMAN_SIZE)
        DOT_SIZE = (8, 8)
        self.dot_image = pygame.image.load("dot.png")  # Ensure this image is in your project directory
        self.dot_image = pygame.transform.scale(self.dot_image, DOT_SIZE)
        GHOST_SIZE = (25, 25)
        self.ghost_image = pygame.image.load("blue_ghost.png")  # Make sure you have a ghost.png file
        self.ghost_image = pygame.transform.scale(self.ghost_image, GHOST_SIZE)


    def move_pacman(self):
        #print(ghost_ai.heuristic(self))
        self.pacman_data["prev_positions"] += (self.pacman_data["x"], self.pacman_data["y"])

        # Proposed new position based on the pacman_data["dir"]
        new_x, new_y = self.pacman_data["x"], self.pacman_data["y"]
        if self.pacman_data["dir"] == 1:  # Moving up
            new_y = (new_y - 1) % self.grid_size_y
        elif self.pacman_data["dir"] == 3:  # Moving down
            new_y = (new_y + 1) % self.grid_size_y
        elif self.pacman_data["dir"] == 2:  # Moving right
            new_x = (new_x + 1) % self.grid_size_x
        elif self.pacman_data["dir"] == 4:  # Moving left
            new_x = (new_x - 1) % self.grid_size_x

    # Check for wall collision
        if not self.is_wall(new_x, new_y):
            self.pacman_data["x"], self.pacman_data["y"] = new_x, new_y
        self.check_win_loss()
        
        
        
    def move_ghosts(self):
        for ghost in self.ghost_data: ghost["prev_positions"]=(ghost["x"], ghost["y"])
        for ghost in self.ghost_data:
            new_x, new_y = ghost["x"], ghost["y"]
            if ghost["dir"] == 1:  # Moving up
                new_y = (new_y - 1) % self.grid_size_y
            elif ghost["dir"] == 3:  # Moving down
                new_y = (new_y + 1) % self.grid_size_y
            elif ghost["dir"] == 2:  # Moving right
                new_x = (new_x + 1) % self.grid_size_x
            elif ghost["dir"] == 4:  # Moving left
                new_x = (new_x - 1) % self.grid_size_x

        # Check for wall collision
            if not self.is_wall(new_x, new_y):
                ghost["x"], ghost["y"] = new_x, new_y

    def get_ai_move(self):
    # Ensure the minimax function is called for the ghosts (minimizing player)
        best_score, best_ghost_moves = ghost_ai.ab_pruning(self, 3, False)

        # Check if best_ghost_moves is a tuple (which it should be for the ghosts)
        if isinstance(best_ghost_moves, tuple):
            #print(best_ghost_moves)
            for i, move in enumerate(best_ghost_moves):
                self.ghost_data[i]["dir"] = move
        else:
            print("Error: Expected a tuple of moves for the ghosts.")


    def play_pacman(self):
        import pygame
        # Initialize Pygame
        pygame.init()

        self.setup_game_screen()
        # Set up the game variables
        self.running = 1
        last_move_time = 0

        # Main game loop
        while self.running == 1:
            self.current_time = pygame.time.get_ticks()

            # Check for player input
            self.check_for_move()

            if self.current_time - last_move_time >= self.game_tic:

                last_move_time = self.current_time

                # Save previous positions for collision check
                self.get_ai_move()
                self.move_ghosts()



                self.move_pacman()
            
                

            self.redraw_game()

            



            # Draw score
            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render("Score: " + str(self.score) + "/"+str(self.total_starting_dots), True, (255, 0, 0))
            self.screen.blit(text, (10, 10))
            pygame.display.flip()



        # Quit Pygame
        pygame.quit()
        if self.running == 2:
            print("Congratulations! You've won the game with a score of", self.score)
        elif self.running == 0:
            print("Oh no! Pac-Man has been caught by a ghost!")
            print("You've lost!")


       
    import copy

    def copy_game_state(self):
        new_game = pacman_game()
        new_game.map = copy.deepcopy(self.map)
        new_game.grid_size_x = self.grid_size_x
        new_game.grid_size_y = self.grid_size_y
        new_game.grid_square_size_x = self.grid_square_size_x
        new_game.grid_square_size_y = self.grid_square_size_y

        new_game.pacman_data = copy.deepcopy(self.pacman_data)
        new_game.ghost_data = copy.deepcopy(self.ghost_data)
        new_game.dots = copy.deepcopy(self.dots)
        new_game.total_starting_dots = self.total_starting_dots

        new_game.score = self.score
        new_game.game_tic = self.game_tic
        new_game.running = self.running

        # Note: We do not copy Pygame screen or images as they are specific to the current instance
        # They should be re-initialized as needed

        return new_game
game = pacman_game()
game.play_pacman()

