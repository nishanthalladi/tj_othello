import random, time

# import KevinAI
import sys
#edgebot
N = 8
directions = [1, -1, 10, -10, 11, -11, 9, -9]
start_state = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
bad = {12, 17, 21, 28, 71, 82, 78, 87}
corners = {11, 18, 88, 81}
really_bad = {22, 27, 72, 77}
edges = {i for i in range(11, 19)} | {i for i in range(81, 89)}\
        | {i for i in range(11, 91, 10)} | {i for i in range(18, 98, 10)} - corners - bad
value_states = dict()
value_states_end = dict()
BEGINNING_LAYERS = 4
LAYERS = 4
END_LAYERS = 100
TOKEN = 0
"""
11 12 13 14 15 16 17 18
21 22 23 24 25 26 27 28
31 32 33 34 35 36 37 38
41 42 43 44 45 46 47 48
51 52 53 54 55 56 57 58
61 62 63 64 65 66 67 68
71 72 73 74 75 76 77 78
81 82 83 84 85 86 87 88"""
weight_matrix_beginning = \
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0, 20, -4,  8,  0,  0,  8, -4, 20,  0,
     0, -4, -8, -3, -3, -3, -3, -8, -4,  0,
     0,  8, -3,  0,  0,  0,  0, -3,  8,  0,
     0,  0, -3,  0,  2,  2,  0, -3,  0,  0,
     0,  0, -3,  0,  2,  2,  0, -3,  0,  0,
     0,  8, -3,  0,  0,  0,  0, -3,  8,  0,
     0, -4, -8, -3, -3, -3, -3, -8, -4,  0,
     0, 20, -4,  8,  0,  0,  8, -4, 20,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

weight_matrix = \
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0, 20, -3,  8,  1,  1,  8, -3, 20,  0,
     0, -3, -5, -1, -1, -1, -1, -5, -3,  0,
     0,  8, -1,  2,  0,  0,  2, -1,  8,  0,
     0,  1, -1,  0,  2,  2,  0, -1,  1,  0,
     0,  1, -1,  0,  2,  2,  0, -1,  1,  0,
     0,  8, -1,  2,  0,  0,  2, -1,  8,  0,
     0, -3, -5, -1, -1, -1, -1, -5, -3,  0,
     0, 20, -3,  8,  1,  1,  8, -3, 20,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

next_to_corners = {11: (12, 21, 22), 18: (17, 21, 28), 81: (71, 72, 82), 88: (78, 77, 87)}


def next_to_edges(n):
    return n + 1, n - 1 if 18 > n > 81 else n + 10, n - 10


def adjust_mat(mat, state):
    for n in edges:
    #     if state[n] == anti(TOKEN):
    #         for j in next_to_edges(n):
    #             if j in edges:
    #                 for k in next_to_edges(j):
    #                     if k in really_bad:
    #                         continue
    #                     mat[k] = 10
    #             mat[j] = -10
        if state[n] == TOKEN:
            for j in next_to_edges(n):
    #             if j in edges:
    #                 for k in next_to_edges(j):
    #                     mat[k] = -10
                mat[j] = 10
    for n in corners:
        if state[n] == anti(TOKEN):
            for j in next_to_corners[n]:
                mat[j] = -100
        if state[n] == TOKEN:
            for j in next_to_corners[n]:
                mat[j] = 100


def anti(token):
    return "@" if token == "o" else "o"


def check_valid(board, index, token):
    for dir in directions:
        k = index + dir
        if board[k] != anti(token):
            continue
        while board[k] == anti(token):
            k += dir
        if board[k] == token:
            return True
    return False


def count_stable(board, token):
    count = 0
    for i in range(len(board)):
        if board[i] == token:
            count += 1 if is_stable(board, i) else 0
    return count


def is_stable(board, index):
    count = 0
    fcount = 0
    for d in directions:
        k = index
        while board[k] == board[index]:
            k += d
        if board[k] == "?":
            count += 1
        if board[k] != ".":
            fcount += 1
    return True if count >= 5 or fcount >= 8 else False


def frontier_count(board, index):
    count = 0
    for d in directions:
        k = index + d
        if board[k] == ".":
            return 1
            # count += 1
    # return count
    return 0


def total_frontier(board, token):
    count = 0
    for i in range(len(board)):
        if board[i] == token:
            count += frontier_count(board, i)
    return count / 8


def possibleMoves(board, token):
    poss = []
    for index in range(len(start_state)):
        if board[index] != ".":
            continue
        if check_valid(board, index, token):
            poss.append(index)
    return poss


def move(state, token, index):
    state = state[:index] + token + state[index + 1:]
    f = state
    for dir in directions:
        k = index + dir
        g = f[k]
        t = anti(token)
        while f[k] == anti(token):
            f = f[:k] + token + f[k + 1:]
            k += dir
        if f[k] != token:
            f = state
            continue
        state = f
    return f


def print_board(board):
    for i in range(10):
        print(" ".join(board[10 * i:10 * i + 10]))


def rand(poss):
    return random.choice(poss)


def set_discs(state, token):
    discs = set()
    for i in range(len(state)):
        if state[i] == token:
            discs.add(i)
    return discs


def frontier(state, discs):
    front = set()
    for disc in discs:
        for dir in directions:
            if state[disc + dir] == ".":
                front.add(disc)
    return front


def negamax_v_kevin(state):
    chosen = []
    for i in range(N * N + 2):
        print_board(state)
        print(state)
        f = 0
        if i > 5:
            f = 1
        print("Black:", state.count("@"), "White:", state.count("o"))

        if i % 2 == 0:
            poss = possibleMoves(state, "@")
            if not poss:
                poss = possibleMoves(state, "o")
                if not poss:
                    print("Game Over")
                    break
                print("black passes")
                chosen.append(-1)
                print("--------------------")
                continue
            print(sorted(poss))
            x = tree_calc(state, poss, "@", i)
            # x = rand(poss)
            print("black chooses", x)
            state = move(state, "@", x)
            chosen.append(x)
        else:
            poss = possibleMoves(state, "o")
            if not poss:
                poss = possibleMoves(state, "@")
                if not poss:
                    print("Game Over")
                    break
                print("white passes")
                chosen.append(-1)
                print("--------------------")
                continue
            print(sorted(poss))
            x = KevinAI.best_strategy(state, "o")
            # x = rand(poss)
            print("white chooses", x)
            state = move(state, "o", x)
            chosen.append(x)
        print("--------------------")
    # print(chosen)


def tree_calc(state, poss, token, layers):
    # for p in poss:
    #     if p in corn:
    #         return p
    # for p in poss:
    #     v = move(state, token, p)
    #     vals[v] = p
    # print(vals[max(vals, key=lambda a: evaluate(a, token))])
    # return vals[max(vals, key=lambda a: find_val(a, turn, anti(token)))]
    global TOKEN
    TOKEN = token
    if state.count(".") >= 48:
        adjust_mat(weight_matrix_beginning, state)
        #
        vals = {}
        maximize_beginning(state, BEGINNING_LAYERS, float("-inf"), float("inf"), token)
        for p in poss:
            v = move(state, token, p)
            vals[v] = p
            if v not in value_states:
                value_states[v] = float("-inf")
        # return vals[max(vals, key=lambda a: 1 * value_states[a] +
        #                                     5 * eval_weight_mat(a, token, weight_matrix_beginning))]
        return vals[max(vals, key=lambda a: 1 * value_states[a] +
                                            10 * weight_matrix_beginning[vals[a]])]

        # return max(poss, key=lambda p: eval_weight_mat(move(state, token, p), token, weight_matrix_beginning))
        # return max(poss, key=lambda p: weight_matrix_beginning[p])

    elif 48 > state.count(".") >= 10:
        adjust_mat(weight_matrix, state)
        # curr = dict([poss, lambda p: eval_weight_mat(move(state, token, p), token, weight_matrix)])
        # curr = dict((move(state, token, p), eval_weight_mat(move(state, token, p), token, weight_matrix)) for p in poss)
        curr = dict((move(state, token, p), weight_matrix[p]) for p in poss)

        vals = {}
        maximize(state, LAYERS, float("-inf"), float("inf"), token)
        for p in poss:
            v = move(state, token, p)
            vals[v] = p
            if v not in value_states:
                value_states[v] = float("-inf")
        return vals[max(vals, key=lambda a: value_states[a] + 1.2 * curr[a])]
    else:
        vals = {}
        maximize_endgame(state, END_LAYERS, float("-inf"), float("inf"), token)
        for p in poss:
            v = move(state, token, p)
            vals[v] = p
            if v not in value_states_end:
                value_states_end[v] = float("-inf")
        print("ENDGAME")
        return vals[max(vals, key=lambda a: value_states_end[a])]


def mobility(pt, pa):
    b, w = len(pt), len(pa)
    if w == 0:
        return float("inf")
    if (b + w) > 0:
        return (b - w) / (b + w)
    return 0


def evaluate(state, token):  # ADD FRONTIER DISCS AND SWEET 16
    atok = anti(token)
    pt, pa = possibleMoves(state, token), possibleMoves(state, atok)
    m = mobility(pt, pa)
    c, d, vd, ac, ad, avd = 0, 0, 0, 0, 0, 0
    for i in really_bad:
        if state[i] == token:
            vd = 1
        if state[i] == atok:
            avd = 1
    for i in bad:
        if state[i] == token:
            d = 1
        if state[i] == atok:
            ad = 1
    for i in corners:
        if state[i] == token:
            c = 1
        if state[i] == atok:
            ac = 1

    st = state.count(token)
    ast = state.count(atok)
    t = (st - ast) / 64
    if st == 0:
        return float("-inf")
    if ast == 0:
        return float("inf")
    f = total_frontier(state, token) / st
    stable = count_stable(state, token) / st
    astable = count_stable(state, atok) / ast
    return (25 * m) + (10 * stable) - (10 * astable) - (10 * f)
    # return (-2 * t) + (30 * m) + \
    #        (10 * stable) - (10 * astable)\
    #        - (5 * f) - (40 * ac) - (8 * vd)


def eval_beginning(state, token):  # ADD FRONTIER DISCS AND SWEET 16 AND PLAYING OUT FROM CORNERS
    atok = anti(token)
    # pt, pa = possibleMoves(state, token), possibleMoves(state, atok)
    # m = mobility(pt, pa)
    c, d, vd, ac, ad, avd = 0, 0, 0, 0, 0, 0
    for i in really_bad:
        if state[i] == token:
            vd = 1
        if state[i] == atok:
            avd = 1
    for i in bad:
        if state[i] == token:
            d = 1
        if state[i] == atok:
            ad = 1
    for i in corners:
        if state[i] == token:
            c = 1
        if state[i] == atok:
            ac = 1

    st = state.count(token)
    ast = state.count(atok)
    t = (st - ast) / 64
    if st == 0:
        return float("-inf")
    if ast == 0:
        return float("inf")
    f = total_frontier(state, token) / st
    return (-8 * vd) + (-6 * d) + (10 * c) + (-2 * t) + \
           (8 * avd) + (6 * ad) - (10 * ac) + (2 * f)


def eval_endgame(state, token):
    return state.count(token)


def eval_weight_mat(state, token, func):
    sum = 0
    atok = anti(token)
    for i in range(len(state)):
        if state[i] == token:
            sum += func[i]
        # if state[i] == atok:
        #     sum -= func[i]
    return sum


def minimize_beginning(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return eval_weight_mat(state, TOKEN, weight_matrix_beginning)
    val = float("inf")
    for child in p:
        m = maximize_beginning(move(state, token, child), depth - 1, a, b, anti(token))
        val = min(val, m)
        b = min(b, val)
        if a >= b:
            value_states[state] = val
            break
    value_states[state] = val
    return val


def maximize_beginning(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return eval_weight_mat(state, TOKEN, weight_matrix_beginning)
    val = float("-inf")
    for child in p:
        m = minimize_beginning(move(state, token, child), depth - 1, a, b, anti(token))
        val = max(val, m)
        a = max(a, val)
        if a >= b:
            value_states[state] = val
            break
    value_states[state] = val
    return val


def minimize(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return evaluate(state, TOKEN) + eval_weight_mat(state, TOKEN, weight_matrix)
    val = float("inf")
    for child in p:
        m = maximize(move(state, token, child), depth - 1, a, b, anti(token))
        val = min(val, m)
        b = min(b, val)
        if a >= b:
            value_states[state] = val
            break
    value_states[state] = val
    return val


def maximize(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return evaluate(state, TOKEN) + eval_weight_mat(state, TOKEN, weight_matrix)
    val = float("-inf")
    for child in p:
        m = minimize(move(state, token, child), depth - 1, a, b, anti(token))
        val = max(val, m)
        a = max(a, val)
        if a >= b:
            value_states[state] = val
            break
    value_states[state] = val
    return val


def minimize_endgame(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return eval_endgame(state, TOKEN)
    val = float("inf")
    for child in p:
        m = maximize_endgame(move(state, token, child), depth - 1, a, b, anti(token))
        val = min(val, m)
        b = min(b, val)
        if a >= b:
            value_states_end[state] = val
            break
    value_states_end[state] = val
    if val == float("inf"):
        value_states_end[state] = float("-inf")
        return float("-inf")
    return val


def maximize_endgame(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return eval_endgame(state, TOKEN)
    val = float("-inf")
    for child in p:
        m = minimize_endgame(move(state, token, child), depth - 1, a, b, anti(token))
        val = max(val, m)
        a = max(a, val)
        if a >= b:
            value_states_end[state] = val
            break
    value_states_end[state] = val
    return val


# negamax_v_kevin(start_state)


class Strategy():
    # implement all the required methods on your own
    def best_strategy(self, board, player, best_move, running):
        count = 0
        if running.value:
            p = possibleMoves(board, player)
            # best_move.value = rand(p)
            best_move.value = tree_calc(board, p, player, count)
            count += 1


# state = sys.argv[1]
# token = sys.argv[2]
# print(tree_calc(state, possibleMoves(state, token), token, 0))
