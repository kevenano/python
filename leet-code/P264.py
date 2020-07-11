import time


class Solution:
    def nthUglyNumber(self, n: int) -> int:
        i = 0
        cnt = 0
        while cnt < n:
            i += 1
            if self.dePrime(i).issubset({1, 2, 3, 5}) is True:
                cnt += 1
        return i

    def isPrime(self, n: int) -> bool:
        if n == 1 or n == 2:
            return True
        else:
            for i in range(2, int(n / 2) + 2):
                if n % i == 0:
                    return False
            return True

    def dePrime(self, n: int):
        res = [1]
        if self.isPrime(n) is True:
            return set([1, n])
        while self.isPrime(n) is False:
            for i in range(2, int(n / 2) + 1):
                if self.isPrime(i) is True and n % i == 0:
                    res.append(i)
                    n = n / i
        return set(res)


class Solution2:
    def nthUglyNumber(self, n: int) -> int:
        start = [1]
        for i in range(2, n+1):
            new = [2*start[-1], 3*start[-1], 5*start[-1]]
            new.sort()
            start.append(new[0])
        return start[-1]


def main():
    S = Solution2()
    t1 = time.time()
    print(S.nthUglyNumber(10))
    print(time.time() - t1)


if __name__ == "__main__":
    main()
