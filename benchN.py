from utfN import UTFN, UNI
import time, random
txt = open('/tmp/vi.txt', encoding='utf-8', errors='replace').read()[:20000]

def stream(u):
    """ma hoa ca van ban, dieu khien do lech don"""
    out = []; disp = 0
    for ch in txt:
        x, d = u.enc(ord(ch), disp); disp += d
        out.append(format(x, '0%db' % u.n))
    return ''.join(out)

def stats(b):
    n = len(b); on = b.count('1')
    tr = sum(1 for i in range(n-1) if b[i] != b[i+1])
    d = 0; mx = 0
    for c in b:
        d += 1 if c == '1' else -1
        if abs(d) > mx: mx = abs(d)
    r = 1; rm = 1
    for i in range(1, n):
        if b[i] == b[i-1]: r += 1; rm = max(rm, r)
        else: r = 1
    return n, abs(2*on-n)/n*100, tr/n*100, rm, mx, d

print("=== KIEM ROUND-TRIP TOAN BO UNICODE ===")
for n in [34,35,36,37]:
    u = UTFN(n); bad = 0; seen = set()
    for c in range(UNI):
        x,_ = u.enc(c, 0)
        if u.dec(x) != c: bad += 1
        seen.add(x)
    print(f"  UTF-{n}: sai {bad}/{UNI}   tu khac nhau {len(seen):,}   {'DON ANH' if len(seen)==UNI else 'TRUNG'}")

print()
print("=== HIEU SUAT tren van ban that (20 000 ky tu) ===")
print(f"{'ma hoa':<10}{'bit':>9}{'lech DC':>10}{'chuyen doi':>12}{'run max':>9}{'|lech| MAX':>12}{'ket thuc':>10}{'vs UTF-32':>11}")
b32 = ''.join(format(ord(c),'032b') for c in txt)
b8  = ''.join(format(x,'08b') for x in txt.encode('utf-8'))
for nm,b in [('UTF-8',b8),('UTF-32',b32)]:
    s = stats(b); print(f"{nm:<10}{s[0]:>9}{s[1]:>9.2f}%{s[2]:>11.2f}%{s[3]:>9}{s[4]:>12,}{s[5]:>10,}{s[0]/len(b32):>10.2f}x")
for n in [34,35,36,37]:
    u = UTFN(n); b = stream(u); s = stats(b)
    print(f"{'UTF-'+str(n):<10}{s[0]:>9}{s[1]:>9.2f}%{s[2]:>11.2f}%{s[3]:>9}{s[4]:>12,}{s[5]:>10,}{s[0]/len(b32):>10.2f}x")

print()
print("=== TOC DO (ma hoa + giai ma, 20 000 ky tu) ===")
print(f"{'ma hoa':<10}{'encode us/ky tu':>18}{'decode us/ky tu':>18}")
for n in [34,35,36,37]:
    u = UTFN(n); cs = [ord(c) for c in txt[:3000]]
    t0=time.perf_counter(); xs=[u.enc(c,0)[0] for c in cs]; te=(time.perf_counter()-t0)/len(cs)*1e6
    t0=time.perf_counter(); [u.dec(x) for x in xs];        td=(time.perf_counter()-t0)/len(cs)*1e6
    print(f"{'UTF-'+str(n):<10}{te:>18.2f}{td:>18.2f}")
