import sys

sys.path.insert(0, '..')
from Model import batiment as b


class Path(b.Batiment):
    def __init__(self, x, y, username=b.t.myName):
        b.Batiment.__init__(self, 1, 5, x, y, 4, 0, 0, 0, 0, 0, username)
        self.isOnAquaduct = 0
        self.name = 'Path'
        self.texture = "road8"
