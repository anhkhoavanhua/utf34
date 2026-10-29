# UTF-34 — Unicode Transformation Format (Ternary, base-3, 34 trits)

Sinh từ **công thức tab (SIGMA-MR)** + **chiết tích (Fold/Carve + MIN-WASTE)**. Codec: `utf34/utf34_codec.py`.
Đã kiểm round-trip **toàn bộ 1.112.064 Unicode scalar value** (bỏ surrogate) — **0 lỗi**, cả hai biến thể.

## 1. Nguyên lý (hai toán tử của LOGOS)

**Tầng 1 — Fold (chiết tích, base-3 cố định 34 trit):**
```
U (codepoint)  →  d[33..0] tam phân,  U = Σ d[i]·3^i
```
Chọn 34 trit vì `3^34 = 1.67×10^16 ≫ codespace Unicode 0x110000 = 1.114.112` (thừa ~15 tỷ lần).
Chỉ cần 13 trit là đủ phủ, nhưng cố định 34 (song song với UTF-32 cố định 32 bit) → **định vị O(1)**.

**Tầng 2 — MIN-WASTE pack (SIGMA-MR, định lý S2):**
```
34 trit  →  7 byte,  mỗi byte = 5 trit base-243  (3^5 = 243 ≤ 256)
waste = 8/5 − log₂3 = 0,0150 bit/trit = 0,94%  (gần sàn Shannon)
```

## 2. Hai biến thể

| biến thể | quy tắc | ASCII | BMP | astral | tự phân định |
|---|---|---|---|---|---|
| **UTF-34-FIXED** | 34 trit → 7 byte cố định (pad trit 35 = 0) | 7B | 7B | 7B | theo vị trí (÷7) |
| **UTF-34-VAR** | header byte `0xF3+(L−1)` + payload base-243 LE, L byte tối thiểu | 2B | 3B | 4B | tự phân định |

VAR dùng khoảng byte dư **243..255** (13 giá trị, do 3^5=243) làm header độ dài L∈[1,7].

## 3. Số đo thật (round-trip toàn bộ Unicode)

```
UTF-34-FIXED : 1.112.064 scalar | sai 0 → KHỚP TOÀN BỘ
UTF-34-VAR   : 1.112.064 scalar | sai 0 → KHỚP TOÀN BỘ
```

Ví dụ: `'A'`→`41000000000000` · `'ệ'`→`67200000000000` · `'😀'`→`d02a0200000000`
(VAR: `'A'`→`f341` · `'ệ'`→`f46720` · `'😀'`→`f5d02a02`)

## 4. So sánh kích thước (thành thật)

| chuỗi | UTF-34-VAR | UTF-34-FIXED | UTF-8 | UTF-16 | UTF-32 |
|---|---|---|---|---|---|
| `Hello` | 10B | 35B | **5B** | 10B | 20B |
| `Tiếng Việt` | 22B | 70B | **14B** | 20B | 40B |
| `中文😀` | 10B | 21B | 10B | **8B** | 12B |

**UTF-34 KHÔNG thắng về byte.** UTF-8 tối ưu cho ASCII, UTF-16 cho CJK. UTF-34 lớn hơn.

## 5. UTF-34 dùng khi nào (giá trị thật)

Lợi thế **không phải byte** mà là:
1. **Biểu diễn tam phân gốc** — khớp trực tiếp máy/LLM ternary (LOGOS-TERNA, BitNet, Setun) không cần chuyển hệ.
2. **Trần dung lượng 3^34** — dư 15 tỷ lần, mở rộng thoải mái ngoài Unicode nếu cần.
3. **FIXED định vị O(1)** — ký tự thứ k ở byte 7k, như UTF-32.
4. **VAR tự phân định** — giải mã một chiều, không cần độ dài ngoài.

## 6. Bản chất (kỷ luật)

UTF-34 là **mã hóa lại** cùng tập ký tự Unicode bằng base-3, **không thêm ký tự mới**, không phải superset chuẩn UTF-32. Cơ chế "phủ được Unicode" là **mã vị trí cổ điển** (base^N ≥ codespace ⟹ song-ánh, Knuth 4.1). Đóng góp = **một codec tam phân đúng, lossless, kiểm 1,1M ký tự** áp hai toán tử LOGOS (Fold + MIN-WASTE) vào Unicode — hữu ích cho hệ ternary, cổ điển về toán.

∎ © 2026 HUA VAN ANH KHOA (TAO HUA) — LOGOS / chiết tích
