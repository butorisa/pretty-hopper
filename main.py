import pyxel
from enum import Enum, auto


class GameMode(Enum):
    """ 画面一覧 """
    # 町
    Town = auto()
    # 家の中
    Home = auto()


class PrettyHopper:
    """ ゲームのメインクラス """
    def __init__(self):
        """ 初期化 """
        pyxel.init(128, 128, caption='pretty hopper')
        # プレイヤー初期化
        self.player = Player()
        # 家初期化
        self.home = MyHome()
        pyxel.load('image/pretty-hopper.pyxres')
        # 町からスタート
        self.game_mode = GameMode.Town
        pyxel.run(self.update, self.draw)

    def update(self):
        """ 画面のコントロール """
        # qが押されたらゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.move()
        self.switch_active(self.player, self.home)

    def draw(self):
        """ 画面描画 """
        if self.game_mode == GameMode.Town:
            self.draw_town()
        elif self.game_mode == GameMode.Home:
            self.draw_home()

    def draw_town(self):
        """ 町を描画 """
        # 背景
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 0, 0, 16, 16)
        # 家
        pyxel.blt(self.home.position[0], self.home.position[1], 0, 16, 0, 16, 16, 5)
        # うさぎ
        pyxel.blt(40, 80, 0, 48, 0, 16, 16, 5)
        # プレイヤー
        if self.player.active:
            pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 5)

    def draw_home(self):
        """ 家の中を描画 """
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 16, 0, 16, 16)

    def switch_active(self, obj, target):
        """ オブジェクトが重なったら一方を非表示にする """
        if abs(obj.position[0] - target.position[0]) < 10\
                and abs(obj.position[1] - target.position[1]) < 10:
            obj.active = False
            # ロード画面
            self.game_mode = GameMode.Home
        else:
            obj.active = True
            # ゲーム画面
            self.game_mode = GameMode.Town


class Player:
    """ プレイヤーのコントロール """
    def __init__(self):
        self.active = True
        self.position = [8, 104]

    def move(self):
        """ プレイヤー移動 """
        if pyxel.btnp(pyxel.KEY_LEFT) and self.position[0] > 0:
            self.position[0] -= 10
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.position[0] < 105:
            self.position[0] += 10
        if pyxel.btnp(pyxel.KEY_UP) and self.position[1] > 10:
            self.position[1] -= 10
        if pyxel.btnp(pyxel.KEY_DOWN) and self.position[1] < 105:
            self.position[1] += 10


class MyHome:
    """ 家オブジェクト """
    def __init__(self):
        self.position = [88, 72]


PrettyHopper()
