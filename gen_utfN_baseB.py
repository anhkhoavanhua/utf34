#!/usr/bin/env python3
"""Sinh 1.000.000 mã dau cua UTF-N BASE-B tong quat -> 1 file .md.
Dung: python3 gen_utfN_baseB.py <N> <B>   (vd 34 100)
w = ceil(log2 B) bit/digit. Digit 0..B-1 hop le; B..2^w-1 = RESERVED (neu B khong luy thua 2).
Cot: dec | digitsN (base-B, MSB) | bin(N*w) (w-bit/digit) | hex
"""
import sys, math
N=int(sys.argv[1]); B=int(sys.argv[2]); COUNT=1_000_000
w=math.ceil(math.log2(B)); NBITS=N*w; NBYTES=math.ceil(NBITS/8)
cap=B**N
is_pow2 = (B & (B-1))==0
waste = w - math.log2(B)
def foldN(v):
    d=[]
    for _ in range(N): d.append(v%B); v//=B
    return d
def digstr(dm):  # base-B digits, moi digit padStart theo do rong so chu so cua B-1
    width=len(str(B-1))
    return ' '.join(str(x).rjust(width,'0') for x in dm)
fn=f"utf{N}_base{B}_1M_binary.md"
with open(fn,'w') as f:
    f.write(f"# UTF-{N} BASE-{B} — 1.000.000 mã nhị phân đầu của codespace {B}^{N}\n\n")
    f.write(f"Giá trị 0…999.999 trong codespace UTF-{N} base-{B} ({B}^{N} = {cap:,} ≈ 1e{len(str(cap))-1}).\n")
    f.write(f"base-{B}: w = ⌈log₂{B}⌉ = **{w} bit/chữ số**. {'Lũy thừa 2 → waste=0, không reserved.' if is_pow2 else f'KHÔNG lũy thừa 2 → digit {B}..{2**w-1} RESERVED, waste = {waste:.4f} bit/digit ({waste/w*100:.2f}%).'}\n\n")
    f.write(f"- `digits{N}` = {N} chữ số base-{B} (0..{B-1}; MSB-first), val = Σ dᵢ·{B}ⁱ\n")
    f.write(f"- `bin{NBITS}` = mã nhị phân: mỗi chữ số → {w} bit = {NBITS} bit\n")
    f.write(f"- `hex{NBYTES}` = {NBYTES} byte của chuỗi bit trên ({NBYTES*8} bit)\n\n")
    f.write("```\n")
    hdr_dig=f"digits{N} (base-{B})"; hdr_bin=f"bin{NBITS} ({w}-bit/digit)"
    f.write(f"{'dec':>7} | {hdr_dig} | {hdr_bin} | hex{NBYTES}\n")
    dwidth=(len(str(B-1))+1)*N-1
    f.write("-"*7+"-+-"+"-"*dwidth+"-+-"+"-"*NBITS+"-+-"+"-"*(NBYTES*2)+"\n")
    buf=[]
    for v in range(COUNT):
        dl=foldN(v); dm=dl[::-1]
        bins=''.join(format(x,f'0{w}b') for x in dm)
        hx=format(int(bins,2), f'0{NBYTES*2}x')
        buf.append(f"{v:>7} | {digstr(dm)} | {bins} | {hx}")
        if len(buf)>=20000: f.write("\n".join(buf)+"\n"); buf=[]
    if buf: f.write("\n".join(buf)+"\n")
    f.write("```\n")
print(f"UTF-{N} base-{B}: 1.000.000 dong -> {fn} | w={w}bit/digit, {NBYTES}B/ma, cap {B}^{N}={cap:,}")
