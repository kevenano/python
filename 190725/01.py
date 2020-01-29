#类型转换，输入测试，%求模运算
a=float(input('Enter the value of a:'))
b=float(input('Enter the value of b:'))
print(a)
print(b)
c=a%b
d=b%a
print(c)
print(d)
print('a%b=',str(c))
print('b%a=',str(d))
print(id(a),id(b),id(c),id(d),sep='|')