import random


class RSA:
    @staticmethod
    def encode(number_to_encode: int, password: tuple):
        return (number_to_encode ** password[0]) % password[1]

    @staticmethod
    def decode(number_to_decode: int, password: tuple):
        return (number_to_decode ** password[0]) % password[1]

    @staticmethod
    def create_password():
        def create_random_prime_number():

            def is_prime(n):
                for i in range(2, n):
                    if n % i == 0:
                        return False
                else:
                    return True

            while True:
                n = random.randint(1, 10000)
                if is_prime(n):
                    return n

        pna = create_random_prime_number()
        pnb = create_random_prime_number()
        step1 = pna * pnb
        step2 = (pna - 1) * (pnb - 1)

        while True:
            to = random.randint(1, 100000)
            if to % step2 == 0 and RSA.is_prime(to) and 1 < to < step2:
                pub_pass = (to, step1)
                break

        while True:
            to_c = random.randint(1, 100000)
            if (to_c * to) % step2 == 1:
                pri_pass = (to_c, step1)
                return [pub_pass, pri_pass]

    @staticmethod
    def is_prime(n):
        for i in range(2, n):
            if n % i == 0:
                return False
        else:
            return True


pass_0 = RSA.create_password()
print(RSA.encode(18, pass_0[0]))
print(RSA.decode(RSA.encode(18, pass_0[0]), pass_0[1]))
