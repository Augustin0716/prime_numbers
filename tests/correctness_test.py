from src.prime_numbers import is_prime

if __name__ == '__main__':
    if is_prime(int(input("Enter a number : "))):
        print("Prime number")
    else:
        print("Composite number")