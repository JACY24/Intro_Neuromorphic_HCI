# Intro_Neuromorphic_HCI
project for the course Introduction to Neuromorphic Human Computer Interaction.

# Project idea

We want to conduct the following experiment: participants get a screen with a mouse, and a target shown on the screen. The goal is to move the cursor from a starting position, to the target. Once a participant starts moving the mouse, they get 'blinded' (i.e. the screen is blacked out). Once they think they have reached the target, they get to see where they actually ended up. By repeating this experiment multiple times with the same start and target positions, we predict participants get closer and closer to the goal.

With this experiment, a user starts with some idea about what movement to make (from start to goal), and through training, the participant updates their believes and we predict the variance of getting to the goal gets smaller and smaller.

From the experiment point of view, you could thus argue that the correct movement is the actual target, since a user is training to make the correct movement, not really to move to the correct target position, since they already now what the target position is from the start.

As data we collect the distance between where the user ends and the actual target, and movement time. 


## Code setup

- Spawn a screen with a starting point
- When user clicks on starting point:
    - show goal
    - freeze cursor
- x seconds after freezing, black-out screen
- user tries to move cursor to goal
- when user clicks on (hopefully) the goal
    - show screen again

## Todo
- Create code
    - data export als csv
- Verwerk data uit csv
- Do experiment

- Make Report
- Make presentation
 