import sys
try:
    sys.path.insert(0, '..')
    from Model import Walker as W
except:
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
    import logique.Walker as W

class Priest(W.Walker):
    def __init__(self, x, y, bat):
        W.Walker.__init__(self, x, y, bat)
        self.name = 'Priest'
