# 类测试
# 画n角星
import turtle
import math


class n_pointed_star:
    ''' 基本属性 '''
    # 角数
    points_count = 0
    # 外接圆半径
    radius = 0
    # n边形内角
    in_cor = 0
    # n等分角
    per_cor = 0
    # 顶角
    apex = 0
    # 步长
    step_len = 0

    # 定义构造方法
    def __init__(self, n, r=0, a=0):
        self.points_count = n
        self.in_cor = (n-2)*180/n
        self.per_cor = 360/n
        self.apex = (90-self.per_cor)*2
        if r <= 0:
            if a <= 0:
                r = 100
                a = r*math.sin(self.per_cor*math.pi/180) / \
                    (1+math.sin(self.apex*math.pi/360))
            else:
                r = a*(1+math.sin(self.apex*math.pi/360)) / \
                    math.sin(self.per_cor*math.pi/180)
        else:
            a = r*math.sin(self.per_cor*math.pi/180) / \
                (1+math.sin(self.apex*math.pi/360))
        self.radius = r
        self.step_len = a

    # 定义draw方法
    def draw(self, x, y, color_out='red', color_in='yellow'):
        turtle.penup()
        turtle.color(color_out, color_in)
        turtle.setpos(x, y)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(self.points_count):
            turtle.setheading(i*self.per_cor*(-1))
            turtle.forward(self.step_len)
            turtle.left(self.per_cor)
            turtle.forward(self.step_len)
        turtle.end_fill()
        turtle.mainloop()


# 实例化类
star = n_pointed_star(15, 200)
star.draw(-100, 150, 'yellow', 'yellow')
