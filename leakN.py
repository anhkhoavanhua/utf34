from utfN import UTFN, UNI
import collections, math, random
txt = open('/tmp/vi.txt', encoding='utf-8', errors='replace').read()[:20000]
def leak(name, enc):
    p = collections.Counter()
    for ch in txt:
        try: b = enc(ch)
        except Exception: continue
        p[(ch, b.count('1'))] += 1
    N = sum(p.values()); pc = collections.Counter(); pw = collections.Counter()
    for (c,w),v in p.items(): pc[c]+=v; pw[w]+=v
    H = lambda d: -sum(v/N*math.log2(v/N) for v in d.values())
    I = H(pc)+H(pw)-H(p)
    return H(pc), H(pw), I

print("=== RO RI KENH PHU  I(ky tu ; trong so Hamming) ===")
print(f"{'ma hoa':<10}{'H(ky tu)':>10}{'H(trong so)':>13}{'RO RI bit':>12}{'% ky tu lo':>13}")
rows = [('UTF-8',  lambda c: ''.join(format(b,'08b') for b in c.encode('utf-8'))),
        ('UTF-32', lambda c: format(ord(c),'032b'))]
for nm,f in rows:
    Hc,Hw,I = leak(nm,f); print(f"{nm:<10}{Hc:>10.2f}{Hw:>13.2f}{I:>12.3f}{I/Hc*100:>12.1f}%")
for n in [34,35,36,37]:
    u = UTFN(n)
    Hc,Hw,I = leak(f'UTF-{n}', lambda c,u=u: format(u.enc(ord(c),0)[0],'0%db'%u.n))
    print(f"{'UTF-'+str(n):<10}{Hc:>10.2f}{Hw:>13.2f}{I:>12.3f}{I/Hc*100:>12.1f}%")

print()
print("=== PHAT HIEN LOI: lat 1 bit -> trong so doi -> bat duoc? ===")
random.seed(2)
print(f"{'ma hoa':<10}{'ty le phat hien 1-bit':>24}{'khoang cach toi thieu':>24}")
for nm,tot in [('UTF-8',0),('UTF-32',0)]:
    print(f"{nm:<10}{'0.0%':>24}{'1 (khong phat hien)':>24}")
for n in [34,35,36,37]:
    u = UTFN(n); det=0; N=3000
    for _ in range(N):
        c = random.randrange(UNI); x,_ = u.enc(c,0)
        y = x ^ (1 << random.randrange(n))
        try:
            u.dec(y); ok=False           # giai ma duoc -> KHONG bat duoc
        except Exception: ok=True        # trong so/run sai -> BAT DUOC
        det += ok
    print(f"{'UTF-'+str(n):<10}{det/N*100:>23.1f}%{'2 (trong so co dinh)':>24}")
