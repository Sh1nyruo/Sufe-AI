'''
同学们可以在get_AI_move函数上测试自己的程序，这只需要返回最佳的落子位置即可
部分大家可能用到的变量和函数汇总：
self.sleep_time = 0 机器对战的时候的停顿时间，在调试阶段，同学们可以设置为0
其他见作业说明文档：

如果同学们在做作业过程中发现有bug，可以联系代码提供者(助教：xhp@163.sufe.edu.cn/18317026869)
'''
import time
from tkinter import *
from tkinter.messagebox import *
from Othello import Othello
import random


class OthelloGUI:
    def __init__(self):
        self.root = Tk('黑白棋')
        self.root.title(" 黑白棋")
        self.black_tile = PhotoImage(file='black.png')
        self.white_tile = PhotoImage(file='white.png')
        self.board_bg = PhotoImage(file='board.png')
        self.info = PhotoImage(file='info2.png')
        self.imgs = [self.black_tile, self.white_tile, self.board_bg, self.info]
        self.cv = Canvas(self.root, bg='green', width=720, height=720)
        self.gameOver = False
        self.gameoverStr = 'Game Over!  Score:'
        self.mainBoard = self.getNewBoard()
        self.playerTile = 'black'
        self.computerTile = 'white'
        self.turn = 'player'
        self.othello = Othello()
        self.white_no_choose=False
        self.black_no_choose=False
        self.AI_player='2018110110-张三'
        self.sleep_time = 0  # 每次停留时间，在调试阶段可以设为0

    # 重置棋盘
    def resetBoard(self):
        '''
        初始化棋盘，黑白棋的最初棋盘上是有两个白棋和黑棋
        :return:
        '''
        for x in range(8):
            for y in range(8):
                self.mainBoard[x][y] = 'none'
        # Starting pieces:
        self.mainBoard[3][3] = 'black'
        self.mainBoard[3][4] = 'white'
        self.mainBoard[4][3] = 'white'
        self.mainBoard[4][4] = 'black'

    def getNewBoard(self):
        '''
        开局建立新棋盘，所有棋子的位置都置为None
        :return:
        '''
        board = []
        for i in range(8):
            board.append(['none'] * 8)
        return board

    # 复制棋盘
    def getBoardCopy(self, board):
        '''
        将传入棋盘的布局复制并返回
        :param board:传入的棋盘布局，是一个8*8的字符串数组
        :return:复制好的棋盘布局数组
        '''
        dupeBoard = self.getNewBoard()
        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]
        return dupeBoard

    def getScoreOfBoard(self, board):
        '''
        获取给定棋盘上黑白双方的棋子数，可以为真实的棋盘mainBoard或者虚拟的棋盘布局
        :param board:传入的棋盘布局
        :return:统计此棋盘布局中黑白棋子的个数dict
        '''
        b_score = 0
        w_score = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'black':
                    b_score += 1
                if board[x][y] == 'white':
                    w_score += 1
        return {'black': b_score, 'white': w_score}

    def makeMove(self, board, tile, x_start, y_start):
        '''
        将一个tile棋子放到(xstart, ystart),之后的棋盘局面，如果有翻转的棋子，将会翻转，
        传入的board是数组，是实参，所以board的值会改变
        :param board:传入棋盘的布局，由于是数组结构，是实参，会被改变，
        :param tile:棋子颜色的字符串，值为“white”或者“black”
        :param x_start:目标位置的x，取值为（0-7）
        :param y_start:目标位置的y，取值为（0-7）
        :return:落子成功则返回True、否则返回False
        '''
        tilesToFlip = self.othello.isValidMove(board, tile, x_start, y_start)
        if tilesToFlip == False:
            return False
        board[x_start][y_start] = tile
        for x, y in tilesToFlip:  # tilesToFlip是需要翻转的棋子列表
            board[x][y] = tile  # 翻转棋子
        return True

    def getValidMoves(self, board, tile):
        '''
        获取棋盘布局board下的可以落子的位置
        :param board: 当前棋盘的布局
        :param tile: 棋子颜色的字符串，值为“white”或者“black”
        :return:返回可以落子位置的list,如[[1,2],[2,3]]
        '''
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.othello.isValidMove(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    # 电脑走法（随机走法，大家也可以写一些稍微复杂的算法自行测试）
    def getComputerMove(self, board, computerTile):
        '''
        将可能的走法打乱，选取第一个可走的位置
        :param board: 传入的棋盘
        :param computerTile: 电脑的棋子颜色的字符串，值为“white”或者“black”
        :return: 走法的数组[x,y],如[2,1] etc.
        '''
        # 获取所以合法走法
        possibleMoves = self.getValidMoves(board, computerTile)
        if not possibleMoves:  # 如果没有合法走法
            print("电脑没有合法走法")
            return None
        # 打乱所有合法走法
        random.shuffle(possibleMoves)
        return possibleMoves[0]


    def isGameOver(self, board):
        '''
        判断游戏是否结束，结束条件为：传入board全部不为空（"none"）
        或者全部为白色棋子、或者全部为黑色棋子，
        或者黑棋和白棋都没地方落子
        :param board:棋盘布局
        :return:游戏是否结束
        '''
        not_have_none = True
        # 棋盘上只剩一种棋子，游戏也结束
        only_white = True
        only_black = True
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'none':
                    not_have_none = False
                if board[x][y] == 'white':
                    only_black = False
                if board[x][y] == 'black':
                    only_white = False
        return not_have_none or only_white or only_black or (self.white_no_choose and self.black_no_choose)

    # 画棋盘背景
    def drawQiPan(self):
        img1 = self.imgs[2]
        self.cv.create_image((360, 360), image=img1)
        self.cv.pack()

    def drawAll(self):
        '''
        画出棋盘和当前布局self.mainBoard的棋子
        :return:
        '''
        self.drawQiPan()
        for x in range(8):
            for y in range(8):
                if self.mainBoard[x][y] == 'black':
                    self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[0])
                    self.cv.pack()
                elif self.mainBoard[x][y] == 'white':
                    self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[1])
                    self.cv.pack()

    def drawCanGo(self):
        '''
        获取当前可以落子的位置的提示信息
        :return:
        '''
        list1 = self.getValidMoves(self.mainBoard, self.playerTile)
        for m in list1:
            x = m[0]
            y = m[1]
            self.cv.create_image((x * 80 + 80, y * 80 + 80), image=self.imgs[3])
            self.cv.pack()

    def callback(self, event):
        '''
        用户走棋
        :param event:用户点击事件，用于获取用户点击位置的坐标。
        :return:
        '''
        # global turn
        # print ("clicked at", event.x, event.y,turn)
        # x=(event.x)//40  #换算棋盘坐标
        # y=(event.y)//40
        if self.gameOver is False and self.turn == 'computer':  # 没轮到玩家走棋
            return
        col = int((event.x - 40) / 80)  # 换算棋盘坐标
        row = int((event.y - 40) / 80)
        if self.mainBoard[col][row] != "none":
            showinfo(title="提示", message="已有棋子")
        if self.makeMove(self.mainBoard, self.playerTile, col, row):  # 将一个玩家棋子放到(col, row)
            if self.getValidMoves(self.mainBoard, self.computerTile) != []:
                self.turn = 'computer'
        # 电脑走棋
        if self.getComputerMove(self.mainBoard, self.computerTile) is None:
            self.turn = 'player'
            showinfo(title="玩家继续", message="玩家继续")
        else:
            self.computerGo()
        # 重画所有的棋子和棋盘
        self.drawAll()
        self.drawCanGo()
        if self.isGameOver(self.mainBoard):  # 游戏结束，显示双方棋子数量
            scorePlayer = self.getScoreOfBoard(self.mainBoard)[self.playerTile]
            scoreComputer = self.getScoreOfBoard(self.mainBoard)[self.computerTile]
            outputStr = self.gameoverStr + "玩家:" + str(scorePlayer) + ":" + "电脑:" + str(scoreComputer)
            if scorePlayer==scoreComputer:
                outputStr+=", 【平 局】"
            elif scorePlayer>scoreComputer:
                outputStr += ", 【玩家胜】"
            else:
                outputStr += ", 【电脑胜】"
            showinfo(title="游戏结束", message=outputStr)
            print(outputStr)

    def computerGo(self):
        '''
        电脑走棋
        :return:
        '''
        if self.gameOver is False and self.turn == 'computer':
            # print("move:",self.getComputerMove(self.mainBoard, self.computerTile) )
            x, y = self.getComputerMove(self.mainBoard, self.computerTile)  # 电脑AI走法
            # x,y =self.get_AI_move(self.computerTile)
            self.makeMove(self.mainBoard, self.computerTile, x, y)
            savex, savey = x, y
            # 玩家没有可行的走法了，则电脑继续，否则切换到玩家走
            if self.getValidMoves(self.mainBoard, self.playerTile) != []:
                self.turn = 'player'
            else:
                if self.getValidMoves(self.mainBoard, self.computerTile) != []:
                    showinfo(title="电脑继续", message="电脑继续")
                    self.computerGo()

    def random_move(self,tile):
        '''
        随机算法
        :param tile: 棋子的颜色
        :return: 落子位置[x,y]，如果没有合法的落子位置，返回false
        '''
        possibleMoves = self.getValidMoves(self.mainBoard, tile)
        if not possibleMoves:  # 如果没有合法走法
            print("{}棋没有合法走法".format(tile))
            return None
        # 打乱所有合法走法
        random.shuffle(possibleMoves)
        return possibleMoves[0]

    def get_baseline_1_move(self,tile):
        '''
        同学们可以换上自己写的其他的baseline的测试函数，与自己写的AI算法对弈
        :param tile:
        :return:
        '''
        inf = 1e8
        
        def cal_values(curboard, tile):
            another = "white" if tile == "black" else "black"
            my_tiles = len(self.getValidMoves(curboard, tile))
            opp_tiles = len(self.getValidMoves(curboard, another))
            
            if my_tiles > opp_tiles:
                return (100 * my_tiles) / (my_tiles + opp_tiles)
            elif my_tiles < opp_tiles:
                return - (100 * opp_tiles) / (my_tiles + opp_tiles)
            else:
                return 0
        
        
        
        def minmax(maxdepth, depth, current_board, player_tile, current_tile, moves, alpha, beta):
            #Terminating condition
            if depth == maxdepth:
                return cal_values(current_board, player_tile), moves
            
            if current_tile == player_tile:
                best = -inf
                best_move = []
                possibleMoves = self.getValidMoves(current_board, current_tile)
                if len(possibleMoves) == 0:
                    return cal_values(current_board, player_tile), None
                for i in range(0,len(possibleMoves)):
                    dupeBoard = self.getBoardCopy(current_board)
                    self.makeMove(dupeBoard, current_tile, possibleMoves[i][0], possibleMoves[i][1])
                    next_tile = "white" if current_tile == "black" else "black"
                    val,move = minmax(maxdepth,depth+1, dupeBoard, player_tile, next_tile, possibleMoves[i], alpha, beta)
                    if best <= val:
                        best = val
                        best_move = possibleMoves[i]
                    alpha = max(alpha, best)
                    
                    if beta <= alpha:
                        break
                return best,best_move
            else:
                best = inf
                best_move = []
                possibleMoves = self.getValidMoves(current_board, current_tile)
                if len(possibleMoves) == 0:
                    return cal_values(current_board, player_tile), None
                for i in range(0,len(possibleMoves)):
                    dupeBoard = self.getBoardCopy(current_board)
                    self.makeMove(dupeBoard, current_tile, possibleMoves[i][0], possibleMoves[i][1])
                    next_tile = "white" if current_tile == "black" else "black"
                    val,move = minmax(maxdepth, depth+1, dupeBoard, player_tile, next_tile, possibleMoves[i], alpha, beta)
                    if best > val:
                        best = val
                        best_move = possibleMoves[i]
                    beta = min(beta, best)
                    
                    if beta <= alpha:
                        break
                return best, best_move
        start_time = time.perf_counter()    
        a = minmax(5, 0, self.mainBoard, tile, tile, [], -inf, inf)[1]
        end_time = time.perf_counter()
        if end_time - start_time < 1:
            a = minmax(6, 0, self.mainBoard, tile, tile, [], -inf, inf)[1]
        end_time = time.perf_counter()
        print("AI time:",end_time - start_time)
        return a        

    def get_baseline_2_move(self,tile):
        def get_score_of_board(board):
            board_weights = [
                [900, -20, 20, 5, 5, 20, -20, 900],
                [-20, -40, -5, -5, -5, -5, -40, -20],
                [20, -5, 15, 3, 3, 15, -5, 20],
                [5, -5, 3, 3, 3, 3, -5, 5],
                [5, -5, 3, 3, 3, 3, -5, 5],
                [20, -5, 15, 3, 3, 15, -5, 20],
                [-20, -40, -5, -5, -5, -5, -40, -20],
                [900, -20, 20, 5, 5, 20, -20, 900]
            ]
            b_score = 0
            w_score = 0
            for x in range(8):
                for y in range(8):
                    if board[x][y] == 'black':
                        b_score += board_weights[x][y]
                    if board[x][y] == 'white':
                        w_score += board_weights[x][y]
            return {'black': b_score, 'white': w_score}
        

        if tile == "white":
            _tile = "black"
        if tile == "black":
            _tile = "white"


        board = self.getBoardCopy(self.mainBoard)

        def do_minimax_with_alpha_beta(board, tile, depth, my_best, opp_best):
            if depth == 0:
                return (get_score_of_board(board)[tile], None)

            move_list = self.getValidMoves(board, tile)

            if not move_list:
                return (get_score_of_board(board)[tile], None)

            for x, y in move_list:
                if self.othello.isOnCorner(x, y):
                    return (get_score_of_board(board)[tile],[x, y])
            best_score = my_best
            best_move = None

            for move in move_list:
                x, y = move
                new_board = self.getBoardCopy(board)
                self.makeMove(new_board, tile, x, y)
                try_tuple = do_minimax_with_alpha_beta(new_board, _tile, depth - 1, -opp_best, -best_score)
                try_score = -try_tuple[0]

                if try_score > best_score:
                    best_score = try_score
                    best_move = move

                if best_score >= opp_best:   #剪枝操作
                    return (best_score, best_move)

            return (best_score, best_move)
        
        start_time =time.perf_counter()
        score, action = do_minimax_with_alpha_beta(board, tile, 7, -1000, 1000)
        end_time = time.perf_counter()
        print("你的时间:", end_time-start_time)
        return action

    def get_baseline_move(self,tile,baseline_num=2):
        '''
        获取baseline的落子位置
        :param tile: 棋子的颜色的字符串，值为“white”或者“black”
        :param baseline_num: baseline的编号
        :return: 返回一个最佳的落子位置[x,y]，如果没有落子位置或baseline编号不合规范，返回None
        '''
        if baseline_num==0:
            return self.random_move(tile)
        elif baseline_num==1:
            return self.get_baseline_1_move(tile)
        elif baseline_num==2:
            return self.get_baseline_2_move(tile)
        else:
            return None

    def get_AI_move(self,tile):
        '''
        这里是同学们需要实现的策略，默认是随机算法，主要是为了让程序跑起来
        同学们需要删掉return这一行，换上自己的算法
        程序的第一行为:self.AI_player='2018110110-张三'，替换成自己的学号-姓名，方便后续程序自动批阅
        :param tile:  棋子颜色的字符串，值为“white”或者“black”
        :return:  返回一个最佳的落子位置[x,y]，如果当前棋子没有可走位置，返回None
        '''
        self.AI_player = '2020111475-顾永威'
        inf = 1e8
        
        #Heuristic function:Component-wise Heuristic with Dynamic Weights
        def cal_values(curboard, tile):
            another = "white" if tile == "black" else "black"
            my_tiles = 0
            opp_tiles = 0
            my_front_tiles = 0
            opp_front_tiles = 0
            
            X_dt = [-1,-1,0,1,1,1,0,-1]
            Y_dt = [0,1,1,1,0,-1,-1,-1]
            weight_matrix = [[20, -3, 11, 8, 8, 11, -3, 20],
                             [-3, -7, -4, 1, 1, -4, -7, -3],
                             [11, -4, 2, 2, 2, 2, -4, 11],
                             [8, 1, 2, -3, -3, 2, 1, 8],
                             [8, 1, 2, -3, -3, 2, 1, 8],
                             [11, -4, 2, 2, 2, 2, -4, 11],
                             [-3, -7, -4, 1, 1, -4, -7, -3],
                             [20, -3, 11, 8, 8, 11, -3, 20]]
            d = 0
            for i in range(8):
                for j in range(8):
                    if curboard[i][j] == tile:
                        d += weight_matrix[i][j]
                        my_tiles += 1
                    elif curboard[i][j] == another:
                        d -= weight_matrix[i][j]
                        opp_tiles += 1
                    if curboard[i][j] != 'none':
                        for k in range(8):
                            x = i + X_dt[k]
                            y = j + Y_dt[k]
                            if x>=0 and x<8 and y>=0 and y<8 and curboard[x][y] == 'none':
                                if curboard[i][j] == tile: my_front_tiles += 1
                                else: opp_front_tiles += 1
                                break
            p = 0
            if my_tiles > opp_tiles:
                p = 100 * my_tiles / (my_tiles + opp_tiles)
            elif my_tiles < opp_tiles:
                p = - (100 * opp_tiles) / (my_tiles + opp_tiles)
            else:
                p = 0
            
            f = 0
            if my_front_tiles > opp_front_tiles:
                f = - (100 * my_front_tiles)/(my_front_tiles+opp_front_tiles)
            elif my_front_tiles < opp_front_tiles:
                f = (100 * my_front_tiles)/(my_front_tiles+opp_front_tiles)
            else:
                f = 0
            
            c = 0
            my_tiles = opp_tiles = 0
            if curboard[0][0] == tile:
                my_tiles += 1
            elif curboard[0][0] == another:
                opp_tiles += 1
            if curboard[0][7] == tile:
                my_tiles += 1
            elif curboard[0][7] == another:
                opp_tiles += 1               
            if curboard[7][0] == tile:
                my_tiles += 1
            elif curboard[7][0] == another:
                opp_tiles += 1   
            if curboard[7][7] == tile:
                my_tiles += 1
            elif curboard[7][7] == another:
                opp_tiles += 1
            c = 25 * (my_tiles - opp_tiles)
            
            l = 0
            my_tiles = opp_tiles = 0
            if curboard[0][0] == 'none':
                if curboard[0][1] == tile: my_tiles += 1
                elif curboard[0][1] == another: opp_tiles += 1
                if curboard[1][1] == tile: my_tiles += 1
                elif curboard[1][1] == another: opp_tiles += 1
                if curboard[1][0] == tile: my_tiles += 1
                elif curboard[1][0] == another: opp_tiles += 1
            if curboard[0][7] == 'none':
                if curboard[0][6] == tile: my_tiles += 1
                elif curboard[0][6] == another: opp_tiles += 1
                if curboard[1][6] == tile: my_tiles += 1
                elif curboard[1][6] == another: opp_tiles += 1
                if curboard[1][7] == tile: my_tiles += 1
                elif curboard[1][7] == another: opp_tiles += 1
            if curboard[7][0] == 'none':
                if curboard[7][1] == tile: my_tiles += 1
                elif curboard[7][1] == another: opp_tiles += 1
                if curboard[6][1] == tile: my_tiles += 1
                elif curboard[6][1] == another: opp_tiles += 1
                if curboard[6][0] == tile: my_tiles += 1
                elif curboard[6][0] == another: opp_tiles += 1
            if curboard[7][7] == 'none':
                if curboard[6][7] == tile: my_tiles += 1
                elif curboard[6][7] == another: opp_tiles += 1
                if curboard[6][6] == tile: my_tiles += 1
                elif curboard[6][6] == another: opp_tiles += 1
                if curboard[7][6] == tile: my_tiles += 1
                elif curboard[7][6] == another: opp_tiles += 1
            l = -12.5 * (my_tiles - opp_tiles)
            
            m = 0                   
            my_tiles = len(self.getValidMoves(curboard, tile))
            opp_tiles = len(self.getValidMoves(curboard, another))
            if my_tiles > opp_tiles:
                m = (100 * my_tiles)/(my_tiles+opp_tiles)
            elif my_tiles < opp_tiles:
                m = -(100 * opp_tiles)/(my_tiles+opp_tiles)
                
            return 10*p + 801.724 * c + 382.026 * l + 78.922 * m + 74.396 * f + 10 * d
            
            
        def minmax(maxdepth, depth, current_board, player_tile, current_tile, moves, alpha, beta):
            #Terminating condition
            if depth == maxdepth:
                return cal_values(current_board, player_tile), moves
            
            if current_tile == player_tile:
                best = -inf
                best_move = []
                possibleMoves = self.getValidMoves(current_board, current_tile)
                if len(possibleMoves) == 0:
                    return cal_values(current_board, player_tile), None
                for i in range(0,len(possibleMoves)):
                    dupeBoard = self.getBoardCopy(current_board)
                    self.makeMove(dupeBoard, current_tile, possibleMoves[i][0], possibleMoves[i][1])
                    next_tile = "white" if current_tile == "black" else "black"
                    val,move = minmax(maxdepth,depth+1, dupeBoard, player_tile, next_tile, possibleMoves[i], alpha, beta)
                    if best <= val:
                        best = val
                        best_move = possibleMoves[i]
                    alpha = max(alpha, best)
                    
                    if beta <= alpha:
                        break
                return best,best_move
            else:
                best = inf
                best_move = []
                possibleMoves = self.getValidMoves(current_board, current_tile)
                if len(possibleMoves) == 0:
                    return cal_values(current_board, player_tile), None
                for i in range(0,len(possibleMoves)):
                    dupeBoard = self.getBoardCopy(current_board)
                    self.makeMove(dupeBoard, current_tile, possibleMoves[i][0], possibleMoves[i][1])
                    next_tile = "white" if current_tile == "black" else "black"
                    val,move = minmax(maxdepth, depth+1, dupeBoard, player_tile, next_tile, possibleMoves[i], alpha, beta)
                    if best > val:
                        best = val
                        best_move = possibleMoves[i]
                    beta = min(beta, best)
                    
                    if beta <= alpha:
                        break
                return best, best_move
        start_time = time.perf_counter()    
        a = minmax(5, 0, self.mainBoard, tile, tile, [], -inf, inf)[1]
        end_time = time.perf_counter()
        if end_time - start_time < 1:
            a = minmax(6, 0, self.mainBoard, tile, tile, [], -inf, inf)[1]
        end_time = time.perf_counter()
        print(end_time - start_time)
        return a
        
    def white_move(self, tile='white'):
        '''
        此处为执白棋的程序需要实现的策略，此处为AI执白
        :param tile: 棋子颜色的字符串，值为“white”或者“black”,在此函数中，默认为白色！
        :return: 返回一个最佳的落子位置[x,y]
        '''
        # return self.get_baseline_move(tile, 1)
        return self.get_AI_move(tile)

    def black_move(self, tile='black'):
        '''
        此处为执黑棋的程序需要实现的策略，此处为随机策略执黑
        :param tile: 棋子颜色的字符串，值为“white”或者“black”,在此函数中，默认为黑色！
        :return: 返回一个最佳的落子位置[x,y]
        '''
        # baseline的策略也可自定义，通过设置get_baseline_move函数的baseline_num进行调用
        return self.get_baseline_move(tile, 2)
        # return self.get_AI_move(tile)

    def program_go(self, playerTile):
        '''
        程序走棋，交叉传入“white”、“black”字符串，交替执行走棋操作
        :param playerTile:当前玩家的棋子颜色
        :return:
        '''
        self.playerTile = playerTile
        self.drawAll()
        self.drawCanGo()
        self.root.update()
        time.sleep(self.sleep_time)
        if playerTile == 'white':
            can_move = self.white_move()
            if can_move is None:
                self.white_no_choose=True
                self.turn = 'black'
                print("program 2 【白棋】 没有走法")
                return
            else:
                self.white_no_choose=False
        elif playerTile == 'black':
            can_move = self.black_move()
            if can_move is None:
                self.black_no_choose=True
                print("program 1 【黑棋】 没有走法")
                self.turn = 'white'
                return
            else:
                self.black_no_choose=False
        x, y = can_move
        self.makeMove(self.mainBoard, playerTile, x, y)
        if self.isGameOver(self.mainBoard):  # 游戏结束，显示双方棋子数量
            self.gameOver=True
            # self.afterGameOver()

    def afterGameOver(self):
        self.drawAll()
        self.root.update()
        self.gameOver = True
        black_score = self.getScoreOfBoard(self.mainBoard)["black"]
        white_score = self.getScoreOfBoard(self.mainBoard)["white"]
        outputStr = self.gameoverStr + "白棋:" + str(white_score) + ":" + "黑棋:" + str(black_score)
        if black_score == white_score:
            outputStr += ", 【平 局】"
        elif black_score > white_score:
            outputStr += ", 【黑棋胜】"
        else:
            outputStr += ", 【白棋胜】"
        print(outputStr)
        showinfo(title="游戏结束", message=outputStr)

    def whoGoesFirst(self, mode=0):
        '''
        决定谁先走的函数，在人机对战模式下，mode==0，不建议修改！！
        因为机器对战不涉及谁先手的问题
        :param mode:0是人机对战，1是机器对战
        :return:先手的角色
        '''
        if mode == 0:
            if random.randint(0, 1) == 0:
                return 'computer'
            else:
                return 'player'
        else:
            return 'black'

    # GUI 界面启动
    def start(self, mode=0):
        '''
        GUI 界面启动函数
        黑白棋的规则是执黑先行！
        :param mode: 对战模式，默认为人机对战模式0，如果需要程序对战，请设置mode=1
        :return:
        '''
        self.resetBoard()
        if mode == 0:
            self.turn = self.whoGoesFirst()
            showinfo(title="游戏开始提示", message=self.turn + "先走!")
            print(self.turn, "先走!")

            if self.turn == 'player':
                self.playerTile = 'black'
                self.computerTile = 'white'
            else:
                self.playerTile = 'white'
                self.computerTile = 'black'
                self.computerGo()
            # 设置窗口
            self.cv = Canvas(self.root, bg='green', width=720, height=720)
            # 重画所有的棋子和棋盘
            self.drawAll()
            self.drawCanGo()
            self.cv.bind("<Button-1>", self.callback)
            self.root.update()
        elif mode == 1:
            for i in range(40):
                if not self.isGameOver(self.mainBoard):
                    self.program_go("black")
                    self.program_go("white")
                else:
                    self.afterGameOver()
                    break
        else:
            print("mode 参数有误！")
            return
        self.cv.pack()
        self.root.mainloop()


if __name__ == '__main__':
    # mode=0 是人机对战模式、mode=1是机器对战模式
    OthelloGUI().start(mode=1)
