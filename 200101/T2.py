from T1 import Clock
import turtle as tu
import time


class V_Clock(Clock):
    size = 100
    pos = ()
    color_tick = 'black'
    color_dial = 'yellow'
    color_pointer = 'black'

    def __init__(self, pos=(0, 0), size=100,
                 color=['black', 'yellow', 'black']):
        self.pos = pos
        self.size = size
        self.color_tick = color[0]
        self.color_dial = color[1]
        self.color_pointer = color[2]
        self.H_hand = size/2
        self.M_hand = size*5/8
        self.S_hand = size*6/8

    def set_time(self, H, M, S):
        Clock.__init__(self, H, M, S)

    def draw_dial(self):
        # 画表盘
        pos_Hb = []
        pos_Hs = []
        pos_S = []
        tu.pensize(2)
        tu.speed(0)
        tu.penup()
        tu.setpos(0+self.pos[0], self.size+self.pos[1])
        tu.setheading(0)
        tu.pendown()
        tu.pencolor(self.color_tick)
        tu.fillcolor(self.color_dial)
        tu.begin_fill()
        for i in range(60):
            now_pos = tu.pos()
            if i % 15 == 0:
                pos_Hb.append(now_pos)
            elif i % 5 == 0:
                pos_Hs.append(now_pos)
            else:
                pos_S.append(now_pos)
            tu.circle((-1)*self.size, (360/60))
        tu.end_fill()
        ############################################
        tu.penup()
        tu.setpos(self.pos)
        tu.pencolor(self.color_tick)
        tu.pendown()
        for i in range(len(pos_S)):
            # 现画秒刻度
            tu.setpos(pos_S[i])
            tu.setpos(self.pos)
        tu.penup()
        tu.setpos(0+self.pos[0], self.size-15+self.pos[1])
        tu.setheading(0)
        tu.pendown()
        # 填充一次，去掉多余的秒刻度线
        tu.pencolor(self.color_dial)
        tu.begin_fill()
        tu.circle((15-self.size))
        tu.end_fill()
        ############################################
        tu.penup()
        tu.setpos(self.pos)
        tu.pencolor(self.color_tick)
        tu.pendown()
        for i in range(len(pos_Hs)):
            # 现画次长刻度
            tu.setpos(pos_Hs[i])
            tu.setpos(self.pos)
        tu.penup()
        tu.setpos(0+self.pos[0], self.size-25+self.pos[1])
        tu.setheading(0)
        tu.pendown()
        # 填充一次，去掉多余的线
        tu.pencolor(self.color_dial)
        tu.begin_fill()
        tu.circle((25-self.size))
        tu.end_fill()
        ############################################
        tu.penup()
        tu.setpos(self.pos)
        tu.pencolor(self.color_tick)
        tu.pendown()
        for i in range(len(pos_Hb)):
            # 现画最长刻度
            tu.setpos(pos_Hb[i])
            tu.setpos(self.pos)
        tu.penup()
        tu.setpos(0+self.pos[0], self.size-30+self.pos[1])
        tu.setheading(0)
        tu.pendown()
        # 填充一次，去掉多余的线
        tu.pencolor(self.color_dial)
        tu.begin_fill()
        tu.circle((30-self.size))
        tu.end_fill()
        ############################################
        tu.penup()
        # tu.mainloop()

    def draw_pointer(self):
        tu.hideturtle()
        S_pos = 90-self.seconds*6
        M_pos = 90-self.minutes*6-self.seconds/10
        H_pos = 90-(self.hour % 12)*(360/12)-self.minutes*(360/12)/60
        # 先画秒针
        tu.penup()
        tu.setpos(self.pos)
        tu.pensize(2)
        tu.pencolor(self.color_pointer)
        tu.setheading(S_pos)
        tu.pendown()
        tu.forward(self.S_hand)
        # 再画分针
        tu.penup()
        tu.setpos(self.pos)
        tu.pensize(3)
        tu.pencolor(self.color_pointer)
        tu.setheading(M_pos)
        tu.pendown()
        tu.forward(self.M_hand)
        # 最后画时针
        tu.penup()
        tu.setpos(self.pos)
        tu.pensize(4)
        tu.pencolor(self.color_pointer)
        tu.setheading(H_pos)
        tu.pendown()
        tu.forward(self.H_hand)
        ################################
        tu.penup()
        # tu.mainloop()

    def clear_pointer(self):
        tu.hideturtle()
        tu.penup()
        tu.pencolor(self.color_dial)
        tu.fillcolor(self.color_dial)
        tu.setpos(self.pos[0], self.pos[1]+self.S_hand+2)
        tu.setheading(0)
        tu.begin_fill()
        tu.circle(-1*(self.S_hand+2))
        tu.end_fill()


def test():
    clock1 = V_Clock((-100, 100), 200, ['black', 'pink', 'black'])
    T = time.localtime()
    clock1.set_time(T.tm_hour, T.tm_min, T.tm_sec)
    clock1.draw_dial()
    clock1.draw_pointer()
    i = 0
    while i <= 120:
        i += 1
        time.sleep(0.1)
        T = time.localtime()
        clock1.set_time(T.tm_hour, T.tm_min, T.tm_sec)
        # clock1.show()
        clock1.clear_pointer()
        clock1.draw_pointer()
    tu.mainloop()


if __name__ == '__main__':
    test()
