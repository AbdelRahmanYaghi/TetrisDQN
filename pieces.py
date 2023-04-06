import numpy as np

class piece():
    def __init__(self, ohe):
        self.piece = np.where(ohe == 1)[0]

    def flips(self, numFlips):
        match self.piece:
            case 1:
                numFlips = numFlips%4
                match numFlips:
                    case 0:
                        return ([0, 0, 0, 1], [4, 5, 6, 5])
                    case 1:
                        return ([0, 1, 1, 2], [5, 4, 5, 5])
                    case 2:
                        return ([0, 1, 1, 1], [5, 4, 5, 6])
                    case 3:
                        return ([1, 2, 2, 3], [5, 5, 6, 5])
            case 2:
                numFlips = numFlips%4
                match numFlips:
                    case 0:
                        return ([0, 0, 0, 1], [4, 5, 6, 6])
                    case 1: 
                        return ([0, 1, 2, 2], [5, 5, 4, 5])
                    case 2: 
                        return ([0, 1, 1, 1], [4, 4, 5, 6])
                    case 3: 
                        return ([0, 0, 1, 2], [5, 6, 5, 5])

            case 3:
                numFlips = numFlips%2
                match numFlips:
                    case 0:
                        return ([0, 0, 1, 1], [4, 5, 5, 6])
                    case 1: 
                        return ([0, 1, 1, 2], [6, 5, 6, 5])
            case 4:
                return ([0, 0, 1, 1], [4, 5, 4, 5])    
            case 5:
                numFlips = numFlips%2
                match numFlips:
                    case 0:
                        return ([0, 0, 1, 1], [5, 6, 4, 5])
                    case 1: 
                        return ([0, 1, 1, 2], [5, 5, 6, 6])

            case 6:
                numFlips = numFlips%4
                match numFlips:
                    case 0:
                        return ([0, 0, 0, 1], [4, 5, 6, 4])
                    case 1: 
                        return ([0, 0, 1, 2], [4, 5, 5, 5])
                    case 2: 
                        return ([0, 1, 1, 1], [6, 4, 5, 6])
                    case 3: 
                        return ([0, 1, 2, 2], [5, 5, 5, 6])
            case 7:
                numFlips = numFlips%2
                match numFlips:
                    case 0:
                        return ([0, 0, 0, 0], [3, 4, 5, 6])
                    case 1: 
                        return ([0, 1, 2, 3], [5, 5, 5, 5])

            case 0:
                return ([-1, -1, -1, -1], [-1, -1, -1, -1])