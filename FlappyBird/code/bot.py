import pyglet
import random
import pickle
import atexit
import os
import math
import json
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
        # train or run
        self.train = True
        # variables for plan
        self.Q = {}
        self.alpha = 0.7
        self.discount_factor = 0.95
        self.reward = {0:1,1:-1000}
        # replay
        self.moves = []
        # alpha decay parameter
        self.alpha_decay = 0.00003
        
        #根据score更新
        self.current_score = 0
        self.current_round = 0
        #state record
        self.previous_action = 0
        self.previous_state = '0_0_0_0_0'
        #load files
        if os.path.isfile('dict_Q'):
            self.Q = pickle.load(open('dict_Q', 'rb'))
        #self.load_training_states()
        
        def do_at_exit():
            pickle.dump(self.Q, open('dict_Q', 'wb'))
            print('wirte to dict_Q')

        atexit.register(do_at_exit)

    
    def init_qvalues(self, state):
        if self.Q.get(state) is None:
            self.Q[state] = [0,0,0]
            
    '''
    def load_training_states(self):
        if self.train:
            try:
                with open("training_values_resume.json",'r') as f:
                    training_state = json.load(f)
                    self.round = training_state['episode'][-1]
                    self.scores = training_state['scores']
                    self.alpha = max(self.alpha - self.alpha_dacay * self.round, 0.1)
            except IOError:
                pass
    '''
    
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
            if self.train:
                self.update_qvalues()
            # restart game
            self.round += 1
            print('score:', self.game.record.get(), 'best: ', self.game.record.best_score,'round: ', self.round)
            if self.round % 2000 == 0 and self.round != 0:
                pickle.dump(self.Q, open('dict_Q', 'wb'))
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
        _state = self.get_Qstate(state, self.previous_action)
        if self.train:
            self.moves.append((self.previous_state,self.previous_action,_state))
            # replay
            self.reduce_moves()
            self.previous_state = _state
        
        if self.Q[_state][0] > self.Q[_state][1]:
            self.previous_action = 0
            return
        elif self.Q[_state][0] < self.Q[_state][1]:
            self.previous_action = 1
            self.tap()
            return
        else:
            y0 = int(_state.split('_')[1])
            self.previous_action = 1 if random.randint(0,100) < 100*(1/(1+math.exp(y0))) else 0
            if self.previous_action == 1:
                self.tap()
            # print("never met!")
            return

    def update_qvalues(self):
        if self.train:
            history = list(reversed(self.moves))
            high_death_flag = True if history[0][2].split("_")[-1] == 1 else False
            t, last_flap = 0, True
            for move in history:
                t += 1
                state, action, new_state = move
                self.Q[state][2] += 1
                curr_reward = self.reward[0]
                
                if t <= 2:
                    curr_reward = self.reward[1]
                    if action:
                        last_flap = False
                elif (last_flap or high_death_flag) and action:
                    curr_reward = self.reward[1]
                    last_flap = False
                    high_death_flag = False
                sample = (curr_reward + self.discount_factor * max(self.Q[new_state][0:2]))
                self.Q[state][action] = (1-self.alpha) * (self.Q[state][action]) + self.alpha * sample
            if self.alpha > 0.1:
                self.alpha = max(self.alpha - self.alpha_decay, 0.1)
            self.moves = []
    
    def end_epsode(self):
        if self.train:
            history = list(reversed(self.moves))
            for move in history:
                state, action, new_state = move
                self.Q[state][action] = (1 - self.alpha) * (self.Q[state][action]) + \
                                        self.alpha * (self.reward[0] + self.discount_factor *
                                                      max(self.Q[new_state][0:2]))
            self.moves = []

    def reduce_moves(self, reduce_len=100000):
        if len(self.moves) > reduce_len:
            # print("OUT OF RANGE!")
            history = list(reversed(self.moves[:reduce_len]))
            for move in history:
                state, action, new_state = move
                self.Q[state][action] = (1 - self.alpha) * (self.Q[state][action]) + \
                                        self.alpha * (self.reward[0] + self.discount_factor *
                                                      max(self.Q[new_state][0:2]))
            self.moves = self.moves[reduce_len:]


    def get_Qstate(self, state, pre_a):
        bird = state['bird']
        pipes = state['pipes']
        if len(pipes) == 0:
            _state = '0_0_{}_0_0'.format(pre_a)
            self.init_qvalues(_state)
            return _state

        if pipes[0][0] + 52 + 26 > bird[0]:
            pipe0, pipe1 = pipes[0], pipes[1]
        else:
            pipe0, pipe1 = pipes[2], pipes[3]
            
        x0 = pipe0[0] - bird[0] + 52 + 26
        y0 = bird[1] - pipe1[1]
        y1 = bird[1] - pipe0[1]
        
        if x0 < 40:
            x0 = int(x0)
        elif x0 < 180:
            x0 = int(x0) - (int(x0) % 10)
        else:
            x0 = int(x0) - (int(x0) % 90)
        
        if -180 < y0 < 180:
            y0 = int(y0) - (int(y0) % 10)
        else:
            y0 = int(y0) - (int(y0) % 60)
        
        if -180 < y1 < 180:
            y1 = int(y1) - (int(y1) % 10)
        else:
            y1 = int(y1) - (int(y1) % 60)
        
        death_flag = 1 if bird[2] == 'dead' else 0
        
        _state = str(int(x0)) + "_" + str(int(y0)) + "_" + str(int(pre_a)) + "_" + str(int(y1)) + "_" + str(int(death_flag))
        
        self.init_qvalues(_state)
        return _state

if __name__ == '__main__':
    show_window = True
    enable_sound = False
    game = Game()
    game.set_sound(enable_sound)
    bot = Bot(game)


    def update(dt):
        game.update(dt)
        bot.run()


    # pyglet.clock.schedule_interval(update, Game.TIME_INTERVAL)
    pyglet.clock.schedule_interval(update, 0.0001)
    if show_window:
        window = pyglet.window.Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT, vsync=False)


        @window.event
        def on_draw():
            window.clear()
            game.draw()


        pyglet.app.run()
    else:
        pyglet.app.run()

