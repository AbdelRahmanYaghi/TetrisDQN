import gymnasium as gym
from gym import Env
from gymnasium.spaces import Discrete, Box
from gymnasium import spaces
import random
import numpy as np
from core import game
import keyboard
import time
import pyautogui
from key_inputs import PressKey, ReleaseKey, F1, W, LeftArrow, RightArrow, DownArrow, S
from numpy import newaxis
import random

class TetrisEnv(Env):
    def __init__(self):
        self.game = game()
        self.action_space = gym.spaces.Tuple((
                gym.spaces.Discrete(10),
                gym.spaces.Discrete(4),
            ))
        self.observation_space = (
            spaces.Box(low=0, high=20, shape=(12,), dtype=np.int32)
        )
        
    def step(self, action):

        loc, rot = action

        for _ in range(rot):
            PressKey(S)
            time.sleep(0.05)
            ReleaseKey(S)
            time.sleep(0.07)

        if loc <= 0:
            for _ in range(loc * -1):
                PressKey(LeftArrow)
                time.sleep(0.05)
                ReleaseKey(LeftArrow)
                time.sleep(0.07)

        elif loc > 0:
            for _ in range(loc):
                PressKey(RightArrow)
                time.sleep(0.05)
                ReleaseKey(RightArrow)
                time.sleep(0.07)
        else:
            pass

        self.hard_drop()
        
        self.game.screenshot()

        state = np.array([sum(self.game.get_heights), self.game.bumpiness, self.game.ClearedLines, self.game.get_all_holes])

        done = self.game.done 
        reward = self.game.score
        self.game.update_dead_blocks()
        info = {}
        return state, reward, done, info

    def render(self):
        pass

    def hard_drop(self):
        while True:
            PressKey(DownArrow)
            time.sleep(0.02)
            self.game.screenshot()
            if self.game.newPiecePlaced or self.game.done:
                ReleaseKey(DownArrow)
                return

    def reset(self):
        # print('Env reset!')
        PressKey(F1)
        time.sleep(0.2)
        ReleaseKey(F1)
        time.sleep(random.uniform(0, 0.5))
        PressKey(W)
        time.sleep(0.2)
        ReleaseKey(W)
        time.sleep(0.8)
        self.game.playground = np.zeros((20, 10))
        self.game.ClearedLines = 0
        self.game.ScoreRemovalDone = 0
        self.game.first_piece = True

        self.pastPlacedImg = 0
        self.game.pastHoles = 0
        self.game.pastHeighest = 0
        self.game.pastWidth = 0

        self.game.screenshot()
        state = np.array([sum(self.game.get_heights), self.game.bumpiness, self.game.ClearedLines, self.game.get_all_holes])
                
        return state