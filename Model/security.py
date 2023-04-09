import sys

sys.path.insert(0, '..')
from Model import batiment as b


class Prefecture(b.Batiment):
    def __init__(self, posx, posy, username=b.t.myName):
        b.Batiment.__init__(self, 1, 55, posx, posy, 30, -2, 1, 1, 2, 6, username)
        self.name = "Prefecture"
        self.texture = "security"
