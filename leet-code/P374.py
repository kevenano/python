# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num: int) -> int:
import time


class Solution:
    def guessNumber(self, n: int) -> int:
        a = 1
        b = n
        while True:
            ans = (a + b) // 2
            if guess(ans) == 0:
                return ans
            elif guess(ans) == -1:
                b = ans
            else:
                a = ans+1


def guess(num: int) -> int:
    pick = 123456789
    if pick < num:
        return -1
    elif pick > num:
        return 1
    else:
        return 0


def main():
    S = Solution()
    t1 = time.time()
    S.guessNumber(123456789)
    print(time.time()-t1)


if __name__ == "__main__":
    main()
