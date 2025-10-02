import numpy as np
import datetime
import csv
import os
import math

class CursorData:
    def __init__(self, step):
        self.data = []
        self.aggregated_data = []
        self.step_size = step*1000000 #How many ms*(time/ms) for each aggregation

    def append_data(self, time, dx, dy):
        self.data.append((time, dx, dy))

    def aggregate_data(self):
        start_time = self.data[0][0]
        end_time = self.data[-1][0]
        nr_steps = math.ceil((end_time - start_time) / self.step_size)
        tmp_data = [(0, 0)] * nr_steps
        for time, dx, dy in self.data:
            i = (time-start_time)//self.step_size
            tmp_data[i] = tmp_data[i][0] + dx, tmp_data[i][1] + dy
        self.aggregated_data.append(tmp_data)
        self.data = []

    def write_to_csv(self, settings, filename: str = f"results_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_cursor.csv"):
        path = os.path.join(os.path.dirname(os.getcwd()), 'results', filename)
        print(f"Saving cursor data to {path}")
        with open (path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amplitude", "Width", "Visible time", "Run", "Time", "Dx", "Dy"])
            for i, data in enumerate(self.aggregated_data):
                for time, (dx, dy) in enumerate(data):
                    writer.writerow([settings["amp"], settings["width"], settings["visibility_time"], i, time, dx, dy])