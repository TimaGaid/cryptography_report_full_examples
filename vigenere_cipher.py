#!/usr/bin/env python3
"""
Vigenere cipher implementation with CLI for encryption/decryption.
"""
import argparse
from typing import List


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


def prepare_key(key: str, length: int, alphabet: str) -> List[int]:
    cleaned = clean_text(key, alphabet)
    if not cleaned:
        raise ValueError("Key must contain at least one letter from the alphabet")
    letters = {ch: idx for idx, ch in enumerate(alphabet)}
    shifts = [letters[ch] for ch in cleaned]
    return [shifts[i % len(shifts)] for i in range(length)]


def vigenere(text: str, key: str, alphabet: str, encrypt: bool) -> str:
    letters = {ch: idx for idx, ch in enumerate(alphabet)}
    clean = clean_text(text, alphabet)
    key_shifts = prepare_key(key, len(clean), alphabet)
    out: List[str] = []
    for ch, k in zip(clean, key_shifts):
        x = letters[ch]
        y = (x + k) % len(alphabet) if encrypt else (x - k) % len(alphabet)
        out.append(alphabet[y])
    return "".join(out)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Vigenere cipher")
    ap.add_argument("mode", choices=["encrypt", "decrypt"], help="operation mode")
    ap.add_argument("--text", required=True, help="input text")
    ap.add_argument("--key", required=True, help="keyword")
    ap.add_argument("--alphabet", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ", help="alphabet to use (unique letters)")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    alphabet = prepare_alphabet(args.alphabet)
    try:
        result = vigenere(args.text, args.key, alphabet, encrypt=(args.mode == "encrypt"))
    except ValueError as exc:
        raise SystemExit(str(exc))
    print(f"Alphabet length m = {len(alphabet)}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
