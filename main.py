import pyxel
from enum import Enum, auto
from random import randint


class GameMode(Enum):
    """ 画面一覧 """
    Town = auto()
    Office = auto()


class PrettyHopper:
    """ ゲームのメインクラス """
    def __init__(self):
        """ 初期化 """
        pyxel.init(128, 128, caption='pretty hopper')
        pyxel.load('image/pretty-hopper.pyxres')
        self.start_frame = pyxel.frame_count
        self.player = Player()
        self.office = Office()
        # オブジェクト
        self.duke = [(i * 60, randint(0, 104)) for i in range(4)]
        self.python = [(i * 60, randint(0, 104)) for i in range(4)]
        self.ruby = [(i * 60, randint(0, 104)) for i in range(4)]
        # 町からスタート
        self.game_mode = GameMode.Town
        # 画像の点滅表示に使用
        self.flip = False
        pyxel.run(self.update, self.draw)

    def update(self):
        """ 画面のコントロール """
        # qが押されたらゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.player.move()

        if self.game_mode == GameMode.Town:
            self.switch_active(self.player, self.office)

        if self.game_mode == GameMode.Office:
            for i, v in enumerate(self.duke):
                self.duke[i] = self.update_object(*v)
            for i, v in enumerate(self.python):
                self.python[i] = self.update_object(*v)
            for i, v in enumerate(self.ruby):
                self.ruby[i] = self.update_object(*v)

    def draw(self):
        """ 画面描画 """
        if self.game_mode == GameMode.Town:
            self.draw_town()
        elif self.game_mode == GameMode.Office:
            self.draw_loading()
            # ローディング画面表示終了
            if (pyxel.frame_count - self.start_frame) > 90:
                self.draw_office()

    def draw_town(self):
        """ 町を描画 """
        # 背景
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 0, 0, 16, 16)
        # オフィス
        pyxel.blt(self.office.position[0], self.office.position[1], 0, 16, 0, 16, 16, 5)
        # プレイヤー
        if self.player.active:
            pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 5)

    def draw_office(self):
        """ ゲーム画面を描画 """
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 48, 0, 16, 16)

        # オブジェクト
        for x, y in self.duke:
            pyxel.blt(x, y, 0, 32, 80, 16, 16, 5)
        for x, y in self.python:
            pyxel.blt(x, y, 0, 48, 80, 16, 16, 5)
        for x, y in self.ruby:
            pyxel.blt(x, y, 0, 0, 96, 16, 16, 5)
        # プレイヤー
        pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 5)

    def draw_loading(self):
        """ ロード画面を描画 """
        # ウサギがジャンプする画像を表示
        if self.flip:
            tm_x = 32
            tm_y = 0
        else:
            tm_x = 16
            tm_y = 0

        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, tm_x, tm_y, 16, 16)

        if pyxel.frame_count % 15 == 0:
            self.flip = not self.flip

    def switch_active(self, obj, target):
        """ オブジェクトが重なったら一方を非表示にする """
        if abs(obj.position[0] - target.position[0]) < 10\
                and abs(obj.position[1] - target.position[1]) < 10:
            obj.active = False
            # ロード画面
            self.game_mode = GameMode.Office
            # フレーム数を保持
            self.start_frame = pyxel.frame_count
        # else:
        #     obj.active = True
        #     # ゲーム画面
        #     self.game_mode = GameMode.Town

    def update_object(self, x, y):
        """ オブジェクトのアニメーション """
        if abs(x - self.player.position[0]) < 12 and abs(y - self.player.position[1]) < 12:
            # is_active = False
            # self.score += 100
            # self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 104)
            # is_active = True

        return (x, y)


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


class Office:
    """ 家オブジェクト """
    def __init__(self):
        self.position = [96, 64]


PrettyHopper()
