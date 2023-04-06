# TetrisDQN
Here, I create a DQN agent which plays the old NES Tetris.

I will quickly go over the methods which I've used to create this agent, and optimize it as much as I could in the given time that I've worked on it.

## How I trained a model through an emulater?
### Extracting Data
What I did is screenshot my other screen, since I have 2 monitors. Since I cropped the actual emulater screen, and grayscaled it, whichh resulted in an image like this:

![photo_1](https://i.imgur.com/HNGBlg8.png?dl=0)

Then, to I brainstormed to find the most efficient way to extract information about the playground, which is the most important aspect of the picture, in the least computationally expensive way. And, I though of something incredible that surprisingly worked, and that was to crop the main img to be only the playground, and since the tetris playground is comprised of 20 rows and 10 columns, I compressed the picture into 20x10 pixels. And that DID work, and it resulted in a 2d array, such that any 0 pixels mean that there is no blocks there, and any > 0 pixels meant that there was a piece there.

![photo_2](https://i.imgur.com/quc8UX9.png?dl=0)

And from this 2d grid representation. I was able to extract any data I wanted.

### Applying actions
For some reason, the library called "keyboard" wasn't able to input actions to the actual emulater, hence I had to use another library called ctypes. Using this, I was able just to run the program, the program then would wait one second for me to click on the emulater window, and then the program would start. Ctypes uses DirectKeyInput (DKI) codes to simulate a button. So I just had to check the buttons I needed online, and then translate them into a DKI format. 

### Actual training process
For the first 3 weeks or so, I used to leave the model to train on the actual game, meaning that I had to wait for it to wait for the pieces to drop, generate new pieces, the ~0.5 needed for a piece to be dead after it had been placed. That took SO MUCH TIME, so what I did is create a virtual enviroment which I've used for training, saying that it sped up the process would be an under-statement. Here are some numbers for comparison:
Without a virtual env: 1000 games would take around 6 hours
With a virtual env: 1000 games would take around 30 minutes

## Q-Values calculation
When creating a Tetris DQN agent, the first thing that comes to mind is to calculate the Q-value for each action, which are (left_move, right_move, flip, and drop). However, after almost 3 weeks of trial and error, and researching, I reached to the conculsion that it could become really hard for the model to predict both how to place a piece and where to place it. I wanted the model to know WHERE to place the piece, hence what I did is check the current piece I am playing, calculate all possible moves which that piece could be in (which are at max 40 - 10 y-axis locations and 4 rotations), and then train the model to predict the Q value for the states. This made a huge difference, since now, all the model had to do is know the best place to drop a piece based on the Q-values. And then, I can drop it using CTYPES. [A paper published by Matt Stevens and Sabeek Pradhan](http://cs231n.stanford.edu/reports/2016/pdfs/121_Report.pdf) was great in helping me understand all of this. And probably saved me more time that I can imagine.

## States
I've exprimented with many, MANY states. Firstly, I tried to use a grid represntation of the playground as an input to a CNN. But it didn't seem to be computationally efficient in my case since I was running everything on my local machine. Then, I proceeded to research more into this topic, and after alot of trial and error, I reached to the conclusion that (Sum_of_heights, Number_of_holes, Bumpiness, Lines_cleared) provided the best quality for the computational power that I have. I also reached the conculsion to use these states because of another [github project](https://github.com/nuno-faria/tetris-ai) which I checked out, and used alot to help me understand how DQN works.

## Actions
First, as mentioned before, I tried training the model to predict one of these possible actions (left, right, flip, drop), but that didn't actually work because it would have made the model alot more complicated because the model would have had to learn HOW to drop and a piece AND WHERE to drop it. Hence, I used what was suggested in both the references I mentioned above , [github project](https://github.com/nuno-faria/tetris-ai) and [the paper](http://cs231n.stanford.edu/reports/2016/pdfs/121_Report.pdf) to drastically decrease the complixity of the model. Also, to speed up the process alittle, after it had done the 2 actions required (moving to the correct Y-axis and flipping the correct amount of time), I asked it to hard drop the piece, but since the NES version of Tetris doesn't have a hard, I just told it to keep dropping it until the piece is "dead". 

## Rewards
I wanted the model to actually learn how to play the game, since I simplified everything for it alittle too much, that's why I only rewarded the agent under 2 conditions, dropping a piece (+1) and clearing a line/s (#ofLines^2 * 50). That means that it didn't know if leaving holes for example was a bad thing or not, neither did it know that placing blocks high was a bad thing either. However, after around 2000 minutes of training (around 6000 games) it had figured out that it alone that leaving holes and building high blocks was a bad thing.

## Final Notes
A) In total, I've trained the final model for around 1600 minutes, however, the number of episodes it completes per hour get lower and lower as time goes in, probably due to increased memory and CPU usage. So, training the model with a better computer and for a longer time should make the model much better.
B) There seems to be a minor issue when the agent clear more than 1 line sometimes, which causes it to freak out and do a random move for 1 action or two. It is probably a bug with the game enviroment (core.py) which I have created which makes it process this action in an incorrect manner.
C) For some reason, despite the model performing very well, the error for calculating the Q value for the states reaches upto 1000 during the training.
