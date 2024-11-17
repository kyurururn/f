import tkinter
import math
import copy
import keyboard
import time
import sys

def next_ply(ply):
    ply += 1
    if ply == 3: ply = 1
    return ply

def flatter(array):
    a = []
    for i in array:
        if isinstance(i,list):
            stack = flatter(i)
            for j in stack:
                a.append(j)
        else:
            a.append(i)
    return a

def max_without_str(array):
    max_num = -100000000
    first = True
    for i in array:
        if isinstance(i,float) or isinstance(i,int):
            if first:
                max_num = i
                first = False
            elif i >= max_num:
                max_num = i
    if max_num == -100000000:
        return "CANT_PUT"
    return max_num

def min_without_str(array):
    min_num = 100000000
    first = True
    for i in array:
        if isinstance(i,float) or isinstance(i,int):
            if first:
                min_num = i
                first = False
            elif i <= min_num:
                min_num = i
    if min_num == 100000000:
        return "CANT_PUT"
    return min_num
                


def check_win(board):
    winner = 0

    for i in range(6):
        for j in range(4):
            check = [board[i][j],board[i][j+1],board[i][j+2],board[i][j+3]]
            if len(list(set(check))) == 1 and board[i][j] != 0:
                winner = board[i][j]

    for i in range(3):
        for j in range(7):
            check = [board[i][j],board[i+1][j],board[i+2][j],board[i+3][j]]
            if len(list(set(check))) == 1 and board[i][j] != 0:
                winner = board[i][j]

    for i in range(3):
        for j in range(4):
            check = [board[i][j],board[i+1][j+1],board[i+2][j+2],board[i+3][j+3]]
            if len(list(set(check))) == 1 and board[i][j] != 0:
                winner = board[i][j]

    for i in range(3,6):
        for j in range(4):
            check = [board[i][j],board[i-1][j+1],board[i-2][j+2],board[i-3][j+3]]
            if len(list(set(check))) == 1 and board[i][j] != 0:
                winner = board[i][j]

    return winner

def put(board,num,ply):
    bb = copy.deepcopy(board)
    check = -1
    if isinstance(num,int): num = [num]

    if 0 not in flatter(bb):return ["FULL",bb]

    for i in num:
        check = -1
        for j in range(6):
            if bb[5-j][i] == 0:
                check = 5 - j
                break
        if check == -1: return ["CANT_PUT",bb]

        bb[check][i] = ply
        ply = next_ply(ply)

    return ["PUT",bb]

def column_evaluation(columns,ply):
    eva = 0
    for i in columns:
        length = len(i)
        for j in range(length - 3):
            if ply in i[j:j+4]:
                num = i[j:j+4].count(ply)
                if num == 1:
                    eva += 0.05 * (length - 3)
                elif num == 2:
                    eva += 0.5 * (length - 3)
                elif num == 3:
                    eva += 5
                elif num == 4:
                    eva += 30000
    return round(eva,10)

def evaluation(board,ply):
    rows = []
    for i in board:
        rows.append(i)
    for i in range(7):
        rows.append(list(x[i] for x in board))
    diagonal = [[2,0],[1,0],[0,0],[0,1],[0,2],[0,3]]
    for i in diagonal:
        x_index = i[1]
        y_index = i[0]
        stack   = []
        for j in range(min([7-x_index,6-y_index])):
            stack.append(board[y_index + j][x_index + j])
        rows.append(stack)
    diagonal = [[3,0],[4,0],[5,0],[5,1],[5,2],[5,3]]
    for i in diagonal:
        x_index = i[1]
        y_index = i[0]
        stack = []
        for j in range(min([7-x_index,1+y_index])):
            stack.append(board[y_index - j][x_index + j])
        rows.append(stack)

    rows_1 = []
    for i in rows:
        stack = []
        for j in i:
            if j == 2:
                if len(stack) >= 4:
                    rows_1.append(stack)
                stack = []
            else:
                stack.append(j)
        if len(stack) >= 4:
            rows_1.append(stack)
    eva_1 = column_evaluation(rows_1,1)

    rows_2 = []
    for i in rows:
        stack = []
        for j in i:
            if j == 1:
                if len(stack) >= 4:
                    rows_2.append(stack)
                stack = []
            else:
                stack.append(j)
        if len(stack) >= 4:
            rows_2.append(stack)

    eva_2 = column_evaluation(rows_2,2)

    if ply == 1:
        return round(eva_1 - eva_2,10)
    elif ply == 2:
        return round(eva_2 - eva_1,10)
    else:
        return round(eva_1 - eva_2,10)

def ai_eva(board,ply_abs,ply,depth,condition,mm,map):
    dd = depth - 1
    evas = []

    if condition == ply_abs and condition >= 1:
        return [30000]
    elif condition != ply_abs and condition >= 1:
        return [-30000]

    for i in range(7):
        cc = condition
        bb = put(board,i,ply)
        b = bb[1]
        if bb[0] != "PUT":
            cc = -1
        elif cc == 0:
            cc = check_win(b)
        if dd >= 1:
            ss = ai_eva(b,ply_abs,next_ply(ply),dd,cc,mm+1,evas)
            if mm % 2 == 0:
                stack = max_without_str(ss)
                evas.append(stack)
            elif mm % 2 == 1:
                stack = min_without_str(ss)
                evas.append(stack)
        else:
            if cc == -1:
                add = "CANT_PUT"
            elif cc == ply_abs and cc >= 1:
                add = 30000
            elif cc != ply_abs and cc >= 1:
                add = -30000
            elif bb[0] == "PUT":
                add = evaluation(b,ply_abs)
            else:
                add = "CANT_PUT"
            evas.append(add)


        minn = min_without_str(map)
        maxx = max_without_str(evas)
        if (isinstance(minn,int) or isinstance(minn,float)) and (isinstance(maxx,int) or isinstance(maxx,float)):
            if mm % 2 == 1 and minn < maxx:
                return evas
        
        minn = min_without_str(evas)
        maxx = max_without_str(map)
        if (isinstance(maxx,int) or isinstance(maxx,float)) and (isinstance(minn,int) or isinstance(minn,float)):
            if mm % 2 == 0 and maxx > minn:
                return evas
            

    return evas

def ai_put(board,ply):
    combi_1 = ai_eva(board,ply,ply,1,0,0,{})
    if max_without_str(combi_1) >= 29000:
        return combi_1.index(max_without_str(combi_1))

    num_z = flatter(board).count(0)
    if num_z >= 6: num_z = 5

    if num_z == 1:
        pass
        return combi_1.index(max_without_str(combi_1))
    else:
        no = []

        combi_2 = ai_eva(board,ply,ply,2,0,1,{})
        for i,index in enumerate(combi_2):
            if isinstance(index,int) or isinstance(index,float):
                if index <= -80000:
                    no.append(i)

        combi_5 = ai_eva(board,ply,ply,num_z,0,1,{})
        max_num = -1
        first = True
        for i,index in enumerate(combi_5):
            if (isinstance(index,float) or isinstance(index,int)) and i not in no:
                if first:
                    max_num = index
                    first = False
                elif index >= max_num:
                    max_num = index

        if max_num in combi_5:
            return combi_5.index(max_num)
        else:
            return combi_5.index(max_without_str(combi_5))

def click(event):
    global ply
    global board
    global ai_think

    if winner >= 1 or ai_think >= 1:
        return
    
    if ply == 1 and players[0] == "human":
        inp = math.floor(event.x / 100)
    elif ply == 2 and players[1] == "human":
        inp = math.floor(event.x / 100)
    else:
        return

    bb = put(board,inp,ply)
    if bb[0] == "PUT":
        board = bb[1]
    else:
        return
    

    ply = next_ply(ply)
    paint()


def paint():
    cvs.delete("all")
    for y in range(6):
        for x in range(7):
            x_index = x * 100
            y_index = y * 100
            cvs.create_rectangle(x_index+2,y_index+2,x_index+100,y_index+100,outline="black",width=2)
            if board[y][x] == 1:
                cvs.create_oval(x_index+10, y_index+10, x_index+90, y_index+90, fill="blue", width=0)
            if board[y][x] == 2:
                cvs.create_oval(x_index+10, y_index+10, x_index+90, y_index+90, fill="red", width=0)

root = tkinter.Tk()
root.state("zoomed")
root.title("リバーシ")
root.resizable(False, False)
cvs = tkinter.Canvas(width=700, height=600, bg="white",highlightthickness=1,highlightbackground="black")
cvs.place(x=300,y=90)

cvs2 = tkinter.Canvas(width=700,height=80)
cvs2.place(x=300,y=5)

ply = 1
winner = 0
ai_think = 0
board = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]


cvs.bind("<Button-1>",click)

paint()

args = sys.argv

players = []

if len(args) >= 2:
    print(args[1])
    if args[1] == "0":
        players = ["human","human"]
    elif args[1] == "1":
        players = ["human","ai"]
    elif args[1] == "2":
        players = ["ai","human"]
    else:
        players = ["ai","ai"]
else:
    players = ["ai","ai"]

next_players = players

while True:
    while winner >= 1:
        if keyboard.is_pressed("1"):
            players = ["human","ai"]
        if keyboard.is_pressed("2"):
            players = ["ai","human"]

        if keyboard.is_pressed("space"):
            winner = 0
            ai_think = 0
            board = [[0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0]]
            cvs2.delete("all")
            paint()

    if flatter(board).count(0) == 0:
        winner = 3

    if ply == 1 and players[0] == "ai":
        if winner <= 0:
            ai_think = 1
            inp = ai_put(board,ply)
            bb = put(board,inp,ply)
            if bb[0] == "PUT":
                board = bb[1]
            paint()
            ply = next_ply(ply)
            time.sleep(1)
            ai_think = 0
    elif ply == 2 and players[1] == "ai":
        if winner <= 0:
            ai_think = 1
            inp = ai_put(board,ply)
            bb = put(board,inp,ply)
            if bb[0] == "PUT":
                board = bb[1]
            paint()
            ply = next_ply(ply)
            time.sleep(1)
            ai_think = 0


    winner = check_win(board)
    if winner == 1:
        cvs2.delete("all")
        cvs2.create_text(350, 40, text="Blue Win!",font=("HG丸ｺﾞｼｯｸM-PRO",50),fill="blue")
    elif winner == 2:
        cvs2.delete("all")
        cvs2.create_text(350, 40, text="Red Win!",font=("HG丸ｺﾞｼｯｸM-PRO",50),fill="red")
    elif winner == 2:
        cvs2.delete("all")
        cvs2.create_text(350, 40, text="Draw...",font=("HG丸ｺﾞｼｯｸM-PRO",50),fill="green")

    root.update()