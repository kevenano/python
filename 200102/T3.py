class Student(object):

    def __init__(self):
        self._birth = 100

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        print('HAAAA')
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth
