# The Passport Page of a Country That Isn't There

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Anggizx90/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Anggizx90/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)

Entry for the [make.fun](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
competition **The Passport Page of a Country That Isn't There**.

`main.py` (Python 3.13, Pillow only, no network) draws one uncaptioned open
passport spread for an invented country — the **Republic of Caldris**, a
North Atlantic island nation, capital Port Anselm — and writes it to
`/output/entry.png` (1024×1024 PNG, under 1 MiB).

- **Left page — data page:** state crest, holder Elin Mara Voss (born
  14 Mar 1992, Port Anselm), a code-drawn portrait of the holder in her
  lighthouse-keeper's uniform, bilingual field labels, signature, and a
  valid ICAO 9303 machine-readable strip with correct check digits.
- **Right page — visas:** arrival/departure stamps from the two
  neighbouring countries, Kestrelia (ferry) and Vordania (mountain pass),
  in three matching pairs — every stamp dated after the passport's issue
  (02 Jun 2025) and before its expiry (01 Jun 2035).
- **Telling detail:** a Kestrelia visa-condition box (30-day stay, no
  employment, return ferry booked before entry, fare payable in caldr
  only) and a "Harbour Tax Paid — 12 CLD" fee stamp, tying the paperwork
  to an island nation that lives by its ferries and its lighthouse.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

Deterministic: re-running produces a byte-identical image.

## License

MIT — see [LICENSE](LICENSE).
