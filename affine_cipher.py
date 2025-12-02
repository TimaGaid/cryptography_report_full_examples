#!/usr/bin/env python3
"""
Affine monoalphabetic substitution cipher with CLI for encryption/decryption.
"""
import argparse
from typing import List, Tuple


def mod_inverse(a: int, m: int) -> int:
    """Return modular inverse of a mod m or raise ValueError if not invertible."""
    t, new_t = 0, 1
    r, new_r = m, a % m
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError(f"a={a} is not invertible modulo {m}")
    return t % m


def prepare_alphabet(alphabet: str) -> str:
    seen = set()
    cleaned = []
    for ch in alphabet:
        up = ch.upper()
        if up.isalpha() and up not in seen:
            seen.add(up)
            cleaned.append(up)
    if len(cleaned) < 2:
        raise ValueError("Alphabet must have at least 2 unique letters")
    return "".join(cleaned)


def clean_text(text: str, alphabet: str) -> str:
    letters = set(alphabet)
    return "".join(ch.upper() for ch in text if ch.upper() in letters)


def affine_encrypt(text: str, a: int, b: int, alphabet: str) -> str:
    m = len(alphabet)
    letters = {ch: idx for idx, ch in enumerate(alphabet)}
    out: List[str] = []
    for ch in clean_text(text, alphabet):
        x = letters[ch]
        y = (a * x + b) % m
        out.append(alphabet[y])
    return "".join(out)


def affine_decrypt(cipher: str, a: int, b: int, alphabet: str) -> str:
    m = len(alphabet)
    a_inv = mod_inverse(a, m)
    letters = {ch: idx for idx, ch in enumerate(alphabet)}
    out: List[str] = []
    for ch in clean_text(cipher, alphabet):
        y = letters[ch]
        x = (a_inv * (y - b)) % m
        out.append(alphabet[x])
    return "".join(out)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Affine monoalphabetic substitution cipher")
    ap.add_argument("mode", choices=["encrypt", "decrypt"], help="operation mode")
    ap.add_argument("--text", required=True, help="input text")
    ap.add_argument("--a", type=int, required=True, help="multiplier a (must be coprime with alphabet length)")
    ap.add_argument("--b", type=int, required=True, help="shift b")
    ap.add_argument("--alphabet", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ", help="alphabet to use (unique letters)")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    alphabet = prepare_alphabet(args.alphabet)
    m = len(alphabet)
    if args.a % m == 0:
        raise SystemExit("Multiplier a cannot be 0 mod alphabet length")
    try:
        if args.mode == "encrypt":
            result = affine_encrypt(args.text, args.a, args.b, alphabet)
        else:
            result = affine_decrypt(args.text, args.a, args.b, alphabet)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print(f"Alphabet length m = {m}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
