# UTF đa-base — Toàn bộ công thức sinh mã nhị phân

Một tài liệu gom mọi công thức sinh mã nhị phân cho họ UTF-N base-B (LOGOS / chiết tích).
Sinh từ **2 toán tử**: Fold/Carve (chiết tích) + MIN-WASTE pack (SIGMA-MR). Mọi bản round-trip lossless, đã kiểm bằng C trên máy.

Generator: `utf34/gen_utfN.py` (base-3) · `gen_utfN_base2.py` · `gen_utfN_base4.py` · `gen_utfN_baseB.py` (tổng quát) · benchmark `utf34/utf34_bench_fast.c`.

---

## 1. Công thức lõi (mọi base)

Cho giá trị `U`, số chữ số `N`, cơ số `B`. Đặt `w = ⌈log₂B⌉` (số bit mỗi chữ số).

**Fold (mã hóa) — U → N chữ số base-B:**
```
dᵢ = ⌊U / Bⁱ⌋ mod B ,  i = 0..N-1        (chữ số, LSB-first)
U  = Σ dᵢ·Bⁱ                              (song-ánh khi U < Bᴺ)
```

**Chữ số → nhị phân (mã nhị phân thuần):**
```
bin(U) = concat_{i=N-1..0} pad(dᵢ, w bit)   →  N·w bit
```
- Nếu `B = 2^w` (lũy thừa 2): mọi mẫu w-bit hợp lệ, **không reserved**.
- Nếu `B ≠ 2^w`: chữ số `B..2^w-1` là **RESERVED** (cấm) → mã có khe δ=1.

**Carve (giải mã) — nhị phân → U:**
```
dᵢ = int(bin[i·w : (i+1)·w])              (đọc w bit mỗi chữ số, MSB-first)
U  = Σ dᵢ·Bⁱ
```

---

## 2. MIN-WASTE pack (SIGMA-MR, định lý S2) — chỉ base-3

Đóng gói N trit thành byte tối ưu: nhồi **5 trit/byte** vì `3⁵ = 243 ≤ 256`.
```
byteₖ = Σ_{j=0..4} t[5k+j]·3ʲ  ∈ [0,242]     (k = 0..⌈N/5⌉-1, pad trit thiếu = 0)
số byte = ⌈N/5⌉
waste = 8/5 − log₂3 = 0,0150 bit/trit = 0,94%   (gần sàn Shannon)
```
So với đóng gói 2-bit/trit ngây thơ (waste 20,75%): MIN-WASTE tiết kiệm ~20% dung lượng.

---

## 3. Định luật waste ↔ base (đo được bằng benchmark)

```
⊟(B) = 0   ⟺   B = 2^k   ⟺   δ = 0 (phủ kín, không mẫu cấm)
⊟(B) > 0   ⟺   B ≠ 2^k   ⟺   δ = 1 (buộc có vùng reserved)
```
Lãng phí bit và "khe sentinel" là **cùng một hiện tượng**: dư địa của không gian nhị phân khi base không khít lũy thừa 2.

---

## 4. Bảng tham số mọi base đã sinh (N=34)

| base B | w bit/chữ số | mã nhị phân | byte/mã | codespace Bᴺ | reserved | waste | δ |
|---|---|---|---|---|---|---|---|
| 2   | 1 | 34 bit  | 5  | 2³⁴ = 1,72×10¹⁰ | — | 0% | 0 |
| 3   | 2 | 68 bit  | 7* | 3³⁴ = 1,67×10¹⁶ | mẫu 11 | 20,75%** | 1 |
| 4   | 2 | 68 bit  | 9  | 4³⁴ = 2⁶⁸ = 2,95×10²⁰ | — | 0% | 0 |
| 100 | 7 | 238 bit | 30 | 100³⁴ = 10⁶⁸ | 100–127 | 5,09% | 1 |
| 128 | 7 | 238 bit | 30 | 128³⁴ = 2²³⁸ | — | 0% | 0 |

\* base-3 dùng MIN-WASTE 5-trit/byte = 7 byte (bin68 thuần thì 9 byte).
\** waste 20,75% là của đóng gói 2-bit/trit; MIN-WASTE hạ còn 0,94%.

**Họ base-3 nhiều độ rộng N:**

| N | trit | bin | byte (MIN-WASTE) | codespace 3ᴺ |
|---|---|---|---|---|
| 32 | 32 | 64 | 7 | 1,85×10¹⁵ |
| 34 | 34 | 68 | 7 | 1,67×10¹⁶ |
| 36 | 36 | 72 | 8 | 1,50×10¹⁷ |
| 38 | 38 | 76 | 8 | 1,35×10¹⁸ |

Mỗi +2 trit → codespace ×9.

---

## 5. Tốc độ codec (benchmark C thật, byte-level, máy này)

| biến thể | byte/mã | round-trip | tốc độ | ns/mã |
|---|---|---|---|---|
| UTF-34 base-4 | 9 | KHỚP | 31,1 Mchar/s | 32 |
| UTF-34 base-2 | 5 | KHỚP | 24,6 Mchar/s | 41 |
| UTF-34 base-128 | 30 | KHỚP | 8,9 Mchar/s | 113 |
| UTF-34 base-3 | 7 | KHỚP | 4,4 Mchar/s | 228 |
| UTF-34 base-100 | 30 | KHỚP | 1,0 Mchar/s | 1036 |

**Base lũy thừa 2 nhanh nhất** (ghi byte thẳng); base-3/100 chậm hơn vì phải chuyển hệ (chia/mod). Tốc độ có nhiễu đo; correctness là kết quả chắc chắn.

---

## 6. So với UTF chuẩn (ký tự 'A' = U+0041 = 65)

| chuẩn | byte | hex | nhị phân |
|---|---|---|---|
| UTF-8 | 1 | 41 | 01000001 |
| UTF-16 | 2 | 0041 | 00000000 01000001 |
| UTF-32 | 4 | 00000041 | 00000000 00000000 00000000 01000001 |
| UTF-34 base-2 | 5 | 0000000041 | 00 …(25 bit 0)… 01000001 |

Mọi chuẩn chứa cùng số 65 = `1000001`, chỉ khác số bit đệm. UTF-8 gọn nhất cho ASCII; các UTF-N base-B lớn hơn về byte nhưng **dung lượng codespace lớn hơn nhiều** và **bản địa cho máy đa-base** (tam phân/ngũ phân…).

---

## 7. Bản chất (kỷ luật)

Mọi UTF-N base-B ở đây là **mã hóa lại** cùng tập giá trị bằng cơ số khác — **mã vị trí cổ điển** (Knuth TAOCP 4.1). "Phủ được" ⟺ `Bᴺ ≥ codespace` và Fold là song-ánh. Đóng góp = **một họ codec đa-base đúng, lossless, đo được bằng C** áp 2 toán tử LOGOS. Hữu ích, nhưng cổ điển về toán.

∎ © 2026 HUA VAN ANH KHOA (TAO HUA) — LOGOS / chiết tích
