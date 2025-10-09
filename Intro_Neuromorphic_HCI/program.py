import pygame
import experiment as exp
import time

class Program:
    def __init__(self, width=1200, height=800, fps=60, title="Blinded Fitts' Law Experiment", icon_path='../img/target.png'):
        # initialize experiment
        self.experiment = exp.Experiment()
        self.exp_start_time = None
        self.exp_running = False
        self.from_left = True

        pygame.init()

        # initialize pygame window
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((255, 255, 255))
        self.fps_clock = pygame.time.Clock()
        self.fps = fps
        self.icon = pygame.image.load(icon_path)

        # set window title and icon
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(title)
        
        # draw initial targets
        self.draw_targets()
        self.running = True

    def draw_targets(self):
        ''' Draw start and target rectangles '''
        if self.from_left:
            self.start = (50, self.screen.get_height() // 2 - 20, 20, 40)
            self.target = (self.experiment.amp + 60 - (self.experiment.width//2), 20, self.experiment.width, self.screen.get_height() - 40) # Add 50 to the amplitude to account for the mouse start location
        else:
            self.start = (self.screen.get_width() - 50, self.screen.get_height() // 2 - 20, 20, 40)
            self.target = (self.screen.get_width() - (self.experiment.amp + (self.experiment.width//2) + 40), 20, self.experiment.width, self.screen.get_height() - 40) # Subtract 50 to the amplitude to account for the mouse start location

        pygame.draw.rect(self.screen, (34, 177, 76), self.start)
        pygame.draw.rect(self.screen, (230, 34, 114), self.target)

    def game_loop(self):
        ''' Main game loop '''

        # Loop for both directions (left to right and right to left)
        for direction in [True, False]:
            self.from_left = direction
            trial_count = 0

            # Game loop for trials per direction
            while self.running and trial_count < self.experiment.trials:   
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    # On mouse click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # if click is within start rectangle and experiment is not running, start experiment
                        if event.button == 1 and not self.exp_running:  # Left mouse button
                            if event.pos[0] >= self.start[0] and event.pos[0] <= self.start[0] + self.start[2] and event.pos[1] >= self.start[1] and event.pos[1] <= self.start[1] + self.start[3]:
                                self.start_experiment()
                        elif event.button == 1 and self.exp_running:
                            trial_count += 1
                            if trial_count == self.experiment.trials and self.from_left:
                                self.from_left = False
                            self.end_experiment(event.pos) 

                pygame.display.update()
                self.fps_clock.tick(self.fps)        

        time.sleep(1)
        pygame.quit()
        self.experiment.save_results()
        self.experiment.print_results()

    def start_experiment(self):
        ''' Start the experiment '''

        self.exp_running = True
        self.exp_start_time = time.time()
        
        # Reset mouse to correct start position
        if self.from_left:
            pygame.mouse.set_pos((60, self.screen.get_height() // 2))
        else:
            pygame.mouse.set_pos((self.screen.get_width() - 40, self.screen.get_height() // 2))

        time.sleep(self.experiment.visibility_time)
        
        # Clear screen and hide mouse
        pygame.mouse.set_visible(False)
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.screen.get_width(), self.screen.get_height()))

    def end_experiment(self, pos: int):
        ''' End the experiment and calculate score '''

        self.exp_running = False
        end_time = time.time() 
        pygame.mouse.set_visible(True)
        
        # Calculate distance from target center
        dist = pos[0] - self.target[0] - (self.experiment.width / 2)
        # account for direction
        if not self.from_left:
            dist *= -1

        abs_dist = abs(dist)

        # Add score to experiment
        self.experiment.add_score(dist, end_time - self.exp_start_time)
        
        max_distance = max(self.experiment.amp, self.screen.get_width() - (self.experiment.amp + self.experiment.width))
        
        normalized_dist = min((abs_dist**0.3) / (max_distance**0.3), 1.0)
        color = (int(255 * normalized_dist), int(255 * (1 - normalized_dist)), 8)

        # Redraw screen with targets and feedback
        self.draw_targets()
        pygame.draw.circle(self.screen, color, pos, 10)


    def run(self):
        self.game_loop()