#!/usr/bin/env python3
"""Liet ke 1.000.000 mã dau cua codespace UTF-34 (3^34) -> 1 file .md.
Gia tri 0..999999 (mã UTF-34 thuan, KHONG gioi han Unicode).
Cot: dec | trit34(base-3) | bin68(2bit/trit 00/01/10) | hex7(packed 5trit/byte base-243)
"""
N_TRITS = 34
TRIT2BIN = {0:'00', 1:'01', 2:'10'}     # 11 = RESERVED
COUNT = 1_000_000

def fold34(v):
    t = []
    for _ in range(N_TRITS):
        t.append(v % 3); v //= 3
    return t                             # LSB-first, len 34
def pack_hex(t_lsb):                     # 34 trit + pad -> 7 byte base-243
    t = t_lsb + [0]                      # 35 = 7*5
    out = []
    for i in range(7):
        b = 0
        for x in reversed(t[i*5:i*5+5]): b = b*3 + x
        out.append(b)
    return bytes(out).hex()

with open('utf34_1M_binary.md', 'w') as f:
    f.write("# UTF-34 — 1.000.000 mã nhị phân đầu của codespace 3³⁴\n\n")
    f.write("Giá trị 0…999.999 trong codespace UTF-34 (3³⁴ = 16.677.181.699.666.569).\n")
    f.write("Đây là mã UTF-34 **thuần** — KHÔNG giới hạn Unicode (0x10FFFF). Sinh bằng chiết tích Fold base-3 + MIN-WASTE pack.\n\n")
    f.write("- `trit34` = 34 trit tam phân (Fold base-3, MSB-first), val = Σ dᵢ·3ⁱ\n")
    f.write("- `bin68`  = mã nhị phân thuần: mỗi trit → 2 bit (0=00 1=01 2=10; 11 RESERVED) = 68 bit\n")
    f.write("- `hex7`   = 7 byte đóng gói MIN-WASTE (5 trit/byte base-243), 56 bit\n\n")
    f.write("```\n")
    f.write(f"{'dec':>7} | {'trit34 (base-3, MSB-first)':<34} | {'bin68 (2-bit/trit)':<68} | hex7\n")
    f.write("-"*7 + "-+-" + "-"*34 + "-+-" + "-"*68 + "-+-" + "-"*14 + "\n")
    buf = []
    for v in range(COUNT):
        t_lsb = fold34(v)
        t_msb = t_lsb[::-1]
        trit34 = ''.join(map(str, t_msb))
        bin68  = ''.join(TRIT2BIN[x] for x in t_msb)
        hx     = pack_hex(t_lsb)
        buf.append(f"{v:>7} | {trit34} | {bin68} | {hx}")
        if len(buf) >= 20000:
            f.write("\n".join(buf) + "\n"); buf = []
    if buf: f.write("\n".join(buf) + "\n")
    f.write("```\n")
print("Da sinh 1.000.000 dong -> utf34_1M_binary.md")
