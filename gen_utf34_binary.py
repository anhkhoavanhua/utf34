#!/usr/bin/env python3
"""Sinh TOAN BO mã nhị phân UTF-34 cho moi Unicode scalar -> file du lieu rieng.
Cot: cp_hex  trit34(base3)  bin68(2bit/trit 00/01/10)  bin56(7byte packed)  fixed_hex7  var_hex
"""
import sys, gzip
sys.path.insert(0, '.')
import utf34_codec as u

TRIT2BIN = {0:'00', 1:'01', 2:'10'}   # 11 = RESERVED (khong dung)

def row(cp):
    t_lsb = u.fold34(cp)              # 34 trit LSB-first
    t_msb = t_lsb[::-1]              # MSB-first (dang doc)
    trit34 = ''.join(map(str, t_msb))
    bin68  = ''.join(TRIT2BIN[x] for x in t_msb)     # 34*2 = 68 bit, 11 reserved
    fx     = u.encode_char(cp)                        # 7 byte packed
    bin56  = ''.join(f'{b:08b}' for b in fx)          # 56 bit
    var    = u.enc_var_char(cp)
    return f"U+{cp:05X}\t{trit34}\t{bin68}\t{bin56}\t{fx.hex()}\t{var.hex()}"

out = gzip.open('utf34_full_binary.tsv.gz', 'wt')
out.write("cp\ttrit34_base3\tbin68_2bit_per_trit\tbin56_packed7byte\tfixed_hex7\tvar_hex\n")
n = 0
for cp in range(u.UNI_MAX + 1):
    if not u.is_scalar(cp): continue
    out.write(row(cp) + "\n"); n += 1
out.close()
print(f"Da sinh {n:,} dong mã nhị phân UTF-34 -> utf34_full_binary.tsv.gz")
