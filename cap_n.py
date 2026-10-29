"""Suc chua cua {tu n-bit : trong so w, run <= R} — dem bang quy hoach dong."""
from functools import lru_cache
UNI = 0x110000
def cap(n, w, R):
    @lru_cache(maxsize=None)
    def f(i, last, run, ones):
        if ones < 0 or ones > n - i: return 0
        if i == n: return 1 if ones == 0 else 0
        t = 0
        for b in (0, 1):
            nr = run + 1 if b == last else 1
            if nr > R: continue
            t += f(i+1, b, nr, ones-b)
        return t
    return sum(f(1, b, 1, w-b) for b in (0,1))

print(f"{'n':>3}{'w':>4}{'lech/tu':>9}{'R=2':>14}{'R=3':>14}{'R=4':>14}{'du R=2':>10}")
for n in [34,35,36,37]:
    for w in ([n//2] if n%2==0 else [n//2, n//2+1]):
        c2,c3,c4 = cap(n,w,2), cap(n,w,3), cap(n,w,4)
        d = 2*w-n
        ok = f"{c2/UNI:.2f}x" if c2>=UNI else "THIEU"
        print(f"{n:>3}{w:>4}{d:>+9}{c2:>14,}{c3:>14,}{c4:>14,}{ok:>10}")
print()
print(f"  Unicode can: {UNI:,}")
print("  lech/tu = 2w - n : 0 = can bang hoan hao ; ±1 = phai dieu khien do lech don")
