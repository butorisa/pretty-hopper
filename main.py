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
        self.score = 0
        self.player = Player()
        self.office = Office()
        self.skill = self.create_skill()
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
            self.player.active = self.switch_active(*self.player.position, *self.office.position, True)
            if not self.player.active:
                # ロード画面
                self.game_mode = GameMode.Office
                # フレーム数を保持
                self.start_frame = pyxel.frame_count

        if self.game_mode == GameMode.Office:
            for enum in self.skill:
                for i, v in enumerate(enum.state):
                    enum.state[i] = self.update_object(*v)

    def draw(self):
        """ 画面描画 """
        if self.game_mode == GameMode.Town:
            self.draw_town()
        elif self.game_mode == GameMode.Office:
            # self.draw_loading()
            # # ローディング画面表示終了
            # if (pyxel.frame_count - self.start_frame) > 90:
            self.draw_office()

    def draw_town(self):
        """ 町を描画 """
        # 背景
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 0, 0, 16, 16)
        # オフィス
        pyxel.blt(self.office.position[0], self.office.position[1], 0, 16, 0, 16, 16, 5)
        # startアイコン
        self.draw_start()
        # プレイヤー
        if self.player.active:
            pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 5)

        self.flash_object()


    def draw_office(self):
        """ ゲーム画面を描画 """
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 48, 0, 16, 16)
        pyxel.text(5, 5, str(self.score), 14)
        # オブジェクト
        self.draw_object()
        # プレイヤー
        pyxel.blt(self.player.position[0], self.player.position[1], 0, 0, 0, 16, 16, 5)

    def draw_object(self):
        """ 流れてくるオブジェクトを描画 """
        for enum in self.skill:
                u, v = enum.get_image(enum.name)
                for x, y, is_active in enum.state:
                    if is_active:
                        pyxel.blt(x, y, 0, u, v, 16, 16, 5)

    def draw_start(self):
        """ startアイコン """
        if self.flip:
            u = 16
            v = 16
        else:
            u = 32
            v = 16
        pyxel.blt(self.office.position[0], self.office.position[1] - 16, 0, u, v, 16, 16, 5)

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
        self.flash_object()

    def flash_object(self):
        """ 点滅フラグON/OFF """
        if pyxel.frame_count % 15 == 0:
            self.flip = not self.flip

    def switch_active(self, obj_x, obj_y, target_x, target_y, is_activate):
        """ オブジェクトが重なったら一方を非表示にする """
        if not is_activate:
            return False

        if abs(obj_x - target_x) < 10 and abs(obj_y - target_y) < 10:
            if self.game_mode == GameMode.Town:
                self.player.position = [8, 104]
            elif self.game_mode == GameMode.Office:
                self.score += 10
            return False
        else:
            return True

    def update_object(self, x, y, is_activate):
        """ オブジェクトのアニメーション """
        active = self.switch_active(x, y, self.player.position[0], self.player.position[1], is_activate)

        x -= 2
        # 左端を過ぎたらまた右から流れるようにする
        if x < -40:
            x += 240
            y = randint(0, 104)
            active = True

        return x, y, active

    def create_skill(self):
        """ skillオブジェクト生成 """
        num = len([obj.name for obj in Skill])
        skills = [Skill(i) for i in range(1, num + 1)]
        return skills


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
    """ 会社オブジェクト """
    def __init__(self):
        self.position = [96, 64]


class Skill(Enum):
    """ 画面に流れるオブジェクト """
    Java = auto()
    Python = auto()
    Ruby = auto()

    def __init__(self, num):
        # [x, y, is_active]
        self.state = [(i * 60, randint(0, 104), True) for i in range(4)]

    def get_image(self, enum):
        """ イメージバンクから切り出す座標を返す """
        if enum == 'Java':
            return 32, 80
        elif enum == 'Python':
            return 48, 80
        elif enum == 'Ruby':
            return 0, 96


PrettyHopper()

