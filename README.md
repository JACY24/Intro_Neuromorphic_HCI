# Intro Neuromorphic HCI
Project for the course Introduction to Neuromorphic Human Computer Interaction.

## Project idea

We want to conduct the following experiment: participants get a screen with a mouse, and a target shown on the screen. The goal is to move the cursor from a starting position, to the target. Once a participant starts moving the mouse, they get 'blinded' (i.e. the screen is blacked out). Once they think they have reached the target, they get to see where they actually ended up. By repeating this experiment multiple times with the same start and target positions, we predict participants get closer and closer to the goal.

With this experiment, a user starts with some idea about what movement to make (from start to goal), and through training, the participant updates their believes and we predict the variance of getting to the goal gets smaller and smaller.

From the experiment point of view, you could thus argue that the correct movement is the actual target, since a user is training to make the correct movement, not really to move to the correct target position, since they already now what the target position is from the start.

As data we collect the distance between where the user ends and the actual target, and movement time. 


## Running the code
1. First make sure to install poetry following [the guide on their website](https://python-poetry.org/docs/). Also install the Also install the [poetry shell plugin](https://github.com/python-poetry/poetry-plugin-shell).
2. Next, run `poetry install` in your terminal, this will install all the required packages you need to run the code
3. To activate the virtual environment in which the packages are now installed, run `poetry shell`
4. In your terminal, navigate to the `Intro_Neuromorphic_HCI` directory, and run `python3 main.py`

### Program manual
Once the code is running, it will prompt to input some initial values:

- `distance`: integer representing the distance from the start_position to the target in pixels
- `width`: integer representing the width of the target in pixels
- `trials`: integer representing the amount of trials to run
- `visibility time`: float representing the amount of seconds until the users vision is obscured

Once these values are provided, the program starts, showing the target on the screen. 
When a user clicks the left mouse button, the cursor will be teleported to the _start-position_. After `visibility time` seconds, all visible queues disappear, and the user can start moving the (invisible) cursor to the target. Once a user clicks again, the target, cursor and click-positions are shown again. When a user clicks again, the second trial will start.
This will continue until `trials` amount of trials have been completed. Afterwards, results are printed in the terminal, as well as saved to a `.csv` file in the `results/` directory.