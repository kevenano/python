# 正则
import re

mess = 'My number is 736-867-9963, and 239-233-1960'
phoneNumRegex = re.compile(r'\d\d\d(-)+(\d\d\d-\d\d\d\d)(ahh)*')
mo = phoneNumRegex.search(mess)
mp = phoneNumRegex.findall(mess)
print(mo.group())
# print(mp)
