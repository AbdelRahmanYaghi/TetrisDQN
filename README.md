# TetrisDQN
Here, I create a DQN agent which plays the old NES Tetris.

I will quickly go over the methods which I've used to create this agent, and optimize it as much as I could in the given time that I've worked on it.

## How I trained through an emulater?
What I did is screenshot my other screen, since I have 2 monitors. Since I cropped the actual emulater screen, and grayscaled it, whichh resulted in an image like this:

![link]([https://i.imgur.com/HNGBlg8.png])

Then, to I brainstormed to find the most efficient way to extract information about the playground, which is the most important aspect of the picture, in the least computationally expensive way. And, I though of something incredible that surprisingly worked, and that was to crop the main img to be only the playground, and since the tetris playground is comprised of 20 rows and 10 columns, I compressed the picture into 20x10 pixels. And that DID work, and it resulted in a 2d array, such that any 0 pixels mean that there is no blocks there, and any > 0 pixels meant that there was a piece there.

![alt_text][https://i.imgur.com/quc8UX9.png]

## States
I've exprimented with many, MANY states. Firstly, I tried to use a grid represntation of the playground as an input to a CNN. But it didn't seem to be computationally efficient in my case since I was running everything on my local machine. Then, I proceeded to research more into this topic, and after alot of trial and error, I reached to the conclusion that (Sum_of_heights, Number_of_holes, Bumpiness, Lines_cleared) provided the best quality for the computational power that I have.


