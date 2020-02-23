from math import pi
import cmath


def whirl(L, kn):
    return cmath.exp(-1j*2*pi*kn/L)


def fft(x):
    L = len(x)
    if L == 2:
        X = [0]*2
        X[0] = x[0]*whirl(2, 0)+x[1]*whirl(2, 0)
        X[1] = x[0]*whirl(2, 0)+x[1]*whirl(2, 1)
        return X
    # 获取偶数项和奇数项
    x0 = []
    x1 = []
    for i in range(L):
        if i % 2 == 0:
            x0.append(x[i])
        else:
            x1.append(x[i])
    #
    X = [0]*L
    for k in range(int(L/2)):
        X0 = fft(x0)
        X1 = fft(x1)
        X[k] = X0[k]+whirl(L, k)*X1[k]
        X[k+int(L/2)] = X0[k]-whirl(L, k)*X1[k]
    return X


def test():
    x = list(range(8))
    X = fft(x)
    for item in X:
        print('%.4f%+.4fj' % (item.real, item.imag))


# 测试
if __name__ == '__main__':
    test()
