import time


def time_it(x):
    start = time.time()

    def iterate(y):
        for i in range(x):
            for j in range(y):
                calc = i * j

        return y * x

    end = time.time()

    elapse = end - start
    return iterate, elapse


runTime = time_it(10)
print(runTime[0](20))
print(runTime[1])
