#!/usr/bin/env python3
"""Sinh 1.000.000 mã dau cua UTF-N BASE-4 (4^N = 2^(2N)) -> 1 file .md.
Dung: python3 gen_utfN_base4.py <N>   (vd 34)
base-4 = 2^2 => waste=0 (dinh ly ⊟=0 khi base la luy thua 2). Moi digit 2 bit, ca 4 mau hop le.
Cot: dec | quadN (base-4 MSB) | bin2N (2-bit/digit, KHONG reserved) | hex (ceil(2N/8) byte)
"""
import sys, math
N = int(sys.argv[1]); COUNT = 1_000_000
DIG2BIN = {0:'00',1:'01',2:'10',3:'11'}   # base-4: TAT CA hop le
NBITS = 2*N; NBYTES = math.ceil(NBITS/8)
cap = 4**N
def foldN(v):
    d=[]
    for _ in range(N): d.append(v%4); v//=4
    return d                                # LSB-first
fn=f"utf{N}_base4_1M_binary.md"
with open(fn,'w') as f:
    f.write(f"# UTF-{N} BASE-4 — 1.000.000 mã nhị phân đầu của codespace 4^{N} = 2^{NBITS}\n\n")
    f.write(f"Giá trị 0…999.999 trong codespace UTF-{N} base-4 (4^{N} = {cap:,} = 2^{NBITS}).\n")
    f.write(f"base-4 = 2² → **waste = 0** (định lý ⊟=0 khi base là lũy thừa 2). Mọi mẫu 2-bit hợp lệ, KHÔNG reserved.\n\n")
    f.write(f"- `quad{N}` = {N} chữ số base-4 (0,1,2,3; MSB-first), val = Σ dᵢ·4ⁱ\n")
    f.write(f"- `bin{NBITS}` = mã nhị phân thuần: mỗi digit → 2 bit (0=00 1=01 2=10 3=11) = {NBITS} bit (= chính val nhị phân)\n")
    f.write(f"- `hex{NBYTES}` = {NBYTES} byte ({NBYTES*8} bit, pad {NBYTES*8-NBITS} bit cao)\n\n")
    f.write("```\n")
    f.write(f"{'dec':>7} | {'quad'+str(N)+' (base-4)':<{N}} | {'bin'+str(NBITS)+' (2-bit/digit)':<{NBITS}} | hex{NBYTES}\n")
    f.write("-"*7+"-+-"+"-"*N+"-+-"+"-"*NBITS+"-+-"+"-"*(NBYTES*2)+"\n")
    buf=[]
    for v in range(COUNT):
        dl=foldN(v); dm=dl[::-1]
        quad=''.join(map(str,dm))
        bins=''.join(DIG2BIN[x] for x in dm)
        hx=format(v,f'0{NBYTES*2}x')
        buf.append(f"{v:>7} | {quad} | {bins} | {hx}")
        if len(buf)>=20000: f.write("\n".join(buf)+"\n"); buf=[]
    if buf: f.write("\n".join(buf)+"\n")
    f.write("```\n")
print(f"UTF-{N} base-4: 1.000.000 dong -> {fn} | {NBYTES} byte/ma, cap 4^{N}={cap:,}=2^{NBITS}")
