#!/usr/bin/env python3
"""Sinh 1.000.000 mã dau cua UTF-N BASE-2 (2^N, nhi phan thang) -> 1 file .md.
Dung: python3 gen_utfN_base2.py <N>   (vd 34)
Cot: dec | binN (N-bit base-2 truc tiep) | hex (dong goi ceil(N/8) byte)
"""
import sys, math
N = int(sys.argv[1]); COUNT = 1_000_000
NBYTES = math.ceil(N/8)
cap = 2**N
fn = f"utf{N}_base2_1M_binary.md"
with open(fn,'w') as f:
    f.write(f"# UTF-{N} BASE-2 — 1.000.000 mã nhị phân đầu của codespace 2^{N}\n\n")
    f.write(f"Giá trị 0…999.999 trong codespace UTF-{N} base-2 (2^{N} = {cap:,}).\n")
    f.write(f"Mã nhị phân **thẳng** (base-2), KHÔNG qua trit. Mỗi mã = {N} bit.\n\n")
    f.write(f"- `bin{N}` = {N} bit nhị phân trực tiếp (base-2), val = Σ bᵢ·2ⁱ\n")
    f.write(f"- `hex{NBYTES}` = {NBYTES} byte ({NBYTES*8} bit, pad {NBYTES*8-N} bit cao)\n\n")
    f.write("```\n")
    f.write(f"{'dec':>7} | {'bin'+str(N)+' (base-2)':<{N}} | hex{NBYTES}\n")
    f.write("-"*7+"-+-"+"-"*N+"-+-"+"-"*(NBYTES*2)+"\n")
    buf=[]
    for v in range(COUNT):
        binN = format(v, f'0{N}b')
        hx = format(v, f'0{NBYTES*2}x')
        buf.append(f"{v:>7} | {binN} | {hx}")
        if len(buf)>=20000: f.write("\n".join(buf)+"\n"); buf=[]
    if buf: f.write("\n".join(buf)+"\n")
    f.write("```\n")
print(f"UTF-{N} base-2: 1.000.000 dong -> {fn} | {NBYTES} byte/ma, cap 2^{N}={cap:,}")
