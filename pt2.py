import random, time

# from KevinAI import best_strategy
import sys
#also good version before break

N = 8
directions = [1, -1, 10, -10, 11, -11, 9, -9]
start_state = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
bad = {12, 17, 21, 28, 71, 82, 78, 87}
corners = {11, 18, 88, 81}
really_bad = {22, 27, 72, 77}
value_states = dict()
value_states_end = dict()
BEGINNING_LAYERS = 4
LAYERS = 4
END_LAYERS = 100
TOKEN = 0
weight_matrix_beginning = \
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  9, -4,  6,  6,  6,  6, -4,  9,  0,
     0, -4, -8, -2, -2, -2, -2, -8, -4,  0,
     0,  6, -2,  0,  0,  0,  0, -2,  6,  0,
     0,  6, -2,  0,  2,  2,  0, -2,  6,  0,
     0,  6, -2,  0,  2,  2,  0, -2,  6,  0,
     0,  6, -2,  0,  0,  0,  0, -2,  6,  0,
     0, -4, -8, -2, -2, -2, -2, -8, -4,  0,
     0,  9, -4,  6,  6,  6,  6, -4,  9,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

weight_matrix = \
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  9, -3,  6,  3,  3,  6, -3,  9,  0,
     0, -3, -5, -2, -2, -2, -2, -5, -3,  0,
     0,  6, -2,  0,  0,  0,  0, -2,  6,  0,
     0,  3, -2,  0,  2,  2,  0, -2,  3,  0,
     0,  3, -2,  0,  2,  2,  0, -2,  3,  0,
     0,  6, -2,  0,  0,  0,  0, -2,  6,  0,
     0, -3, -5, -2, -2, -2, -2, -5, -3,  0,
     0,  9, -3,  6,  3,  3,  6, -3,  9,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

next_to_corners = {11: (12, 21, 22), 18: (17, 21, 28), 81: (71, 72, 82), 88: (78, 77, 87)}



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
    for d in directions:
        k = index + d
        while board[k] == board[index]:
            k += d
        if board[k] == "?":
            count += 1
    return True if count > 3 else False


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
            # x = best_strategy(state, "o")
            x = rand(poss)
            print("white chooses", x)
            state = move(state, "o", x)
            chosen.append(x)
        print("--------------------")
    # print(chosen)


def tree_calc(state, poss, token, turn):
    # for p in poss:
    #     if p in corn:
    #         return p
    # for p in poss:
    #     v = move(state, token, p)
    #     vals[v] = p
    # print(vals[max(vals, key=lambda a: evaluate(a, token))])
    # return vals[max(vals, key=lambda a: find_val(a, turn, anti(token)))]
    for n in corners:
        if state[n] == anti(token):
            for j in next_to_corners[n]:
                weight_matrix[j] = -10
                weight_matrix_beginning[j] = -10
    global TOKEN
    TOKEN = token
    if state.count(".") >= 48:
        for p in poss:
            if p in corners:
                for n in next_to_corners[p]:
                    weight_matrix[n] = 10
                    weight_matrix_beginning[n] = 10
                return p
        vals = {}
        maximize_beginning(state, BEGINNING_LAYERS, float("-inf"), float("inf"), token)
        for p in poss:
            v = move(state, token, p)
            vals[v] = p
            if v not in value_states:
                value_states[v] = float("-inf")
        return vals[max(vals, key=lambda a: value_states[a])]
    elif 48 > state.count(".") >= 12:
        for p in poss:
            if p in corners:
                for n in next_to_corners[p]:
                    weight_matrix[n] = 10
                return p
        vals = {}
        maximize(state, LAYERS, float("-inf"), float("inf"), token)
        for p in poss:
            v = move(state, token, p)
            vals[v] = p
            if v not in value_states:
                value_states[v] = float("-inf")
        return vals[max(vals, key=lambda a: value_states[a])]
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
    return (-6 * vd) + (-4 * d) + (10 * c) + (2 * t) + \
           (6 * avd) + (4 * ad) - (10 * ac) + (25 * m) + \
           (10 * stable) - (10 * astable) - (5 * f)
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
    atok = anti(token)
    st = state.count(token)
    ast = state.count(atok)
    t = st - ast
    return t


def eval_weight_mat(state, token, func):
    sum = 0
    for i in range(len(state)):
        if state[i] == token:
            sum += func[i]
    return sum


def minimize_beginning(state, depth, a, b, token):
    p = possibleMoves(state, token)
    if depth == 0 or not p:
        return eval_beginning(state, TOKEN) + eval_weight_mat(state, TOKEN, weight_matrix_beginning)
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
        return eval_beginning(state, TOKEN) + eval_weight_mat(state, TOKEN, weight_matrix_beginning)
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
        time.sleep(1)
        if running.value:
            p = possibleMoves(board, player)
            best_move.value = rand(p)
            best_move.value = tree_calc(board, p, player, 0)


# state = sys.argv[1]
# token = sys.argv[2]
# print(tree_calc(state, possibleMoves(state, token), token, 0))
