
import time
import math
import random
import copy
from concurrent.futures import ProcessPoolExecutor
from concurrent import futures 
from heuristic import *

WHITE = 0
BLACK = 2

DELTA = 2

def minimax(board, depth, alpha, beta, is_maximizing, color, tt, timeout, start_time, origin=None):

    win = board.check_win()
    if win is not None:
        return None, heuristic_function(board) * (depth + 1), origin
    
    if depth == 0:
        return None, heuristic_function(board), origin
    
    # TIMEOUT
    if time.time() - start_time >= timeout - DELTA:
        # if is_maximizing:
            # return None, math.inf, None
        # else:
            # return None, -math.inf, None
        return None, heuristic_function(board), origin

    children = board.generate_moves(color)
    best_move = random.choice(children)


    if is_maximizing:
        max_eval = -math.inf
        for child in children:
            board_copy = copy.deepcopy(board)
            board_copy.move(child,color)
            '''
            board_repr = board_copy.gen_state_string()
            row = tt.lookup(board_repr)
            if row is not None:
                old_state, old_score, old_depth = row
                if old_depth > depth:
                    current_eval = row[2]
                else:
                    current_eval = minimax(board_copy, 
                                            depth - 1, 
                                            alpha, 
                                            beta, 
                                            not is_maximizing,
                                            not color,
                                            tt,
                                            timeout, 
                                            start_time)[1]
                    tt.add(depth, board_repr, current_eval)

            else:
            '''
            current_eval = minimax(board_copy, 
                                depth - 1, 
                                alpha, 
                                beta, 
                                not is_maximizing,
                                not color,
                                tt,
                                timeout, 
                                start_time)[1]
            '''tt.add(depth, board_repr, current_eval)'''


            if current_eval > max_eval:
                max_eval = current_eval
                best_move = child
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        if origin:
            return best_move, max_eval, origin
        return best_move, max_eval, None

    else:
        min_eval = math.inf
        for child in children:
            board_copy = copy.deepcopy(board)
            board_copy.move(child,color)

            '''
            board_repr = board_copy.gen_state_string()
            row = tt.lookup(board_repr)
            if row is not None:
                old_state, old_score, old_depth = row
                if old_depth > depth:
                    current_eval = row[2]
                else:
                    current_eval = minimax(board_copy, 
                                            depth - 1,
                                            alpha,
                                            beta,
                                            not is_maximizing,
                                            not color,
                                            tt,
                                            timeout,
                                            start_time)[1]
                    tt.add(depth, board_repr, current_eval)

            else:
            '''
            current_eval = minimax(board_copy, 
                                    depth - 1,
                                    alpha,
                                    beta,
                                    not is_maximizing,
                                    not color,
                                    tt,
                                    timeout,
                                    start_time)[1]
            '''tt.add(depth, board_repr, current_eval)'''


            if current_eval < min_eval:
                min_eval = current_eval
                best_move = child
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        if origin:
            return best_move, min_eval, origin
        return best_move, min_eval, None


def explore(board, depth, alpha, beta, color, tt, threads, timeout, start_time):

    children = board.generate_moves(color)

    if len(board.pawns[WHITE]) < 4 and board.role == 'WHITE':
        depth += 1

    executor =  ProcessPoolExecutor(max_workers=threads)
    wait_for = [
        executor.submit(minimax, copy.deepcopy(board).move(child,color) , depth - 1, alpha, beta, not color, not color, tt, timeout, start_time, child)
        for child in children
    ]
    results = [ f.result() for f in futures.as_completed(wait_for) ]
    results.sort(key=lambda x: x[1], reverse=color)
    

    #for m in results:
    #    print(m)
    return results[0][2], results[0][1]

