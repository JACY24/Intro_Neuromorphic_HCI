import numpy as np
import datetime
import csv
import os

class Experiment:
    def __init__(self):
        self.amp = None
        self.width = None
        self.trials = None
        self.visibility_time = None
        self.dist_to_target = np.array([])
        self.times = np.array([])

        while type(self.amp) is not int or type(self.width) is not int or type(self.trials) is not int and self.visibility_time is not float:
            try:
                amp, width, trials, vis_time = input("Enter distance, width, amount of trials and visibility time (e.g., '200 50 20 1.5'): ").split()
                self.amp = int(amp)
                self.width = int(width)
                self.trials = int(trials)
                self.visibility_time = float(vis_time)
            except ValueError:
                print("Please enter valid integers for distance, width and trials and a float for visibility time.")
    
    def add_score(self, score: float, time: float):
        self.times = np.append(self.times, time)
        self.dist_to_target = np.append(self.dist_to_target, score)

    def save_results(self, filename: str = f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.csv"):
        results = os.path.join(os.path.dirname(os.getcwd()), 'results', filename)
        print(f"Saving results to {results}")
        with open (results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amplitude", "Width", "Visible time", "Distance", "Time"])
            for score, time in zip(self.dist_to_target, self.times):
                writer.writerow([self.amp, self.width, self.visibility_time, score, time])
        

    def print_results(self):
        if self.dist_to_target.size == 0:
            print("No scores to display.")
            return

        mean_score = np.mean(self.dist_to_target)
        std_dev = np.std(self.dist_to_target)
        min_score = np.min(self.dist_to_target)
        max_score = np.max(self.dist_to_target)

        print("\nExperiment Results:")
        print("-------------------")
        print(f"Distance: {self.amp}, Width: {self.width}, Trials: {self.trials}, Visibility Time: {self.visibility_time}")
        print(f"Mean Dist: {mean_score:.2f}")
        print(f"Dist Standard Deviation: {std_dev:.2f}")
        print(f"Dist Min Dist: {min_score:.2f}")
        print(f"Dist Max Dist: {max_score:.2f}")
        print("-------------------")
        print(f"Mean Time: {np.mean(self.times):.2f}")
        print(f"Time Standard Deviation: {np.std(self.times):.2f}")
        print(f"Time Min: {np.min(self.times):.2f}")
        print(f"Time Max: {np.max(self.times):.2f}")
    
    def get_settings(self):
        return {"amp": self.amp, 
                "width": self.width, 
                "visibility_time": self.visibility_time
                }

    def run(self):
        print("Experiment is running")