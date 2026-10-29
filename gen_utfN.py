#!/usr/bin/env python3
"""Sinh 1.000.000 mã dau cua codespace UTF-N (3^N, base-3) -> 1 file .md.
Dung: python3 gen_utfN.py <N>   (N = so trit, vd 36, 38)
Cot: dec | tritN(base-3 MSB) | bin2N(2bit/trit 00/01/10) | hexP(packed 5trit/byte base-243)
"""
import sys, math
N = int(sys.argv[1])
COUNT = 1_000_000
TRIT2BIN = {0:'00', 1:'01', 2:'10'}      # 11 = RESERVED
NBYTES = math.ceil(N/5)                    # 5 trit/byte base-243
PAD = NBYTES*5 - N

def foldN(v):
    t=[]
    for _ in range(N): t.append(v%3); v//=3
    return t                               # LSB-first, len N
def pack_hex(t_lsb):
    t = t_lsb + [0]*PAD                     # pad len -> NBYTES*5
    out=[]
    for i in range(NBYTES):
        b=0
        for x in reversed(t[i*5:i*5+5]): b=b*3+x
        out.append(b)
    return bytes(out).hex()

cap = 3**N
fn = f"utf{N}_1M_binary.md"
with open(fn,'w') as f:
    f.write(f"# UTF-{N} — 1.000.000 mã nhị phân đầu của codespace 3^{N}\n\n")
    f.write(f"Giá trị 0…999.999 trong codespace UTF-{N} (3^{N} = {cap:,}).\n")
    f.write(f"Mã UTF-{N} **thuần** — KHÔNG giới hạn Unicode. Sinh bằng chiết tích Fold base-3 + MIN-WASTE pack.\n\n")
    f.write(f"- `trit{N}` = {N} trit tam phân (Fold base-3, MSB-first), val = Σ dᵢ·3ⁱ\n")
    f.write(f"- `bin{2*N}` = mã nhị phân thuần: mỗi trit → 2 bit (0=00 1=01 2=10; 11 RESERVED) = {2*N} bit\n")
    f.write(f"- `hex{NBYTES}` = {NBYTES} byte đóng gói MIN-WASTE (5 trit/byte base-243, pad {PAD} trit) = {NBYTES*8} bit\n\n")
    f.write("```\n")
    f.write(f"{'dec':>7} | {'trit'+str(N)+' (base-3, MSB)':<{N}} | {'bin'+str(2*N)+' (2-bit/trit)':<{2*N}} | hex{NBYTES}\n")
    f.write("-"*7+"-+-"+"-"*N+"-+-"+"-"*(2*N)+"-+-"+"-"*(NBYTES*2)+"\n")
    buf=[]
    for v in range(COUNT):
        tl=foldN(v); tm=tl[::-1]
        trit=''.join(map(str,tm))
        bins=''.join(TRIT2BIN[x] for x in tm)
        hx=pack_hex(tl)
        buf.append(f"{v:>7} | {trit} | {bins} | {hx}")
        if len(buf)>=20000: f.write("\n".join(buf)+"\n"); buf=[]
    if buf: f.write("\n".join(buf)+"\n")
    f.write("```\n")
print(f"UTF-{N}: 1.000.000 dong -> {fn} | {NBYTES} byte/ma, cap 3^{N}={cap:,}")
