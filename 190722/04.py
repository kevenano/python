#bytes类型
b1=bytes()
b2=b''
b3=b'hello'
print(b3)
print(b3[0])
print(b3[2:4])
print(b3[0:0])
print(b3[4:4])
b4=bytes('I love python(我爱python)',encoding='utf-8')
print(b4)
b4=bytes('I love python(我爱python)',encoding='utf-16')
print(b4)
b5="I enjoy prongramming(编程很有趣)".encode('utf-8')
print(b5)
b5="I enjoy prongramming(编程很有趣)".encode('UTF-16')
print(b5)
st=b5.decode('utf-16')
print(st)
print(len(b5))
print(len(st))
print(len("I enjoy prongramming(编程很有趣)"))
print(len(st.encode('utf-16')))
print(len(b5.decode('utf-16')))
print(b5)
print(b5.decode('utf-16').encode('gbk'))
print("I enjoy prongramming(编程很有趣)".encode('gbk'))
print("I enjoy prongramming(编程很有趣)")

