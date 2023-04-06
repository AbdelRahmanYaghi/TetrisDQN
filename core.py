import pyautogui
import cv2
from PIL import ImageGrab
from PIL import Image
from functools import partial
import numpy as np
import time
import os
from MTM import matchTemplates
from easyocr import Reader
from pieces import piece

class game:
    def __init__(self):
        self.playground = np.zeros((20, 10))
        self.ClearedLines = 0
        self.ScoreRemovalDone = 0
        self.first_piece = True

        self.pastPlacedImg = 0
        self.pastHoles = 0
        self.pastHeighest = 0
        self.pastWidth = 0

        self.reader = Reader(['en'])
        self.screenshot()

    def screenshot(self):
        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        ss = pyautogui.screenshot()
            
        box = (2060,47 , 3060, 984)
        cv_image = np.array(ss.crop(box))[:, :, ::-1]
        
        self.img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        pg = self.img[187:808, 375:686]
        pg[pg > 15] = 255 
        pg = cv2.resize(pg, (10, 20), Image.ANTIALIAS)

        mask = self.playground == 127

        pg[mask] = self.playground[mask]

        self.playground = pg

    @property
    def score(self):
        
        scoreNum = 0

        pgcopy = self.playground.copy()

        full_rows = (pgcopy == [127,127,127,127,127,127,127,127,127,127]).all(-1).sum()

        if (full_rows > 0 and full_rows <= 4):
            self.ClearedLines += full_rows
            scoreNum += (full_rows**2) * 50
            lines = (np.where((pgcopy == np.array([127]*10)).all(axis=1))[0])
            self.update_cleared_lines(lines)


        scoreNum += 5
        # scoreNum -= self.get_holes(self.x_just_dropped, self.y_just_dropped)
        # scoreNum += (self.get_height_curr(self.x_just_dropped))
        scoreNum += self.ScoreRemovalDone


        return scoreNum

    @property
    def done(self):
        deads = np.where(self.playground == 127)
        if len(deads[0]) > 0:
            if min(deads[0]) <= 4: 
                self.ScoreRemovalDone = -25
                return True
        return False
        
    def get_holes(self, xcoords, ycoords):
        arr = np.array(self.playground)
        count = 0

        for x,y in zip(xcoords, ycoords):
            t = x+1
            while(t < arr.shape[0] and arr[t][y] != 127):
                if not(arr[t][y]):
                    count+=1
                t+=1

        return count

    def get_height_curr(self, xcoords):

        return (min(xcoords)) if len(xcoords) > 0 else 0

    def update_dead_blocks(self):
        pg = self.playground
        
        padded_pg = np.pad(pg, [(0, 1), (0, 0)], mode='constant', constant_values=127)
        padded_pg = np.pad(padded_pg, [(1, 0), (1, 1)], mode='constant', constant_values=0)

        coords = np.where(padded_pg == 255)
        coords = sorted([(x, y) for x, y in zip(coords[0], coords[1])], key=lambda x: x[0], reverse=True)
        self.x_just_dropped = []
        self.y_just_dropped = []

        for _ in range(4):
            coords = np.where(padded_pg == 255)
            coords = sorted([(x, y) for x, y in zip(coords[0], coords[1])], key=lambda x: x[0], reverse=True)
            for x, y in coords:
                if 127 in [padded_pg[x][y+1], padded_pg[x+1][y], padded_pg[x][y-1] ,padded_pg[x-1][y]]:
                    self.x_just_dropped.append(x-1)
                    self.y_just_dropped.append(y-1)
                    padded_pg[x][y] = 127

        self.x_just_dropped = self.x_just_dropped
        self.y_just_dropped = list(dict.fromkeys(self.y_just_dropped))
        self.playground = padded_pg[1:-1,1:-1]

    @property
    def get_current_piece(self):
        pg = self.playground

        arr = np.zeros((4, 4))
        coords = np.where(pg == 255)

        if len(coords[0]) != 4:
            return arr

        x_min = min(coords[0])
        y_min = min(coords[1])

        for x_hat, y_hat in zip(coords[0], coords[1]):
            x_true = x_hat - x_min
            y_true = y_hat - y_min

            if x_true >= 4 or y_true >= 4:
                return arr

            arr[x_true][y_true] = 255

        return arr

    @property
    def get_current_piece_ohe(self):
        curr_shape = self.get_current_piece
        ohed = np.zeros(8)

        if np.array_equal(curr_shape, np.array([[255, 255, 255, 0],[0, 255, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[1] = 1
        elif np.array_equal(curr_shape,np.array([[255, 255, 255, 0],[0, 0, 255, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[2] = 1
        elif np.array_equal(curr_shape,np.array([[255 ,255, 0, 0],[0, 255, 255, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[3] = 1
        elif np.array_equal(curr_shape,np.array([[255, 255, 0, 0],[255, 255, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[4] = 1
        elif np.array_equal(curr_shape,np.array([[0, 255, 255, 0],[255, 255, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[5] = 1
        elif np.array_equal(curr_shape,np.array([[255, 255, 255, 0],[255, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[6] = 1
        elif np.array_equal(curr_shape,np.array([[255, 255, 255, 255],[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])):
            ohed[7] = 1
        else:
            ohed[0] = 1

        return ohed

    @property
    def get_current_piece_coords(self):
        pg = self.playground

        coords = np.where(pg == 255)

        if len(coords[0]) != 4:
            return np.zeros((4, 4))
        else:
            return np.array([(x_hat, y_hat) for x_hat, y_hat in zip(coords[0], coords[1])])

    @property
    def get_heights(self):
        arr = self.playground
        inds = [np.where(arr[:, i] == 127)[0][0] if len(np.where(arr[:, i] == 127)[0]) > 0 else arr.shape[0] for i in range(arr.shape[1])]

        pp = [20 - ind for ind in inds]
        return np.array(pp)

    @property
    def newPiecePlaced(self):
        placedImg = self.img[370:780, 185:279]
        if self.first_piece: 
            self.pastPlacedImg = placedImg
            self.first_piece = False
            return False
        elif np.array_equal(placedImg, self.pastPlacedImg):
            return False
        else:
            self.pastPlacedImg = placedImg
            self.update_dead_blocks()
            return True

    @property
    def get_all_holes(self):
        arr = self.playground
        inds = [np.where(arr[:, i] == 127)[0][0] if len(np.where(arr[:, i] == 127)[0]) > 0 else arr.shape[0] for i in range(arr.shape[1])]
        count = 0
        if not inds:
            return 0
        for x,y in zip(inds, range(10)):
            t = x+1
            while(t < arr.shape[0]):
                if not(arr[t][y]):
                    count+=1
                t+=1

        return count

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

    @property
    def score_falling_piece(self):
        coords = self.get_falling_pos
        return sum([(x-10) for x,y in coords])/20

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

    def getNextStates(self):
        states = {}
        X_news = []
        Y_news = []
        curr_piece = piece(self.get_current_piece_ohe)

        print(curr_piece.piece)

        if curr_piece.piece == 0:
            return {tuple(np.array([50, 50, 0, 50]).flatten()): (0, 0)}

        for rot in range(4):
            
            piece_coords_X, piece_coords_Y = curr_piece.flips(rot)
            y_left = min(piece_coords_Y)
            y_right = 9-max(piece_coords_Y)
            
            states[tuple(self.pg2state(self.place_piece(self.get_falling_pos(piece_coords_X, piece_coords_Y))).flatten())] = (0, rot)

            while y_left > 0:
                Ys = [y - y_left for y in piece_coords_Y]
                y_left -= 1
                fall_coords = self.get_falling_pos(piece_coords_X, Ys)
                key = tuple(self.pg2state(self.place_piece(fall_coords)).flatten())
                states[key] = ((y_left + 1)*-1, rot)
                
            while y_right > 0:
                Ys = [y + y_right for y in piece_coords_Y]
                y_right -= 1
                fall_coords = self.get_falling_pos(piece_coords_X, Ys)
                key = tuple(self.pg2state(self.place_piece(fall_coords)).flatten())
                states[key] = ((y_right + 1), rot)

        print(len(states))
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
