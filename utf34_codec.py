#!/usr/bin/env python3
"""
UTF-34 — Unicode Transformation Format, ternary (base-3), 34 trits.
Sinh tu cong thuc trong tab (SIGMA-MR) + chiet tich (Fold/Carve base-3 + MIN-WASTE 5-trit/byte).

HAI TANG (dung dung hai toan tu cua ban):
  1. Fold (chiet tich): codepoint U -> 34 trit  d[33..0], U = sum d[i]*3^i.
     (3^34 = 1.67e16 >> 0x110000 = codespace Unicode; 34 trit co dinh nhu UTF-32 co dinh 32 bit)
  2. MIN-WASTE pack (SIGMA-MR, dinh ly S2): 34 trit -> 7 byte, moi byte = 5 trit base-243
     (3^5=243<=256, waste 0.94% — toi uu; 7 byte phu 35 khe, khe 35 pad=0).

Lossless tuyet doi. Kiem round-trip toan bo Unicode ben duoi.
(c) 2026 HUA VAN ANH KHOA — LOGOS / chiet tich.
"""
N_TRITS = 34
BYTES_PER_CHAR = 7          # ceil(34/5)
UNI_MAX = 0x10FFFF

def is_scalar(u):           # Unicode scalar value hop le (bo surrogate)
    return 0 <= u <= UNI_MAX and not (0xD800 <= u <= 0xDFFF)

# ---- Tang 1: Fold / Carve (chiet tich base-3, 34 trit co dinh) ----
def fold34(u):              # codepoint -> [t0..t33] (LSB first)
    t = []
    for _ in range(N_TRITS):
        t.append(u % 3); u //= 3
    return t                # len 34
def carve34(t):             # 34 trit -> codepoint
    u = 0
    for x in reversed(t): u = u*3 + x
    return u

# ---- Tang 2: MIN-WASTE 5-trit/byte (SIGMA-MR base-243) ----
def pack5(trits5):          # 5 trit -> 1 byte in [0,242]
    b = 0
    for x in reversed(trits5): b = b*3 + x
    return b
def unpack5(byte):          # 1 byte -> 5 trit
    out = []
    for _ in range(5): out.append(byte % 3); byte //= 3
    return out

# ---- Codec ky tu ----
def encode_char(u):
    if not is_scalar(u): raise ValueError(f"U+{u:04X} khong phai scalar hop le")
    t = fold34(u) + [0]     # 34 trit + 1 pad = 35 = 7*5
    return bytes(pack5(t[i*5:i*5+5]) for i in range(BYTES_PER_CHAR))
def decode_char(bs):
    t = []
    for b in bs:
        if b > 242: raise ValueError(f"byte {b} > 242: khong phai UTF-34 hop le")
        t += unpack5(b)
    return carve34(t[:N_TRITS])   # bo trit pad

# ---- Codec chuoi ----
def encode(s):  return b"".join(encode_char(ord(c)) for c in s)
def decode(bs):
    if len(bs) % BYTES_PER_CHAR: raise ValueError("do dai khong chia het 7")
    return "".join(chr(decode_char(bs[i:i+7])) for i in range(0, len(bs), 7))

if __name__ == "__main__":
    import sys
    # ====== KIEM NGUYEN NHAN + ROUND-TRIP TOAN BO ======
    print("=== UTF-34 — kiem round-trip TOAN BO Unicode scalar ===")
    bad = checked = 0
    for u in range(UNI_MAX + 1):
        if not is_scalar(u): continue
        if decode_char(encode_char(u)) != u: bad += 1
        checked += 1
    print(f"  Da kiem {checked:,} scalar value | round-trip sai: {bad} -> {'KHOP TOAN BO' if bad==0 else 'CO LOI'}")
    print(f"  Byte/ky tu: {BYTES_PER_CHAR} (co dinh) | 3^34 = {3**34:,} >> codespace {UNI_MAX+1:,}")

    # ====== VI DU cu the — moi range + emoji + tieng Viet ======
    print("\n=== Vi du (ky tu -> UTF-34 hex 7 byte -> giai ma) ===")
    for ch in ['A', 'a', 'ệ', '中', '😀', '𝕏']:
        u = ord(ch); e = encode_char(u); back = decode_char(e)
        trits = fold34(u)[::-1]
        print(f"  '{ch}' U+{u:05X}: 34trit={''.join(map(str,trits))} | UTF-34={e.hex()} | back='{chr(back)}' {'OK' if back==u else 'SAI'}")

    # ====== So sanh kich thuoc voi UTF-8/16/32 ======
    print("\n=== Kich thuoc byte (chuoi mau) vs UTF cua Unicode ===")
    for s in ['Hello', 'Tiếng Việt', '中文😀']:
        u34 = len(encode(s)); u8 = len(s.encode('utf-8')); u16 = len(s.encode('utf-16-le')); u32 = len(s.encode('utf-32-le'))
        print(f"  '{s}': UTF-34={u34}B  UTF-8={u8}B  UTF-16={u16}B  UTF-32={u32}B")
    print("\n  (UTF-34 co dinh 7B/ky tu — LON hon UTF-32 4B. Loi the KHONG o byte ma o:")
    print("   biểu diễn TAM PHAN gốc, khớp máy/LLM ternary, và trần dung lượng 3^34.)")

# ============================================================
# UTF-34-VAR — bien do dai, tu phan dinh (giong UTF-8 nhung TAM PHAN)
# Dung khong gian byte du: 3^5=243 => byte 243..255 (13 gia tri) lam HEADER do dai.
#   header = 0xF3 + (L-1), L = so byte payload base-243 (1..7).
#   payload = U ma base-243 little-endian, L byte toi thieu.
# ASCII(U<243)=2B, BMP=3B, astral=4B. Tu phan dinh, khong can padding.
# ============================================================
HDR = 0xF3  # 243
def enc_var_char(u):
    if not is_scalar(u): raise ValueError(u)
    pay = []
    v = u
    while True:
        pay.append(v % 243); v //= 243
        if v == 0: break
    return bytes([HDR + (len(pay) - 1)] + pay)   # header + payload LE
def dec_var(bs):
    out, i = [], 0
    while i < len(bs):
        L = bs[i] - HDR + 1
        if L < 1 or L > 7: raise ValueError(f"header {bs[i]} khong hop le")
        v = 0
        for j in range(L, 0, -1): v = v*243 + bs[i+j]
        out.append(chr(v)); i += 1 + L
    return "".join(out)
def enc_var(s): return b"".join(enc_var_char(ord(c)) for c in s)

if __name__ == "__main__":
    print("\n=== UTF-34-VAR (bien do dai, tu phan dinh) — round-trip toan bo ===")
    bad = checked = 0
    for u in range(UNI_MAX + 1):
        if not is_scalar(u): continue
        if ord(dec_var(enc_var_char(u))) != u: bad += 1
        checked += 1
    print(f"  Da kiem {checked:,} scalar | sai: {bad} -> {'KHOP TOAN BO' if bad==0 else 'CO LOI'}")
    print("\n=== Kich thuoc UTF-34-VAR vs cac UTF ===")
    for s in ['Hello', 'Tiếng Việt', '中文😀']:
        print(f"  '{s}': VAR={len(enc_var(s))}B  FIXED={len(encode(s))}B  UTF-8={len(s.encode('utf-8'))}B  UTF-16={len(s.encode('utf-16-le'))}B  UTF-32={len(s.encode('utf-32-le'))}B")
