# 砍柱子
from abc import ABCMeta, abstractclassmethod
from random import random


class fighter(metaclass=ABCMeta):
    '''战士'''
    __slots__ = ('__name',  '__side', '__HP', '__NP',
                 '__ATK', '__DEF', '__CD_fu', '__CD_re', '__alive')

    # 基础属性的初始化
    def __init__(self, name, side, HP, ATK, DEF, CD, NP=0):
        self.__name = name
        self.__side = side
        if side == 'enemy':
            self.__full_HP = HP*5
            self.__current_HP = HP*5
            self.__DEF = DEF*0.8
            self.__ATK = ATK*0.5
        else:
            self.__full_HP = HP
            self.__current_HP = HP
            self.__DEF = DEF*0.8
            self.__ATK = ATK
        self.__CD_fu = CD
        self.__CD_re = [0, 0, 0]
        self.__NP = NP
        self.__alive = True

    # 基础属性(状态)相关的访问与设置
    @property
    def name(self):
        return self.__name

    @property
    def side(self):
        return self.__side

    @property
    def HP(self):
        return self.__current_HP

    @HP.setter
    def HP(self, HP):
        if HP >= 0 and HP <= self.__full_HP:
            self.__current_HP = int(HP)
        else:
            self.__current_HP = 0 if HP < 0 else self.__full_HP

    @property
    def NP(self):
        return self.__NP

    @NP.setter
    def NP(self, NP):
        self.__NP = int(NP if NP >= 0 else 0)

    @property
    def alive(self):
        return self.HP > 0

    '''
    @alive.setter
    def alive(self, state):
        self.__alive = bool(state)
    '''

    @property
    def ATK(self):
        return self.__ATK

    @ATK.setter
    def ATK(self, ATK):
        self.__ATK = int(ATK if ATK >= 0 else 0)

    @property
    def DEF(self):
        return self.__DEF

    @DEF.setter
    def DEF(self, DEF):
        self.__DEF = int(DEF if DEF >= 0 else 0)

    @property
    def CD_fu(self):
        return self.__CD_fu

    @property
    def CD(self):
        return self.__CD_re

    @CD.setter
    def CD(self, skill_CD):
        for i in range(3):
            if skill_CD[i] < 0:
                skill_CD[i] = 0
            if skill_CD[i] > self.__CD_fu[i]:
                skill_CD[i] = self.__CD_fu[i]
        self.__CD_re = skill_CD

    # 动作
    @abstractclassmethod
    def action(self):
        raise NotImplementedError

    # 默认
    def __str__(self):
        mes = '%s\t' % self.name + '%s\t' % self.side + \
            'level: %d\n' % self.level + \
            'HP=%d\t' % self.HP + 'NP=%d\t' % self.NP + \
            'ATK=%d\t' % self.ATK + 'DEF=%d\n' % self.DEF + \
            'CD: %d %d %d\t' % (self.CD[0], self.CD[1], self.CD[2]) + \
            'Alive: %s\n' % self.alive
        return mes


class Tamamo(fighter):
    # 玉藻前

    # 基础属性初始化
    def __init__(self, side, level):
        self.__base_HP = 2091
        self.__base_ATK = 1629
        # self.__level = level if (level > 0 and level <= 100) else 90
        self.__level = level if level > 0 else 90
        self.__full_HP = int(self.__base_HP+self.__level*135.3)
        self.__full_ATK = int(self.__base_ATK+self.__level*99.15)
        self.__full_DEF = int(self.__full_HP*0.2)
        self.__CD_fu = [5, 6, 5]    # 总CD
        fighter.__init__(self, '玉藻前', side, self.__full_HP, self.__full_ATK,
                         self.__full_DEF, self.__CD_fu)

    # 属性(固有)访问设置
    @property
    def base_HP(self):
        return self.__base_HP

    @property
    def base_ATK(self):
        return self.__base_ATK

    @property
    def level(self):
        return self.__level

    @property
    def full_HP(self):
        return self.__full_HP

    @property
    def full_ATK(self):
        return self.__full_ATK

    @property
    def full_DEF(self):
        return self.__full_DEF

    # 技能
    def skill_1(self, targets):
        # 减NP
        now_CD = self.CD
        # 技能CD中。。。
        if now_CD[0] > 0:
            return '技能CD中'
        else:
            for fighter in targets:
                if fighter.side != self.side:
                    fighter.NP -= 20+0.3*self.level
                    break
            # 重置技能CD
            fu_CD = self.CD_fu
            now_CD[0] = fu_CD[0]
            self.CD = now_CD
            # 技能使用成功
            return 'success'

    def skill_2(self):
        # 加防御
        now_CD = self.CD
        # 技能CD中。。。
        if now_CD[1] > 0:
            return '技能CD中'
        else:
            self.DEF = self.DEF*(1+0.3+0.3*self.level/100)
            # 重置技能CD
            fu_CD = self.CD_fu
            now_CD[1] = fu_CD[1]
            self.CD = now_CD
            # 技能使用成功
            return 'success'

    def skill_3(self, targets):
        # 蓝buff 回血
        now_CD = self.CD
        # 技能CD中。。。
        if now_CD[1] > 0:
            return '技能CD中'
        else:
            for fighter in targets:
                if fighter.side == self.side:
                    fighter.ATK = fighter.ATK*(1+0.3+0.2*self.level/100)
                    fighter.HP = fighter.HP+1000+1500*self.level/100
                    break
            # 重置技能CD
            fu_CD = self.CD_fu
            now_CD[2] = fu_CD[2]
            self.CD = now_CD
            # 技能使用成功
            return 'success'

    def ex_skill(self, targets):
        # 宝具 加NP 回血 减 CD
        # NP 不足
        if self.NP < 100:
            return 'NP不足'
        else:
            # NP清零
            self.NP = 0
            for fighter in targets:
                if fighter.side == self.side:
                    fighter.HP = fighter.HP+2000
                    fighter.NP = fighter.NP+30
                    for i in range(3):
                        now_CD = fighter.CD
                        now_CD[i] -= 1
                        fighter.CD = now_CD
            # 宝具使用成功
            print('%s小玉使用了宝具\n' % self.side)
            return 'success'

    def attack(self, targets):
        # 攻击
        for fighter in targets:
            if fighter.side != self.side and fighter.HP > 0:
                harm = self.ATK * (0.8+0.7*random())-fighter.DEF
                fighter.HP -= harm if harm > 0 else 0
                fighter.NP += 10+10*random()
                self.NP += 10+30*random()
                break

    # 动作
    def action(self, targets):

        Enemy = []
        Allies = []
        for fighter in targets:
            if fighter.alive is True:
                if fighter.side != self.side:
                    Enemy.append(fighter)
                else:
                    Allies.append(fighter)

        if self.alive is True and Enemy != []:
            temp1 = []
            # 考虑敌人的NP
            for fighter in Enemy:
                temp1.append(fighter.NP)
            if max(temp1) >= 30:
                # 若敌人的NP至少为30
                self.skill_1([Enemy[temp1.index(max(temp1))]])
                # 对NP最高的敌人使用1技能

            temp1 = []
            # 考虑友军HP
            for fighter in Allies:
                temp1.append(fighter.HP/fighter.full_HP)
            if min(temp1) <= 0.9:
                # 若友军HP最高为0.9
                self.skill_3([Allies[temp1.index(min(temp1))]])
                # 对HP最底的内位使用3技能

            if self.NP >= 100:
                # 开宝具
                self.ex_skill(Allies)

            self.skill_2()
            # 默认对自己使用二技能
            self.attack(Enemy)
            # 最后一击


def test2():
    ##########################
    # 初始化
    print('#################################################\n')
    a1 = Tamamo('ally', 100)
    a2 = Tamamo('ally', 90)
    a3 = Tamamo('ally', 80)
    print(a1, a2, a3)
    print('- - - - - - - - - - - - - - - - - - - - - - - - -\n')
    em1 = Tamamo('enemy', 100)
    em2 = Tamamo('enemy', 100)
    print(em1, em2)
    print('#################################################\n')
    ###########################
    targets = [a1, a2, a3, em1, em2]
    battle_finish = False
    # 战斗结束的标志
    round_cnt = 1
    while battle_finish is False:
        print('#################################################\n')
        print('\t回合%d' % round_cnt)
        a1.action(targets)
        a2.action(targets)
        a3.action(targets)
        em1.action(targets)
        em2.action(targets)

        # 更新技能CD
        temp1 = []
        for fighter in targets:
            temp1 = fighter.CD
            for i in range(len(temp1)):
                temp1[i] -= 1
            fighter.CD = temp1

        print(a1, a2, a3)
        print('- - - - - - - - - - - - - - - - - - - - - - - - -\n')
        print(em1, em2)
        print('#################################################\n')

        if a1.alive is False and a2.alive is False and a3.alive is False:
            battle_finish = True
            print('战斗失败!\n')
        if em1.alive is False and em2.alive is False:
            battle_finish = True
            print('战斗胜利!\n')
        if round_cnt == 30:
            battle_finish = True

        round_cnt += 1


if __name__ == '__main__':
    a1 = test2()
