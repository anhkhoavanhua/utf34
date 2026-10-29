"""UTF-N (N = 34,35,36,37) — sinh bang chiet tich: combinadic co rang buoc + SIGMA-MR.
   n chan: w = n/2, lech moi tu = 0.
   n le  : hai bien the w = (n-1)/2 va (n+1)/2, chon theo DO LECH DON (nhu 8b/10b)."""
from functools import lru_cache
UNI = 0x110000

class UTFN:
    def __init__(self, n, R=2):
        self.n, self.R = n, R
        self.ws = [n//2] if n % 2 == 0 else [n//2, n//2+1]
        self._f = {}
        for w in self.ws: self._mk(w)
    def _mk(self, w):
        n, R = self.n, self.R
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
        self._f[w] = f
    def cap(self, w): return sum(self._f[w](1, b, 1, w-b) for b in (0,1))
    def enc(self, c, disp=0):
        """disp = do lech don hien tai; n le -> chon bien the keo ve 0"""
        if len(self.ws) == 1: w = self.ws[0]
        else: w = self.ws[1] if disp < 0 else self.ws[0]   # disp<0 -> chon w lon (them 1)
        f = self._f[w]; n, R = self.n, self.R
        x = 0; r = c; last = -1; run = 0; ones = w
        for i in range(n):
            for b in (0, 1):
                nr = run + 1 if b == last else 1
                if nr > R: continue
                k = f(i+1, b, nr, ones-b)
                if r < k:
                    if b: x |= 1 << (n-1-i)
                    last, run, ones = b, nr, ones-b; break
                r -= k
            else: raise RuntimeError
        return x, 2*w - n
    def dec(self, x):
        n, R = self.n, self.R
        w = bin(x).count('1')
        if w not in self._f: raise ValueError(f"trong so {w} khong hop le")
        f = self._f[w]
        c = 0; last = -1; run = 0; ones = w
        for i in range(n):
            bit = (x >> (n-1-i)) & 1
            for b in (0, 1):
                nr = run + 1 if b == last else 1
                if nr > R: continue
                if b == bit: last, run, ones = b, nr, ones-b; break
                c += f(i+1, b, nr, ones-b)
        return c

if __name__ == "__main__":
    print(f"{'UTF-N':>7}{'w':>10}{'suc chua':>16}{'du':>9}{'lech/tu':>10}")
    for n in [34,35,36,37]:
        u = UTFN(n)
        caps = [u.cap(w) for w in u.ws]
        print(f"{'UTF-'+str(n):>7}{str(u.ws):>10}{caps[0]:>16,}{caps[0]/UNI:>8.2f}x{'0' if n%2==0 else '±1':>10}")
    print()
    print("=== Vi du 'A' (U+0041) ===")
    for n in [34,35,36,37]:
        u = UTFN(n); x,d = u.enc(65, 0)
        print(f"  UTF-{n}: {format(x,'0%db'%n)}  w={bin(x).count('1')} lech={d:+d} RT={u.dec(x)==65}")
