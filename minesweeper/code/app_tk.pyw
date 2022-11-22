from __future__ import unicode_literals
import webbrowser

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from tkinter import messagebox
except ImportError:
    import tkMessageBox as messagebox

from core import Game
from helpers import GameHelpers
from helpers import level_config
import widgets
import static
import random


class App(tk.Frame):
    def __init__(self, is_AI, map_path):
        tk.Frame.__init__(self)
        self.is_AI = is_AI
        self.map_frame = None
        mine_map = level_config.map(map_path)
        self._create_map_frame(mine_map, is_AI)
        self.create_top_menu()

    def create_top_menu(self):
        top = self.winfo_toplevel()
        menu_bar = tk.Menu(top)
        top['menu'] = menu_bar

        game_menu = tk.Menu(menu_bar)
        game_menu.add_command(label='开始', command=self.map_frame.start)
        game_menu.add_command(label='重置', command=self.map_frame.reset)
        game_menu.add_separator()
        game_menu.add_command(label='退出', command=self.exit_app)
        menu_bar.add_cascade(label='游戏', menu=game_menu)

        map_menu = tk.Menu(menu_bar)
        self.level = tk.StringVar()
        self.level.set('secondary')
        for level, label in level_config.choices:
            map_menu.add_radiobutton(label=label,
                                     variable=self.level,
                                     value=level,
                                     command=self.select_map_level)
        map_menu.add_separator()
        map_menu.add_command(label='自定义...', command=self.create_custom_map)
        menu_bar.add_cascade(label='地图', menu=map_menu)

        about_menu = tk.Menu(menu_bar)
        about_menu.add_command(label='主页', command=lambda: webbrowser.open_new_tab(static.HOME_URL))
        about_menu.add_command(label='关于...', command=self.show_about_info)
        menu_bar.add_cascade(label='关于', menu=about_menu)

    def select_map_level(self):
        level = self.level.get()
        mine_map = level_config.map(level)
        self._create_map_frame(mine_map, self.is_AI)

    def _create_map_frame(self, mine_map, is_AI):
        if self.map_frame:
            self.map_frame.pack_forget()
        self.map_frame = GameFrame(mine_map, is_AI)
        self.map_frame.pack(side=tk.TOP)

    def create_custom_map(self):
        params = {
            'width': self.map_frame.game.width,
            'height': self.map_frame.game.height,
            'mine_number': self.map_frame.game.mine_number
        }
        return widgets.MapParamsInputDialog(self, callback=App.get_map_params, initial=params)

    def get_map_params(self, params_dict):
        new_map = GameHelpers.create_from_mine_number(**params_dict)
        self._create_map_frame(new_map, self.is_AI)

    def exit_app(self):
        self.quit()

    def show_about_info(self):
        widgets.view_file(self, '关于', static.static_file('project.txt'))


class GameFrame(tk.Frame):
    def __init__(self, mine_map, is_AI):
        tk.Frame.__init__(self)
        self.map = mine_map
        self.is_AI = is_AI
        self._create_controller_frame()
        self.map_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.map_frame.pack(side=tk.TOP, expand=tk.YES, padx=10, pady=10)
        self.game = Game(mine_map)
        height, width = mine_map.height, mine_map.width
        self.bt_map = [[None for _ in range(0, width)] for _ in range(0, height)]
        for x in range(0, height):
            for y in range(0, width):
                if not self.is_AI:
                    self.bt_map[x][y] = tk.Button(self.map_frame, text='', width=3, height=1,
                                                  command=lambda px=x, py=y: self.sweep_mine(px, py))
                else:
                    self.bt_map[x][y] = tk.Button(self.map_frame, text='', width=3, height=1)
                self.bt_map[x][y].config(static.style('grid.unknown'))

                def _mark_mine(event, self=self, x=x, y=y):
                    return self.mark_grid_as_mine(event, x, y)

                self.bt_map[x][y].bind('<Button-3>', _mark_mine)
                self.bt_map[x][y].grid(row=x, column=y)
        self._create_info_frame()

    def _create_controller_frame(self):
        self.controller_bar = tk.LabelFrame(self, text='控制', padx=5, pady=5)
        self.controller_bar.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=2)
        self.start_bt = tk.Button(self.controller_bar, text='开始', relief=tk.GROOVE, command=self.start)
        self.start_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.reset_bt = tk.Button(self.controller_bar, text='重置', relief=tk.GROOVE, command=self.reset)
        self.reset_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.map_info_bt = tk.Button(self.controller_bar, text='查看', relief=tk.GROOVE, command=self._show_map_info)
        self.map_info_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)

    def _show_map_info(self):
        map_info_str = '当前地图大小：%d X %d\n地雷数目：%d' % (self.game.height, self.game.width, self.game.mine_number)
        messagebox.showinfo('当前地图', map_info_str, parent=self)

    def _create_info_frame(self):
        self.info_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.info_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=5)
        self.step_text_label = tk.Label(self.info_frame, text='步数')
        self.step_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.step_count_label = widgets.CounterLabel(self.info_frame, init_value=0, step=1)
        self.step_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.timer_text_label = tk.Label(self.info_frame, text='时间')
        self.timer_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.timer_count_label = widgets.TimerLabel(self.info_frame)
        self.timer_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_text_label = tk.Label(self.info_frame, text='标记')
        self.flag_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_count_label = widgets.CounterLabel(self.info_frame, init_value=0, step=1)
        self.flag_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.msg_label = widgets.MessageLabel(self.info_frame)
        self.msg_label.pack(side=tk.RIGHT)

    def start(self):
        self._draw_map()
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.timer_count_label.reset()
        self.msg_label.splash('新游戏已就绪')
        if self.is_AI:
            self.run_AI()

    def reset(self):
        self.game.reset()
        self._draw_map()
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.timer_count_label.reset()
        self.msg_label.splash('游戏已经重置')

    def sweep_mine(self, x, y, lighter=False):
        if self.game.swept_state_map[x][y]:
            if not lighter:
                return Game.STATE_PLAY
                # return
        if not self.timer_count_label.state:
            self.timer_count_label.start_timer()
        state = self.game.play((x, y), lighter)
        self.step_count_label.set_counter_value(str(self.game.cur_step))
        # self._draw_map()
        if state == Game.STATE_SUCCESS:
            self.timer_count_label.stop_timer()
            self.msg_label.splash('恭喜你，游戏通关了')
        elif state == Game.STATE_FAIL:
            self.timer_count_label.stop_timer()
            self.msg_label.splash('很遗憾，游戏失败')
        return state

    def mark_grid_as_mine(self, event, x, y):
        if self.game.state == Game.STATE_PLAY and not self.game.swept_state_map[x][y]:
            cur_text = self.bt_map[x][y]['text']
            if cur_text == '?':
                cur_text = ''
                self.flag_count_label.decrease()
            elif cur_text == '':
                cur_text = '?'
                self.flag_count_label.increase()
            self.bt_map[x][y]['text'] = cur_text

    def _draw_map(self):
        for i in range(0, self.game.height):
            for j in range(0, self.game.width):
                if self.game.swept_state_map[i][j]:
                    if self.game.mine_map.is_mine((i, j)):
                        self.bt_map[i][j].config(static.style('grid.mine'))
                    elif self.game.mine_map.is_double_mine((i, j)):
                        self.bt_map[i][j].config(static.style('grid.double_mine'))
                    else:
                        tmp = self.game.mine_map.distribute_map[i][j]
                        self.bt_map[i][j].config(static.style('grid.swept', num=tmp))
                else:
                    if self.bt_map[i][j]['text'] == '?':
                        self.bt_map[i][j].config(static.style('grid.marked'))
                    else:
                        self.bt_map[i][j].config(static.style('grid.unknown'))

    def run_AI(self):
        """
        这里是大家写AI的地方哦！！！
        1. AI的第一步固定是中心点(10,15)，测试地图中不会出现第一步踩雷的情况！
        2. 只能使用self.game.visible_map，作为AI看得见的地图部分
        3. 地图中的元素(括号里是对应数组中的值)：
            Invisible(-999)：不可见区块，AI可以选择探索，探索后区块变为可见
            Mine(-1)：雷，踩到后扣1分！但还是可以继续游戏。
            Double_Mine(-2)：双响雷，踩到后扣10分！
            Triple_Mine(-3): 三响雷，踩到后扣10分！
            Space(0)：空白格，什么都没有发生
            Number(x)：周围有x颗雷。注意双响雷会被计算两次、三响雷会被计算三次，所以请一定小心。
        4. 当除了雷以外的单元格均被探索，游戏结束！
        5. 为降低难度，可以使用灯塔道具查看已探索点的周围情况，但该道具使用次数受限！
        """
        if self.is_AI:
            light_count = 1  # 目前可以使用的灯塔数量
            use_lighter = False
            state = self.game.state
            first = True
            while state == Game.STATE_PLAY:
                x, y = 10, 15
                # 在区块内填写逻辑，让你的AI选择要探索的区块(x, y)
                ###################################
                #     这里只是一个随机选择的版本    #
                if first:
                    first = False
                    state = self.sweep_mine(x, y, lighter=False)
                    print('(%d, %d)' % (x, y))
                    continue
                else:
                    while self.game.visible_map[x][y] != -999:
                        x, y = random.randint(0, 19), random.randint(0, 29)

                ###################################

                # 探索区块(x, y), 使用lighter时令use_lighter = True, 注意: 使用灯塔道具的次数有限！
                lighter = use_lighter if light_count > 0 else False
                if lighter:
                    light_count -= 1
                state = self.sweep_mine(x, y, lighter=lighter)

                # 输出每一步的选择
                print('(%d, %d)' % (x, y))

            # 输出当前的分数
            print(self.game.score)


def main():
    """
    添加选择
    当AI_or_General_Choice为0时，使用鼠标点击，即正常扫雷；
    当AI_or_General_Choice为1时，使用AI算法进行扫雷
    """
    score_list = []
    AI_or_General_Choice = 1
    for i in range(1):
        map_path = './map_data/npz/array_map{}.npz'.format(str(i + 1))
        app = App(AI_or_General_Choice, map_path)
        app.map_frame.start()
        if not AI_or_General_Choice:
            app.mainloop()
        score = app.map_frame.game.score
        score_list.append(score)
    print(score_list)


if __name__ == '__main__':
    main()
