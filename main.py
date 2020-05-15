import pyxel


class PrettyHopper:
    """ ゲームのメインクラス """
    def __init__(self):
        """ 初期化 """
        pyxel.init(160, 120, caption='pretty hopper')
        # プレイヤー初期化
        self.player = Player()
        pyxel.load(self.player.rect)
        pyxel.run(self.update, self.draw)

    def update(self):
        """ 画面のコントロール """
        # qが押されたらゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """ 画面描画 """
        # 背景
        pyxel.cls(7)
        # プレイヤー描画
        pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 7)


class Player:
    """ プレイヤーのコントロール """
    def __init__(self):
        self.rect = 'image/player.pyxres'
        self.position = [100, 100]


PrettyHopper()
