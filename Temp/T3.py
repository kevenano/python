# 项目： 口令保管箱
import random
import pyperclip
import sys

# 生成字符库
cha = ''
for i in range(33, 127):
    cha += chr(i)

PASSWORDS = {'QQ': ''.join(random.choices(cha, k=16)),
             'Phone': ''.join(random.choices(cha, k=9)),
             'Steam': ''.join(random.choices(cha, k=16)),
             'Microsoft': ''.join(random.choices(cha, k=12)),
             'Google': ''.join(random.choices(cha, k=13)),
             'Sony': ''.join(random.choices(cha, k=15))}

# 输入参数检测
if len(sys.argv) < 2:
    print('Usage: python3 T3.py [account] - copy account password')
    sys.exit()

account = sys.argv[1]

# if account.upper() in ' '.join(PASSWORDS.keys()).upper():
#    pyperclip.copy()

if account in PASSWORDS.keys():
    pyperclip.copy(PASSWORDS[account])
    print('Password copied to the clipboard!')
else:
    print('No such account!')
    print('Accounts avilable:')
    print('\n'.join(PASSWORDS.keys()))
    sys.exit()
