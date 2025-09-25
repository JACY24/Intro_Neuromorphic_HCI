import numpy as np
import datetime
import csv
import os

class Experiment:
    def __init__(self):
        self.dist = None
        self.width = None
        self.scores = np.array([])
        self.times = np.array([])
        self.trials = None

        while type(self.dist) is not int or type(self.width) is not int or type(self.trials) is not int:
            try:
                dist, width, trials = input("Enter distance, width and amount of trials (e.g., '200 50 20'): ").split()
                self.dist = int(dist)
                self.width = int(width)
                self.trials = int(trials)
            except ValueError:
                print("Please enter valid integers for distance, width and trials")
    
    def add_score(self, score: float, time: float):
        self.times = np.append(self.times, time)
        self.scores = np.append(self.scores, score)

    def save_results(self, filename: str = f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"):
        results = os.path.join(os.path.dirname(os.getcwd()), 'results', filename)
        print(f"Saving results to {results}")
        with open (results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Distance", "Width", "Score", "Time"])
            for score, time in zip(self.scores, self.times):
                writer.writerow([self.dist, self.width, score, time])
        

    def print_results(self):
        if self.scores.size == 0:
            print("No scores to display.")
            return

        mean_score = np.mean(self.scores)
        std_dev = np.std(self.scores)
        min_score = np.min(self.scores)
        max_score = np.max(self.scores)

        print("\nExperiment Results:")
        print("-------------------")
        print(f"Distance: {self.dist}, Width: {self.width}")
        print(f"Number of Trials: {self.scores.size}")
        print(f"Mean Dist: {mean_score:.2f}")
        print(f"Dist Standard Deviation: {std_dev:.2f}")
        print(f"Dist Min Score: {min_score:.2f}")
        print(f"Dist Max Score: {max_score:.2f}")
        print("-------------------")
        print(f"Mean Time: {np.mean(self.times):.2f}")
        print(f"Time Standard Deviation: {np.std(self.times):.2f}")
        print(f"Time Min: {np.min(self.times):.2f}")
        print(f"Time Max: {np.max(self.times):.2f}")

    def run(self):
        print("Experiment is running")