def new_txt(name, msg='$'):
    path = name+'.txt'
    file = open(path, 'w')
    file.write(msg)
    file.close()
    print('Done!')


password_list = ['$$kkon&&~', '123455']


def account_login():
    password = input('Password: ')
    password_correct = password == password_list[-1]
    password_reset = password == password_list[0]
    if password_correct:
        print('Login success!')
    elif password_reset:
        new_password = input('Enter a new password: ')
        password_list.append(new_password)
        print('Your password has changed successfully!')
        account_login()
    elif password == 'fuck off' or password == 'exit()':
        exit()
    else:
        print('Wrong password or invalid input!')
        account_login()


account_login()
print('Let\'s continue...')

for num1 in range(1, 10, 1):
    for num2 in range(1, num1+1, 1):
        print('{}\t'.format(num1*num2), end=' ')
        if num2 == num1:
            print('\n')

print('---------------------------------------------------------------------')
num1 = 1
while num1 <= 9:
    num2 = 1
    while num2 <= num1:
        print('{}\t'.format(num1*num2), end=' ')
        if num2 == num1:
            print('\n')
        num2 = num2+1
    num1 = num1+1

print('---------------------------------------------------------------------')
a = {'key1': '123456', 'key2': 'qhm201', 'key3': '$$kkon&&~'}
print(a, '\t', type(a))
