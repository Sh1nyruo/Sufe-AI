# coding=utf8
"""
@author:kinegratii(kinegratii@yeah.net)
@Version:1.0.1
Update on 2014.05.04
"""
from __future__ import unicode_literals

import random

try:
    import queue
except ImportError:
    import Queue as queue


class Map(object):
    # the mine flag in distribute map
    MINE_FLAG = -1
    DOUBLE_MINE_FLAG = -2
    TRIPLE_MINE_FLAG = -3

    def __init__(self, height, width, mine_pos_list, double_mine_number, triple_mine_number):
        self._height = height
        self._width = width
        self._mine_number = 0
        self._mine_list = list(set(mine_pos_list))
        self._double_mine_number = double_mine_number
        self._double_mine_index_list = []
        self._triple_mine_number = triple_mine_number
        self._triple_mine_index_list = []
        self._generate_distribute_map()

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def map_size(self):
        return self._height * self._width

    @property
    def mine_list(self):
        return self._mine_list

    @property
    def mine_number(self):
        return len(self._mine_list)

    @property
    def double_mine_number(self):
        return self._double_mine_number

    @property
    def triple_mine_number(self):
        return self._triple_mine_number

    @property
    def distribute_map(self):
        return self._distribute_map

    def _generate_distribute_map(self):
        self._distribute_map = [[0 for _ in range(0, self.width)] for _ in range(0, self.height)]
        offset_step = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        double_mine_index = random.sample(range(0, len(self.mine_list)), self._double_mine_number)
        current_index_list = []
        for i in range(len(self.mine_list)):
            if i not in double_mine_index:
                current_index_list.append(i)
        triple_mine_index = random.sample(current_index_list, self._triple_mine_number)
        self._triple_mine_index_list = triple_mine_index
        self._double_mine_index_list = double_mine_index
        current_index = 0
        for t_x, t_y in self.mine_list:
            if current_index in double_mine_index:
                self._distribute_map[t_x][t_y] = Map.DOUBLE_MINE_FLAG
                for o_x, o_y in offset_step:
                    d_x, d_y = t_x + o_x, t_y + o_y
                    if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != Map.DOUBLE_MINE_FLAG \
                            and self._distribute_map[d_x][d_y] != Map.MINE_FLAG and \
                            self._distribute_map[d_x][d_y] != Map.TRIPLE_MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 2
            elif current_index in triple_mine_index:
                self._distribute_map[t_x][t_y] = Map.TRIPLE_MINE_FLAG
                for o_x, o_y in offset_step:
                    d_x, d_y = t_x + o_x, t_y + o_y
                    if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != Map.MINE_FLAG \
                            and self._distribute_map[d_x][d_y] != Map.DOUBLE_MINE_FLAG and \
                            self._distribute_map[d_x][d_y] != Map.TRIPLE_MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 3
            else:
                self._distribute_map[t_x][t_y] = Map.MINE_FLAG
                for o_x, o_y in offset_step:
                    d_x, d_y = t_x + o_x, t_y + o_y
                    if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != Map.MINE_FLAG \
                            and self._distribute_map[d_x][d_y] != Map.DOUBLE_MINE_FLAG and \
                            self._distribute_map[d_x][d_y] != Map.TRIPLE_MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 1
            current_index += 1
        # print(self._distribute_map)

    def is_in_map(self, pos, offset=None):
        if offset:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        else:
            x, y = pos
        return x in range(0, self.height) and y in range(0, self.width)

    def is_mine(self, pos):
        return pos in self.mine_list

    def get_near_mine_number(self, pos):
        x, y = pos
        return self._distribute_map[x][y]

    def is_double_mine(self, pos):
        double_mine_list = []
        for index in self._double_mine_index_list:
            double_mine_list.append(self._mine_list[index])
        return pos in double_mine_list

    def is_triple_mine(self, pos):
        triple_mine_list = []
        for index in self._triple_mine_index_list:
            triple_mine_list.append(self._mine_list[index])
        return pos in triple_mine_list


class Game(object):
    STATE_PLAY = 1
    STATE_SUCCESS = 2
    STATE_FAIL = 3

    def __init__(self, mine_map):
        self._mine_map = mine_map
        self._init_game()

    def _init_game(self):
        self._score = 10
        self._swept_state_map = [[False for _ in range(0, self._mine_map.width)] for _ in
                                 range(0, self._mine_map.height)]
        self._visible_map = [[-999 for _ in range(0, self._mine_map.width)] for _ in
                              range(0, self._mine_map.height)]

        self._not_swept_number = self._mine_map.map_size
        self._cur_step = 0
        self._sweep_trace = []
        self._state = Game.STATE_PLAY

    def reset(self):
        self._init_game()


    @property
    def cur_step(self):
        return self._cur_step

    @property
    def sweep_trace(self):
        return self._sweep_trace

    @property
    def state(self):
        return self._state

    @property
    def not_swept_number(self):
        return self._not_swept_number

    @property
    def swept_state_map(self):
        return self._swept_state_map

    @property
    def height(self):
        return self._mine_map.height

    @property
    def width(self):
        return self._mine_map.width

    @property
    def mine_number(self):
        return self._mine_map.mine_number

    @property
    def double_mine_number(self):
        return self._mine_map.double_mine_number

    @property
    def triple_mine_number(self):
        return self._mine_map.triple_mine_number

    @property
    def mine_map(self):
        return self._mine_map

    @property
    def visible_map(self):
        return self._visible_map

    @property
    def score(self):
        return self._score

    def _sweep(self, click_pos, lighter):
        if self._state == Game.STATE_SUCCESS or self._state == Game.STATE_FAIL:
            # success or fail is the end state of game.
            return self._state
        self._cur_step += 1
        self._sweep_trace.append(click_pos)
        cx, cy = click_pos
        if self._swept_state_map[cx][cy]:
            # click the position has been clicked,pass
            self._state = Game.STATE_PLAY
            return self._state

        near_mine_number = self._mine_map.get_near_mine_number(click_pos)

        if near_mine_number == Map.MINE_FLAG:
            # click the mine,game over.
            # self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            self._visible_map[cx][cy] = self._mine_map.distribute_map[cx][cy]
            # 踩到雷需要扣分
            if not lighter:
                self._score -= 1
            return self._state

        elif near_mine_number == Map.DOUBLE_MINE_FLAG:
            self._swept_state_map[cx][cy] = True
            self._visible_map[cx][cy] = self._mine_map.distribute_map[cx][cy]
            if not lighter:
                self._score -= 10
            return self._state

        elif near_mine_number == Map.TRIPLE_MINE_FLAG:
            self._swept_state_map[cx][cy] = True
            self._visible_map[cx][cy] = self._mine_map.distribute_map[cx][cy]
            if not lighter:
                self._score -= 10
            return self._state

        elif near_mine_number > 0:
            self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            self._visible_map[cx][cy] = self._mine_map.distribute_map[cx][cy]
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return self._state
        else:
            scan_step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            assert near_mine_number == 0
            q = queue.Queue()
            q.put(click_pos)
            self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            self._visible_map[cx][cy] = self._mine_map.distribute_map[cx][cy]
            while not q.empty():
                c_x, c_y = q.get()
                for o_x, o_y in scan_step:
                    d_x, d_y = c_x + o_x, c_y + o_y
                    if self._mine_map.is_in_map((d_x, d_y)) and not self._swept_state_map[d_x][d_y]:
                        near_mine_number = self._mine_map.get_near_mine_number((d_x, d_y))
                        if near_mine_number == Map.MINE_FLAG:
                            pass
                        elif near_mine_number == Map.DOUBLE_MINE_FLAG:
                            pass
                        elif near_mine_number == Map.TRIPLE_MINE_FLAG:
                            pass
                        elif near_mine_number == 0:
                            q.put((d_x, d_y))
                            self._swept_state_map[d_x][d_y] = True
                            self._visible_map[d_x][d_y] = self._mine_map.distribute_map[d_x][d_y]
                            self._not_swept_number -= 1
                        else:
                            self._swept_state_map[d_x][d_y] = True
                            self._visible_map[d_x][d_y] = self._mine_map.distribute_map[d_x][d_y]
                            self._not_swept_number -= 1
            assert self._not_swept_number >= self._mine_map.mine_number
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return self._state

    def play(self, click_pos, lighter):
        state = None
        if lighter:
            x, y = click_pos
            for near_x in [x - 1, x, x + 1]:
                for near_y in [y - 1, y, y + 1]:
                    if self._mine_map.is_in_map((near_x, near_y)) and self.visible_map[near_x][near_y] == -999:
                        state = self._sweep((near_x,near_y), lighter=True)
        else:
            state = self._sweep(click_pos, lighter=False)
        # 踩到雷了不停止游戏
        if state == Game.STATE_SUCCESS:
            self._sweep_all_map()
        return state

    def _sweep_all_map(self):
        self._swept_state_map = [[True for _ in range(0, self.width)] for _ in range(0, self.height)]
        self._not_swept_number = self.mine_map.map_size - self.mine_map.mine_number
