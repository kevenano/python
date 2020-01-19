# 正则2
import re
import pyperclip

# 电话号码正则
phoneNumRegex = re.compile(r'''(
        (\+\d{1,2}(\s|-)?)?         # 区号
        ((\d{11})                   # 7-11位号码
        |(\d{3}\s?\d{4}\s?\d{4})    # 11位有分隔手机号
        |(\d{3}|\(\d{3}\))          # 10位手机号, area code
        (\s|-|–)?                     # 分隔符
        (\d{3}(\s|-|–)?)              # first 3
        (\d{4}))                    # last 4
        )''', re.VERBOSE)
# 邮件正则
emailAdd = re.compile(r'''(
        [a-zA-Z0-9._%+-]+   # 用户名
        @                   # @
        [a-zA-Z0-9.-]+      # 主机名
        (\.[a-zA-Z0-9]+)    # .域名
        )''', re.VERBOSE)
# 库
# mess = '''
#        number: +86 18512845114;13338229966;+86188374094;134 3822 9999
#        email : henzod92@outlook.com;dsagf.23099skkd@gmail.ccp;
#        '''

"""
mp = phoneNumRegex.findall(mess)
me = emailAdd.findall(mess)
"""
"""
for i in range(len(mp)):
    print(mp[i][0])
for i in range(len(me)):
    print(me[i][0])
"""

# Find matches in clipboard text
messTet = str(pyperclip.paste())
mp = phoneNumRegex.findall(messTet)
me = emailAdd.findall(messTet)

# Copy result to the clipboard
# 法1
mpOut = ''
for i in range(len(mp)):
    mpOut += mp[i][0]+'\n'
meOut = ''
for i in range(len(me)):
    meOut += me[i][0]+'\n'
allOut = mpOut+meOut

# 法2
mpOut2 = []
for i in range(len(mp)):
    mpOut2.append(mp[i][0])
mpOut2 = list(set(mpOut2))
meOut2 = []
for i in range(len(me)):
    meOut2.append(me[i][0])
meOut2 = list(set(meOut2))
allOut2 = '\n'.join(mpOut2 + meOut2)

if len(allOut2) > 0:
    pyperclip.copy(allOut2)
    print('Result copied to the clipboard!')
else:
    print('No matches found!')
    exit()
