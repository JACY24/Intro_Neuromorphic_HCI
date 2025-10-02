import pygame
import experiment as exp
import time

class Program:
    def __init__(self, width=1200, height=800, fps=60, title="Blinded Fitts' Law Experiment", icon_path='../img/target.png'):
        self.experiment = exp.Experiment()
        self.exp_start_time = None
        self.exp_running = False

        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((255, 255, 255))
        self.fps_clock = pygame.time.Clock()
        self.fps = fps
        self.icon = pygame.image.load(icon_path)

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(title)

        self.target = (self.experiment.amp, 20, self.experiment.width, self.screen.get_height() - 40)
        pygame.draw.rect(self.screen, (230, 34, 114), self.target)
        
        self.running = True


    def game_loop(self):
        ''' Main game loop '''

        while self.running and (self.experiment.trials is None or self.experiment.dist_to_target.size < self.experiment.trials):   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.exp_running:  # Left mouse button
                        self.start_experiment()
                    elif event.button == 1 and self.exp_running:
                        self.end_experiment(event.pos)    

            pygame.display.update()
            self.fps_clock.tick(self.fps)

        time.sleep(1)
        pygame.quit()
        self.experiment.save_results()
        self.experiment.print_results()

    def start_experiment(self):
        self.exp_running = True
        self.exp_start_time = time.time()
        pygame.mouse.set_pos((50, self.screen.get_height() // 2))
        time.sleep(self.experiment.visibility_time)
        pygame.mouse.set_visible(False)
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.screen.get_width(), self.screen.get_height()))

    def end_experiment(self, pos: int):
        self.exp_running = False
        end_time = time.time() 
        pygame.mouse.set_visible(True)
        
        dist = pos[0] - self.target[0] - (self.experiment.width / 2) 
        abs_dist = abs(dist)
        self.experiment.add_score(dist, end_time - self.exp_start_time)

        
        max_distance = max(self.experiment.amp, self.screen.get_width() - (self.experiment.amp + self.experiment.width))
        
        normalized_dist = min((abs_dist**0.3) / (max_distance**0.3), 1.0)
        color = (int(255 * normalized_dist), int(255 * (1 - normalized_dist)), 8)

        pygame.draw.rect(self.screen, (230, 34, 114), self.target)
        pygame.draw.circle(self.screen, color, pos, 10)


    def run(self):
        self.game_loop()