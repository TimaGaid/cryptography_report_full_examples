from __future__ import annotations

import argparse
import math
import random
from typing import Iterable, List, Sequence, Tuple


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    result = 1
    base %= modulus
    e = exponent
    while e:
        if e & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        e >>= 1
    return result


def jacobi(a: int, n: int) -> int:
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def decompose_n_minus_one(n: int) -> Tuple[int, int]:
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def fermat_primality(n: int, k: int = 5, rng: random.Random | None = None) -> bool:
    rng = rng or random
    if n <= 3:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = rng.randrange(2, n - 1)
        if math.gcd(a, n) != 1:
            return False
        if mod_pow(a, n - 1, n) != 1:
            return False
    return True


def solovay_strassen(n: int, k: int = 5, rng: random.Random | None = None) -> bool:
    rng = rng or random
    if n <= 3:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = rng.randrange(2, n - 1)
        if math.gcd(a, n) != 1:
            return False
        exp = (n - 1) // 2
        mod_val = mod_pow(a, exp, n)
        j = jacobi(a, n) % n
        if mod_val != j:
            return False
    return True


def miller_rabin(n: int, k: int = 8, rng: random.Random | None = None) -> bool:
    rng = rng or random
    if n <= 3:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    s, d = decompose_n_minus_one(n)
    for _ in range(k):
        a = rng.randrange(2, n - 2)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def sieve_eratosthenes(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    p = 2
    while p * p <= limit:
        if sieve[p]:
            step = p
            start = p * p
            sieve[start: limit + 1: step] = b"\x00" * (((limit - start) // step) + 1)
        p += 1
    return [i for i in range(2, limit + 1) if sieve[i]]


def run_demo(numbers: Sequence[int], rounds: int, limit: int, seed: int | None) -> None:
    rng = random.Random(seed) if seed is not None else random
    print(f"Primes up to {limit}: {sieve_eratosthenes(limit)}")
    for n in numbers:
        print(f"\nTesting n = {n}")
        print(f"  Fermat            : {fermat_primality(n, k=rounds, rng=rng)}")
        print(f"  Solovay-Strassen  : {solovay_strassen(n, k=rounds, rng=rng)}")
        print(f"  Miller-Rabin      : {miller_rabin(n, k=rounds, rng=rng)}")


def parse_numbers(raw: Iterable[str]) -> List[int]:
    out: List[int] = []
    for token in raw:
        if token.startswith("0x"):
            out.append(int(token, 16))
        else:
            out.append(int(token))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 5: probabilistic primality tests")
    parser.add_argument("numbers", nargs="*", help="numbers to test (decimal or 0x...)")
    parser.add_argument("--rounds", type=int, default=10, help="rounds per probabilistic test")
    parser.add_argument("--limit", type=int, default=50, help="upper bound for sieve demo")
    parser.add_argument("--seed", type=int, help="seed for RNG to make results reproducible")
    args = parser.parse_args()

    default_numbers = [17, 561, 1105, (1 << 61) - 1]
    numbers = parse_numbers(args.numbers) if args.numbers else default_numbers
    run_demo(numbers=numbers, rounds=args.rounds, limit=args.limit, seed=args.seed)


if __name__ == "__main__":
    main()
