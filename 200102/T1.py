# 抽象类 多态 测试
from abc import ABCMeta, abstractclassmethod


class human(metaclass=ABCMeta):
    '''人类'''

    def __init__(self, type):
        self.type = type

    @abstractclassmethod
    def speak(self):
        raise NotImplementedError

    @abstractclassmethod
    def sleep(self):
        raise NotImplementedError

    @abstractclassmethod
    def study(self):
        raise NotImplementedError


class smart_man(human):
    '''聪明人'''

    def __init__(self):
        human.__init__(self, 'smart')

    def speak(self):
        print('I am stupid.')

    def sleep(self):
        print('Have a nice dream~')

    def study(self, course):
        print('Studying %s ...' % (course))


class stupid_man(human):
    '''蠢货'''

    def __init__(self):
        human.__init__(self, 'stupid')

    def speak(self):
        print('You are stupid!')

    def sleep(self):
        print('zzzzZZZZZZzzzzzZZZZZzzzZZzzzZZzz')

    def study(self, course):
        print('Studying %s ...' % (course))
        print('AAAAAAAAAAAAAAAAAAAAAAAAA')


man1 = smart_man()
man2 = stupid_man()
print(man2.type)
man2.speak()
man2.sleep()
man2.study('math')
