# Лабораторна 5 — криптографічні алгоритми

Каталог містить три окремі скрипти:

- `lab5_primality_tests.py` — решето Ератосфена та ймовірнісні тести простоти (Ферма, Соловая–Штрассена, Міллера–Рабіна) з CLI для перевірки чисел.
- `affine_cipher.py` — афінна моноалфавітна заміна (`E(x) = (a*x + b) mod m`, `D(y) = a^{-1}(y - b) mod m`). Працює з довільним алфавітом (за замовчуванням A–Z), фільтрує текст до символів алфавіту.
- `vigenere_cipher.py` — шифр Віженера з довільним алфавітом (за замовчуванням A–Z), очищує текст та ключ до літер алфавіту.

## Приклади запуску

Прості числа та тести простоти:
```bash
python lab5_primality_tests.py
python lab5_primality_tests.py 17 561 1105 --rounds 8 --limit 100
```

Афінний шифр:
```bash
python affine_cipher.py encrypt --text "HELLO WORLD" --a 5 --b 8
python affine_cipher.py decrypt --text "RCLLAOAPLX" --a 5 --b 8
```

Шифр Віженера:
```bash
python vigenere_cipher.py encrypt --text "ATTACK AT DAWN" --key LEMON
python vigenere_cipher.py decrypt --text "LXFOPVEFRNHR" --key LEMON
```

## Вимоги
- Python 3.10+
- Зовнішніх залежностей немає (використовується стандартна бібліотека).
