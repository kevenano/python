class TestA:
    attr = 1


obj_a = TestA()
obj_a.attr = 1
TestA.attr = 42
print(TestA.attr, obj_a.attr)


class TestB:
    attr = 1


obj_b = TestB()
obj_b.attr = 42
print(TestB.attr, obj_b.attr)


class TestC:
    attr = 1

    def __init__(self):
        self.attr = 42


obj_c = TestC
print(TestC.attr, obj_c.attr)
