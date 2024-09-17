#
# ps9pr4.py (Problem Set 9, Problem 4)
#
# AI Player for use in Connect Four  
#

import random  
from ps9pr3 import *

class AIPlayer(Player):
    """ a data type for a Connect Four board in terms of the AI player 
    (intelligent computer) 
    """
    def __init__(self, checker, tiebreak, lookahead):
        """ constructs a new AIPlayer object """
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
        
    def __repr__(self):
        """ returns a string representing an AIPlayer object and indicates 
        tiebreaking and lookahead strategies. """
        s = 'Player ' + str(self.checker) + ' (' + str(self.tiebreak) + ', ' + str(self.lookahead) + ')'
        return s
    
    def max_score_column(self, scores):
        """ takes a list scores containing a score for each column of the 
        board, and that returns the index of the column with the maximum s
        core. If one or more columns are tied for the maximum score, the 
        method should apply the called AIPlayer‘s tiebreaking strategy to 
        break the tie. """
        max_score = max(scores)
        idx = []
        for i in range(len(scores)):
            if scores[i] == max_score:
                idx += [i]
        if self.tiebreak == 'LEFT':
            return idx[0]
        elif self.tiebreak == 'RIGHT':
            return idx[-1]
        else:
            return random.choice(idx)
        
    def scores_for(self, b):
        """ takes a Board object b and determines the called AIPlayer‘s 
        scores for the columns in b and returns a list containing one score 
        for each column """
        scores = [50] * b.width
        for col in range(b.width):
            if b.can_add_to(col) == False:
                scores[col] = -1
            elif b.is_win_for(self.checker):
                scores[col] = 100
            elif b.is_win_for(self.opponent_checker()):
                scores[col] = 0
            elif self.lookahead == 0:
                scores[col] = 50
            else:
                # need to look ahead
                b.add_checker(self.checker, col)
                opp = AIPlayer(self.opponent_checker(), self.tiebreak, self.lookahead - 1)
                opp_scores = opp.scores_for(b)
                maxopp = max(opp_scores)
                scores[col] = 100 - maxopp
                b.remove_checker(col)
        return scores
    
    def next_move(self, b):
        """ should return the called AIPlayer‘s judgment of its best 
        possible move """
        self.num_moves += 1
        return self.max_score_column(self.scores_for(b))
        
                
                
 