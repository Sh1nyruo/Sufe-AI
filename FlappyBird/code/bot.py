import pyglet
import random
import pickle
import atexit
import os
from pybird.game import Game


class Bot:
    def __init__(self, game):
        self.game = game
        # constants
        self.WINDOW_HEIGHT = Game.WINDOW_HEIGHT
        self.PIPE_WIDTH = Game.PIPE_WIDTH
        # this flag is used to make sure at most one tap during
        # every call of run()
        self.tapped = False
        self.round = 0
        self.game.play()

        # variables for plan
        self.Q = {}
        self.alpha = 0.7
        self.explore = 0
        self.pre_s = (9999, 9999)
        self.pre_a = 'do_nothing'

        if os.path.isfile('dict_Q'):
            self.Q = pickle.load(open('dict_Q', 'rb'))

        def do_at_exit():
            pickle.dump(self.Q, open('dict_Q', 'wb'))
            print('wirte to dict_Q')

        atexit.register(do_at_exit)

    # this method is auto called every 0.05s by the pyglet
    def run(self):

        if self.game.state == 'PLAY':
            self.tapped = False
            # call plan() to execute your plan
            self.plan(self.get_state())
        else:
            state = self.get_state()
            bird_state = list(state['bird'])
            bird_state[2] = 'dead'
            state['bird'] = bird_state
            # do NOT allow tap
            self.tapped = True
            self.plan(state)
            # restart game
            self.round += 1
            print('score:', self.game.record.get(), 'best: ', self.game.record.best_score,'round: ', self.round)
            self.game.restart()
            self.game.play()

    # get the state that robot needed
    def get_state(self):
        state = {}
        # bird's position and status(dead or alive)
        state['bird'] = (int(round(self.game.bird.x)), \
                         int(round(self.game.bird.y)), 'alive')
        state['pipes'] = []
        # pipes' position
        for i in range(1, len(self.game.pipes), 2):
            p = self.game.pipes[i]
            if p.x < Game.WINDOW_WIDTH:
                # this pair of pipes shows on screen
                x = int(round(p.x))
                y = int(round(p.y))
                state['pipes'].append((x, y))
                state['pipes'].append((x, y - Game.PIPE_HEIGHT_INTERVAL))
        return state

    # simulate the click action, bird will fly higher when tapped
    # It can be called only once every time slice(every execution cycle of plan())
    def tap(self):
        if not self.tapped:
            self.game.bird.jump()
            self.tapped = True

    # That's where the robot actually works
    # NOTE Put your code here
    def plan(self, state):
        if random.random() < 0.1:
            self.tap()


if __name__ == '__main__':
    show_window = True
    enable_sound = False
    game = Game()
    game.set_sound(enable_sound)
    bot = Bot(game)


    def update(dt):
        game.update(dt)
        bot.run()


    pyglet.clock.schedule_interval(update, Game.TIME_INTERVAL)

    if show_window:
        window = pyglet.window.Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT, vsync=False)


        @window.event
        def on_draw():
            window.clear()
            game.draw()


        pyglet.app.run()
    else:
        pyglet.app.run()

