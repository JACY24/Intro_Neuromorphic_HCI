import pygame
import experiment as exp
import time
import threading
import json
import csv
import datetime
import os
from libpointing.libpointing import PointingDevice, DisplayDevice, TransferFunction
from cursor_data import CursorData


class Program:
    def __init__(self, width=1200, height=800, fps=60, title="Blinded Fitts' Law Experiment", icon_path='../img/target.png'):
        # initialize experiment
        self.experiment = exp.Experiment()
        self.exp_start_time = None
        self.exp_running = False
        self.exp_between = False
        self.experiment_trials = []
        self.runs_per_trial = 20

        self.results_file_path = os.path.join(os.path.dirname(os.getcwd()), 'results', f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.csv")
        self.cursor_file_path = os.path.join(os.path.dirname(os.getcwd()), 'results', f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_cursor.csv")
        self.experiments_file_name = os.path.join(os.path.dirname(os.getcwd()), 'Intro_Neuromorphic_HCI', "experiments.json")
        with open(self.results_file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amplitude", "Width", "Visible time", "Distance", "Time"])
        with open(self.cursor_file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amplitude", "Width", "Visible time", "Run", "Time", "Dx", "Dy"])
        self.load_json_experiments()
        self.from_left = True

        pygame.init()

        # initialize pygame window
        self.screen = pygame.display.set_mode((width, height))
        self.screen_width = width
        self.screen_height = height
        self.screen.fill((255, 255, 255))
        self.fps_clock = pygame.time.Clock()
        self.fps = fps
        self.icon = pygame.image.load(icon_path)

        # set window title and icon
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(title)

        # Cursor
        self.pdev = PointingDevice.create("any:?vendor=0x046D&product=0xc53f")
        self.ddev = DisplayDevice.create("any:")
        self.tfct = TransferFunction(b"constant:?cdgain=4", self.pdev, self.ddev)
        self.dp_x_res = self.ddev.getResolution()[0]/self.pdev.getResolution()
        self.dp_y_res = self.ddev.getResolution()[1]/self.pdev.getResolution()
        self.cursor_data = CursorData(100) # ms per aggregated time interval
        self.pdev.setCallback(self.cb_fct)
        self.record_cursor_data = False
        self.x = 50
        self.y = self.screen.get_height() // 2

        self.color = (0,0,0)
        self.pos = (0,0)

        self.cursor_visible = True
        self.target_visible = True
        self.pos_visible = False
        
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
        pygame.mouse.set_visible(False)
        for (amp, width, time_visible) in self.experiment_trials:
            threading.Thread(target=self.between_trials).start()
            self.experiment.set_settings(amp, width, self.runs_per_trial, time_visible)
            self.target = (self.experiment.amp, 20, self.experiment.width, self.screen.get_height() - 40)
            self.experiment.reset_experiment()
            self.running = True
            for direction in [True, False]:
              self.from_left = direction
              trial_count = 0
              while self.running and trial_count < self.experiment.trials: 
                  for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                          self.running = False
                      if event.type == pygame.MOUSEBUTTONDOWN:
                          if event.button == 1 and not self.exp_running and not self.exp_between:  # Left mouse button
                              if event.pos[0] >= self.start[0] and event.pos[0] <= self.start[0] + self.start[2] and event.pos[1] >= self.start[1] and event.pos[1] <= self.start[1] + self.start[3]:
                                self.start_experiment()
                          elif event.button == 1 and self.exp_running:
                              trial_count += 1
                              if trial_count == self.experiment.trials and self.from_left:
                                self.from_left = False
                              self.end_experiment(event.pos)
                             
                              if trial_count < self.experiment.trials:
                                  threading.Thread(target=self.between_experiment).start()
                  self.draw_screen()
                  pygame.display.update()
                  pygame.mouse.set_pos((self.x , self.y))
                  self.fps_clock.tick(self.fps)
            self.experiment.save_results(filename = self.results_file_path)
            self.experiment.print_results()
            self.cursor_data.write_to_csv(self.experiment.get_settings(), path = self.cursor_file_path)
        pygame.quit()

    def start_experiment(self):
        ''' Start the experiment '''

        self.exp_running = True
        self.exp_start_time = time.time()
        self.x = 50
        self.y = self.screen.get_height() // 2
        
        self.record_cursor_data = True
        self.cursor_visible = False

    def end_experiment(self, pos: int):
        ''' End the experiment and calculate score '''

        self.exp_running = False
        self.exp_between = True
        self.record_cursor_data = False
        self.pos = pos
        end_time = time.time()
        
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
        self.color = (int(255 * normalized_dist), int(255 * (1 - normalized_dist)), 8)

        self.cursor_visible = True
        self.target_visible = True
        self.pos_visible = True

    def between_experiment(self):
        time.sleep(self.experiment.visibility_time)
        self.target_visible = False # Geen idee of deze wel hier hoeft of niet, misschien is het beter om de target altijd te laten zien
        self.pos_visible = False
        self.exp_between = False
        # Redraw screen with targets and feedback
        self.draw_targets()
        pygame.draw.circle(self.screen, color, pos, 10)

    def between_trials(self):
        self.target_visible = True
        self.pos_visible = False
        time.sleep(2)
        self.target_visible = False
        self.exp_between = False


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
        rx *= self.dp_x_res
        ry *= self.dp_y_res
        self.x = max(min(self.x + rx, self.screen_width), 0)
        self.y = max(min(self.y + ry, self.screen_height), 0)
        if self.record_cursor_data:
            self.cursor_data.append_data(timestamp, dx, dy)

    def draw_cursor(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 5, 5)

    def load_json_experiments(self):
        with open(self.experiments_file_name, "r") as f:
            experiments = json.load(f)
            self.runs_per_trial = experiments["runs_per_trial"]
            for trial in experiments["experiments"]:
                self.add_experiment(trial)

    def add_experiment(self, trial):
            self.experiment_trials.append((trial["amp"], trial["width"], trial["visible_time"]))

    def run(self):
        self.game_loop()