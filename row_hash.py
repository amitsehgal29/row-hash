"""row-hash: add a stable SHA-256 hash column to each CSV row for change detection (CDC)."""
import argparse, csv, hashlib, sys

def row_hash(row, cols, sep="\x1f"):
    vals = [(row.get(c) or "").strip() for c in cols]
    return hashlib.sha256(sep.join(vals).encode("utf-8")).hexdigest()

def add_hashes(src, dst, cols=None, name="row_hash"):
    with open(src, newline="", encoding="utf-8") as f, open(dst, "w", newline="", encoding="utf-8") as o:
        r = csv.DictReader(f)
        fields = r.fieldnames or []
        use = cols or fields
        missing = [c for c in use if c not in fields]
        if missing:
            raise ValueError(f"unknown columns: {missing}")
        w = csv.DictWriter(o, fieldnames=fields + [name])
        w.writeheader()
        n = 0
        for row in r:
            row[name] = row_hash(row, use)
            w.writerow(row); n += 1
    return n

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--cols", help="comma-separated columns to hash (default: all)")
    p.add_argument("--name", default="row_hash")
    a = p.parse_args(argv)
    n = add_hashes(a.src, a.dst, a.cols.split(",") if a.cols else None, a.name)
    print(f"hashed {n} rows -> {a.dst}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
