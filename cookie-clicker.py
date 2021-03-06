"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 10.0
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._tnc = 0.0
        self._current_cok = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total cookies allover = " + str(self._tnc) + ", current cookies = " + str(self._current_cok) + ", current_time = " + str(self._current_time) + " and cookies per second = " + str(self._cps)   
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cok
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cok >= cookies:
            return 0.0
        else:
            num_sec = math.ceil((float(cookies) - self._current_cok) / self._cps)
        return num_sec
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        else:
            self._current_time += time
            self._current_cok += (float(self._cps) * time)
            self._tnc += (float(self._cps) * time)
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._current_cok:
            return
        else:
            self._current_cok -= cost
            self._cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._tnc))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info = build_info.clone()
    c_state = ClickerState()
    t_left = False
    while c_state.get_time() <= duration:
        if c_state.get_time() > duration:
            break
        else:
            if strategy(c_state.get_cookies(), c_state.get_cps(), c_state.get_history(), duration - c_state.get_time(), info) == None:
                t_left = True
                break
            else:    
                stg = strategy(c_state.get_cookies(), c_state.get_cps(), c_state.get_history(), duration - c_state.get_time(), info)
                if stg != None:
                    w_time = c_state.time_until(info.get_cost(stg))
                    if w_time + c_state.get_time() > duration:
                        t_left = True
                        break
                    else:
                        t_left = False
                        c_state.wait(w_time)
                        c_state.buy_item(stg, info.get_cost(stg), info.get_cps(stg))
                        info.update_item(stg)                 

    while t_left:
        c_state.wait(duration - c_state.get_time())
        t_left = False
    return c_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    info = build_info.clone()
    cost = float('inf')
    item_1 = ''
    for item in info.build_items():
        if info.get_cost(item) < cost:
            cost = info.get_cost(item)
            item_1 = item
    #print cost, item_1          
    if cookies + (cps * time_left) >= cost:
        return item_1
    else:
        return None
          
    
#strategy_cheap(0, 0, 0, 0, provided.BuildInfo())
def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    info = build_info.clone()
    cost = float('-inf')
    item_1 = None
    for item in info.build_items():
        if info.get_cost(item) > cost and (cookies + (cps * time_left) >= info.get_cost(item)):
            cost = info.get_cost(item)
            item_1 = item
    #print cost, item_1          
    if cookies + (cps * time_left) >= cost:
        return item_1
    else:
        return None 
    
#strategy_expensive(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))    
#strategy_expensive(1.0, 3.0, [(0.0, None, 0.0, 0.0)], 17.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))    
#strategy_expensive(0, 0, 0, 0, provided.BuildInfo())

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    info = build_info.clone()
    cost = float('-inf')
    ratio = 0
    item_1 = None
    for item in info.build_items():
        if float(info.get_cps(item)) / info.get_cost(item) > ratio and (cookies + (cps * time_left) >= info.get_cost(item)):
            cost = info.get_cost(item)
            ratio = float(info.get_cps(item)) / cost
            item_1 = item
    #print cost, item_1          
    if cookies + (cps * time_left) >= cost:
        return item_1
    else:
        return None     
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
#print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.1]}, 1.15), 5000.0, strategy_none) 
