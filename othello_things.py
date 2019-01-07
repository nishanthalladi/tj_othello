def print_board(board):
    for i in range(10):
        print(" ".join(board[10*i:10*i+10]))

print_board('???????????.......o??..o@..o.??...@.o..??...@o@@.??..@ooo..??.@......??........??........???????????')

print(float("inf") *-1)
edges = {i for i in range(11, 19)} | {i for i in range(81, 89)}\
        | {i for i in range(11, 91, 10)} | {i for i in range(18, 99, 10)}
print(edges)