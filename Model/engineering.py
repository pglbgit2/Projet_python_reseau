import sys
sys.path.insert(0, '..')
from Model import batiment as b


class EngineersPost(b.Batiment):
    def __init__(self, posx, posy, username=b.t.myName):
        b.Batiment.__init__(self, 1, 81, posx, posy, 30, 0, 1, 1, 1, 5, username)
        self.name = "EngineersPost"
        self.texture = "engineer"
