def palin_checker(text):
    val = False
    if text[::-1] == text:
        val = True

    return val

paltext = input("Give some text and we will check if it is a palindrome! \n")

print(palin_checker(paltext))
