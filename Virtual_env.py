import numpy as np
import gymnasium as gym
from gym import Env
from gymnasium.spaces import Discrete, Box
from gymnasium import spaces
from pieces import piece

class Virtual_Env():
    def __init__(self):
        self.action_space = gym.spaces.Tuple((
                gym.spaces.Discrete(10),
                gym.spaces.Discrete(4),
            ))

        self.observation_space = (
            spaces.Box(low=0, high=20, shape=(12,), dtype=np.int32)
        )

        self.playground = np.zeros((20, 10))
        
        self.ClearedLines = 0
        self.first_piece = True

    def generate_next_piece(self):
        rand = np.zeros((8))
        rand[np.random.randint(low = 1, high=7)] = 1
        self.piece = piece(rand)
        
    def step(self, action):
        indx_of_state = list(self.next_possible_states.values()).index(action)
        
        self.playground = np.array(list(self.next_possible_states.keys())[indx_of_state]).reshape((20,10))
        state = self.pg2state(self.playground)

        done = self.get_done() 
        reward = self.get_score()
        self.update_dead_blocks()
        self.generate_next_piece()
        self.next_possible_states = self.getNextStates(self.piece)

        info = {}
        return state, reward, done, info

    def render(self):
        pass

    def reset(self):

        self.playground = np.zeros((20, 10))
        
        self.generate_next_piece()

        self.ClearedLines = 0
        self.first_piece = True

        state = self.pg2state(self.playground)
                
        self.next_possible_states = self.getNextStates(self.piece)

        return state

    def update_cleared_lines(self, coordOfLines):

        self.playground = np.array([line for num, line in enumerate(self.playground) if num not in coordOfLines])

        for i in coordOfLines:
            self.playground = np.insert(self.playground, 0 , np.zeros(10), axis = 0)

    def place_piece(self, coords):
        pgcopy = self.playground.copy()
        for x, y in coords:
            pgcopy[x][y] = 127
        
        return pgcopy


    @property
    def bumpiness(self):
        heights = self.get_heights
        return  sum([abs(x1 - x2) for x1, x2 in zip(heights[:-1], heights[1:])])

    def getNextStates(self, piece):
        states = {}
        X_news = []
        Y_news = []
        curr_piece = piece

        if curr_piece.piece == 0:
            return {tuple(np.array([50, 50, 0, 50]).flatten()): (0, 0)}

        for rot in range(4):
            
            piece_coords_X, piece_coords_Y = curr_piece.flips(rot)
            y_left = min(piece_coords_Y)
            y_right = 9-max(piece_coords_Y)
            
            states[tuple(self.place_piece(self.get_falling_pos(piece_coords_X, piece_coords_Y)).flatten())] = (0, rot)

            while y_left > 0:
                Ys = [y - y_left for y in piece_coords_Y]
                y_left -= 1
                fall_coords = self.get_falling_pos(piece_coords_X, Ys)
                key = tuple(self.place_piece(fall_coords).flatten())
                states[key] = ((y_left + 1)*-1, rot)
                
            while y_right > 0:
                Ys = [y + y_right for y in piece_coords_Y]
                y_right -= 1
                fall_coords = self.get_falling_pos(piece_coords_X, Ys)
                key = tuple(self.place_piece(fall_coords).flatten())
                states[key] = ((y_right + 1), rot)

        return states

    def pg2state(self, pg):
        state = []
        inds = [np.where(pg[:, i] == 127)[0][0] if len(np.where(pg[:, i] == 127)[0]) > 0 else pg.shape[0] for i in range(pg.shape[1])]

        heights = [20 - inds for inds in inds]

        bumpiness = sum([abs(x1 - x2) for x1, x2 in zip(heights[:-1], heights[1:])])

        count = 0
        if not inds:
            return 0
        for x,y in zip(inds, range(10)):
            t = x+1
            while(t < pg.shape[0]):
                if not(pg[t][y]):
                    count+=1
                t+=1

        lines = len(np.where((pg == np.array([127]*10)).all(axis=1))[0])

        return  np.array([sum(heights) - (lines * 10), bumpiness, lines, count])

    def get_done(self):
        deads = np.where(self.playground == 127)
        if len(deads[0]) > 0:
            if min(deads[0]) <= 4: 
                self.ScoreRemovalDone = -25
                return True
        return False

    def get_score(self):
        
        scoreNum = 0

        pgcopy = self.playground.copy()

        full_rows = (pgcopy == [127,127,127,127,127,127,127,127,127,127]).all(-1).sum()

        if (full_rows > 0 and full_rows <= 4):
            self.ClearedLines += full_rows
            scoreNum += (full_rows**2) * 50
            lines = (np.where((pgcopy == np.array([127]*10)).all(axis=1))[0])
            self.update_cleared_lines(lines)

        scoreNum += 1

        return scoreNum

    def get_falling_pos(self, xcoords, ycoords):
        arr = np.array(self.playground)
        currs = [(x, y) for x, y in zip(xcoords, ycoords)]

        while all(curr[0] < (arr.shape[0]-1) for curr in currs):
            if np.array_equal(currs, np.zeros((4,2))):
                return [(10,10), (10,10), (10,10), (10, 10)]
            if any(arr[curr[0]+1][curr[1]] == 127 for curr in currs):
                break
            currs = [(i[0]+1, i[1]) for i in currs]

        return currs

    def update_dead_blocks(self):
        pg = self.playground
        
        padded_pg = np.pad(pg, [(0, 1), (0, 0)], mode='constant', constant_values=127)
        padded_pg = np.pad(padded_pg, [(1, 0), (1, 1)], mode='constant', constant_values=0)

        coords = np.where(padded_pg == 255)
        coords = sorted([(x, y) for x, y in zip(coords[0], coords[1])], key=lambda x: x[0], reverse=True)

        for _ in range(4):
            coords = np.where(padded_pg == 255)
            coords = sorted([(x, y) for x, y in zip(coords[0], coords[1])], key=lambda x: x[0], reverse=True)
            for x, y in coords:
                if 127 in [padded_pg[x][y+1], padded_pg[x+1][y], padded_pg[x][y-1] ,padded_pg[x-1][y]]:
                    padded_pg[x][y] = 127

        self.playground = padded_pg[1:-1,1:-1]