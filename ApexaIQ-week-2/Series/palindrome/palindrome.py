def check_palindrome(word):
    palindrome = " ".join(word.lower().split())
    if palindrome == palindrome[::-1]:
        print(f"The word {palindrome} is a palindromme.")
        return True 
    else:
        return print(f"The word {palindrome} is NOT a palindrome.")

check_palindrome("madam")
check_palindrome("john")