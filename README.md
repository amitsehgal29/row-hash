# row-hash

Add a stable SHA-256 hash column to every CSV row, so you can spot changed rows between loads (CDC-style) by comparing one column instead of all of them.

Pure Python stdlib. Values are trimmed and joined with a unit separator, so `ab|c` and `a|bc` never collide.

```bash
python row_hash.py customers.csv customers_hashed.csv --cols id,name,email
```

Leave out `--cols` to hash every column. Use `--name` to rename the output column.

```bash
python -m unittest -v
```
