import pyxel


class PrettyHopper:
    """ ゲームのメインクラス """
    def __init__(self):
        pyxel.init(160, 120, caption='pretty hopper')
        pyxel.load('image/player.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # qが押されたらゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(75, 45, 0, 0, 0, 100, 100, 5)


PrettyHopper()