limit = int(input("\nHow many fibonacci numbers should there be? "))

fibonacciSequence=[1, 1]

for i in range(limit - 2):
    fibonacciSequence.append(fibonacciSequence[-1] + fibonacciSequence[i])
print(fibonacciSequence)