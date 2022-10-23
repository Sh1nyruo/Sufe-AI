'''
黑白棋的算法类，将部分不属于GUI的函数分离出来
例如计算翻转棋子列表，当前位置是否是角落，当前位置是否出界
'''
class Othello:
    def __init__(self):
        self._turn=""

    def isOnBoard(self,x, y):
        '''
        判断当前落子位置是否在界内，如果出界，返回False,如果在界内，返回True
        :param x:
        :param y:
        :return:
        '''
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def isValidMove(self,board, tile, xstart, ystart):
        '''
        是否是合法走法，如果合法返回需要翻转的棋子列表，如果不合法，即没有可以翻转的棋子，返回[]
        :param board:传入棋盘的布局，由于是数组结构，是实参，会被改变，
        :param tile:棋子颜色的字符串，值为“white”或者“black”
        :param xstart:目标位置的x，取值为（0-7）
        :param ystart:目标位置的y，取值为（0-7）
        :return:
        '''
        # 如果该位置已经有棋子或者出界了，返回False
        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
            return False
        # 临时将tile 放到指定的位置
        board[xstart][ystart] = tile
        if tile == 'black':
            otherTile = 'white'
        else:
            otherTile = 'black'
        # 要被翻转的棋子
        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                # 一直走到出界或不是对方棋子的位置
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                # 出界了，则没有棋子要翻转OXXXXX
                if not self.isOnBoard(x, y):
                    continue
                # 是自己的棋子OXXXXXXO
                if board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        # 回到了起点则结束
                        if x == xstart and y == ystart:
                            break
                        # 需要翻转的棋子
                        tilesToFlip.append([x, y])
        # 将前面临时放上的棋子去掉，即还原棋盘
        board[xstart][ystart] = 'none'  # restore the empty space
        # 没有要被翻转的棋子，则走法非法。翻转棋的规则。
        if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def isOnCorner(self,x, y):
        '''
        判断棋子是否在角上，因为角上的棋子不可能被再次翻转
        :param x: 棋子x坐标，取（0-7）
        :param y: 棋子y坐标，取（0-7）
        :return:
        '''
        return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)





