# 字符串
def printComp(com, leftWidth, rightWidth):
    print('This computer:')
    for k, v in com.items():
        print(k.ljust(leftWidth, '-')+str(v).rjust(rightWidth))


myComp = {'Name': 'HP_ElilteBook', 'Model': '735G5',
          'CPU': 'AMD', 'RAM': '8G', 'Color': 'silver'}

printComp(myComp, 10, 18)
