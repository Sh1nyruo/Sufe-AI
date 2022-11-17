# coding=utf8
"""
This module contains some hard-coding data for level map.
"""
from __future__ import unicode_literals
import random
from collections import OrderedDict

from core import Map
import numpy as np


class GameHelpers(object):
    @staticmethod
    def create_from_mine_index_list(height, width, mine_index_list, double_mine_number, triple_mine_number):
        return Map(height, width, ((index // width, index % width) for index in mine_index_list), double_mine_number, triple_mine_number)

    @staticmethod
    def create_from_mine_number(height, width, mine_number, double_mine_number, triple_mine_number):
        map_size = height * width
        mine_index_list = random.sample(range(0, map_size), mine_number + double_mine_number + triple_mine_number)
        return GameHelpers.create_from_mine_index_list(height, width, mine_index_list, double_mine_number, triple_mine_number)

    @staticmethod
    def create_from_read_array(filename):
        read_mine_map = np.load(filename)
        double_mine_number = 0
        triple_mine_number = 0
        mine_map = read_mine_map['arr_0'].tolist()
        height = len(mine_map)
        width = len(mine_map[0])
        mine_index_list = []
        for x in range(height):
            for y in range(width):
                if mine_map[x][y] == -1 or mine_map[x][y] == -2 or mine_map[x][y] == -3:
                    if mine_map[x][y] == -2:
                        double_mine_number += 1
                    elif mine_map[x][y] == -3:
                        triple_mine_number += 1
                    mine_index_list.append(x * width + y)
        return GameHelpers.create_from_mine_index_list(height, width, mine_index_list, double_mine_number, triple_mine_number)


class LevelMapMeta(object):
    def __init__(self, name, verbose, height, width, mine_number, double_mine_number, triple_mine_number):
        self.name = name
        self.verbose = verbose
        self.height = height
        self.width = width
        self.mine_number = mine_number
        self.double_mine_number = double_mine_number
        self.triple_mine_number = triple_mine_number

    @property
    def description(self):
        return '{0}({1}x{2}-{3}--{4})'.format(self.verbose,
                                              self.height,
                                              self.width,
                                              self.mine_number,
                                              self.double_mine_number,
                                              self.triple_mine_number)


class LevelConfig(object):
    def __init__(self):
        self.data = OrderedDict()

    def add_level_map(self, name, **kwargs):
        kwargs.update({'name': name})
        self.data[name] = LevelMapMeta(**kwargs)

    @property
    def choices(self):
        return [(l.name, l.description) for l in self.data.values()]

    def map(self, name):
        # meta = self.data[name]
        return GameHelpers.create_from_read_array(name)
        # return GameHelpers.create_from_mine_number(meta.height, meta.width, meta.mine_number, meta.double_mine_number)


level_config = LevelConfig()
level_config.add_level_map(name='primary',
                           verbose='初级',
                           height=9,
                           width=9,
                           mine_number=10,
                           double_mine_number=1,
                           triple_mine_number=1)
level_config.add_level_map(name='secondary',
                           verbose='中级',
                           height=20,
                           width=30,
                           mine_number=68,
                           double_mine_number=8,
                           triple_mine_number=4)
level_config.add_level_map(name='tertiary',
                           verbose='高级',
                           height=25,
                           width=40,
                           mine_number=400,
                           double_mine_number=40,
                           triple_mine_number=10)
