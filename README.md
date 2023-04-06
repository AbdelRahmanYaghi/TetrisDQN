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

## General methods I've used

## States
I've exprimented with many, MANY states. Firstly, I tried to use a grid represntation of the playground as an input to a CNN. But it didn't seem to be computationally efficient in my case since I was running everything on my local machine. Then, I proceeded to research more into this topic, and after alot of trial and error, I reached to the conclusion that (Sum_of_heights, Number_of_holes, Bumpiness, Lines_cleared) provided the best quality for the computational power that I have. I also reached the conculsion to use these states because of another [github project](https://github.com/nuno-faria/tetris-ai) which I checked out, and used alot to help me understand how DQN works.



