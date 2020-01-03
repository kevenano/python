import turtle
import math


def draw_star(x, y, n, a=0, r=0):
    """画边长为a或外接圆半径为r的n角星"""
    # 内角
    # in_cor = (n-2)*180/n
    # 等分角
    per_cor = 360/n
    # 顶角
    apex = (90-per_cor)*2
    if a == 0:
        if r == 0:
            r = 100
        a = r*math.sin(per_cor*math.pi/180)/(1+math.sin(apex*math.pi/360))
    turtle.penup()
    turtle.color('red', 'yellow')
    turtle.setpos(x, y)
    turtle.pendown()
    turtle.begin_fill()
    for i in range(n):
        turtle.setheading(i*per_cor*(-1))
        turtle.forward(a)
        turtle.left(per_cor)
        turtle.forward(a)
    turtle.end_fill()
    return per_cor


per_cor = draw_star(-100, 100, 5, r=200)
turtle.penup()
turtle.setpos(-100, 100)
turtle.pendown()
turtle.setheading(per_cor)
turtle.circle(-200)
turtle.mainloop()
