import pygame
import experiment as exp
import time
from libpointing import PointingDevice, DisplayDevice, TransferFunction
from cursor_data import CursorData

class Program:
    def __init__(self, width=1200, height=800, fps=60, title="Blinded Fitts' Law Experiment", icon_path='../img/target.png'):
        self.experiment = exp.Experiment()
        self.exp_start_time = None
        self.exp_running = False

        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.screen_width = width
        self.screen_height = height
        self.screen.fill((255, 255, 255))
        self.fps_clock = pygame.time.Clock()
        self.fps = fps
        self.icon = pygame.image.load(icon_path)

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(title)

        self.target = (self.experiment.amp, 20, self.experiment.width, self.screen.get_height() - 40)
        pygame.draw.rect(self.screen, (230, 34, 114), self.target)

        # Cursor
        self.pdev = PointingDevice.create("any:?vendor=0x046D&product=0xC537")
        self.ddev = DisplayDevice.create("any:")
        self.tfct = TransferFunction(b"system:", self.pdev, self.ddev)
        self.cursor_data = CursorData(100) # ms per aggregated time interval
        self.pdev.setCallback(self.cb_fct)
        self.record_cursor_data = False
        self.corsor_visible = True
        self.x = 50
        self.y = self.screen.get_height() // 2

        self.color = (0,0,0)
        self.pos = (0,0)

        self.cursor_visible = True
        self.target_visible = True
        self.pos_visible = False
        
        self.running = True


    def game_loop(self):
        ''' Main game loop '''
        pygame.mouse.set_visible(False)

        while self.running and (self.experiment.trials is None or self.experiment.dist_to_target.size < self.experiment.trials):   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.exp_running:  # Left mouse button
                        self.start_experiment()
                    elif event.button == 1 and self.exp_running:
                        self.end_experiment(event.pos)    
            self.draw_screen()
            pygame.display.update()
            pygame.mouse.set_pos((self.x , self.y))
            self.fps_clock.tick(self.fps)

        time.sleep(1)
        pygame.quit()
        self.experiment.save_results()
        self.experiment.print_results()
        self.cursor_data.write_to_csv(self.experiment.get_settings())

    def start_experiment(self):
        self.exp_running = True
        self.exp_start_time = time.time()
        self.x = 50
        self.y = self.screen.get_height() // 2
        time.sleep(self.experiment.visibility_time)
        
        self.record_cursor_data = True
        self.cursor_visible = False
        self.target_visible = False
        self.pos_visible = False

    def end_experiment(self, pos: int):
        self.exp_running = False
        self.record_cursor_data = False
        self.pos = pos
        end_time = time.time()
        
        dist = pos[0] - self.target[0] - (self.experiment.width / 2) 
        abs_dist = abs(dist)
        self.experiment.add_score(dist, end_time - self.exp_start_time)
        self.cursor_data.aggregate_data()

        
        max_distance = max(self.experiment.amp, self.screen.get_width() - (self.experiment.amp + self.experiment.width))
        
        normalized_dist = min((abs_dist**0.3) / (max_distance**0.3), 1.0)
        self.color = (int(255 * normalized_dist), int(255 * (1 - normalized_dist)), 8)

        self.cursor_visible = True
        self.target_visible = True
        self.pos_visible = True

    def draw_screen(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (128, 128, 128), (50 - 5, self.screen_height // 2 - 5, 10, 10))
        if self.target_visible:
            pygame.draw.rect(self.screen, (230, 34, 114), self.target)
        if self.pos_visible:
            pygame.draw.circle(self.screen, self.color, self.pos, 10)
        if self.cursor_visible:
            self.draw_cursor()


    def cb_fct(self, timestamp, dx, dy, button):
        rx,ry=self.tfct.applyd(dx, dy, timestamp)
        self.x = max(min(self.x + dx, self.screen_width), 0) # Should be ry after transformation function is not empty
        self.y = max(min(self.y + dy, self.screen_height), 0) # ^
        if self.record_cursor_data:
            self.cursor_data.append_data(timestamp, dx, dy)

    def draw_cursor(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 5, 5)

    def run(self):
        self.game_loop()