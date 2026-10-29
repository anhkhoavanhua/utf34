# UTF-34 & Multi-base Binary Codespace

Tập hợp mã nhị phân và công thức cho họ **UTF-N đa-base** (LOGOS / Chiết tích · Ptyctics).
Sinh từ 2 toán tử nền tảng: **Fold $\oslash$ / Carve $\ominus$** (Chiết tích) + **MIN-WASTE pack** (SIGMA-MR). Mọi bản round-trip lossless, đã kiểm chứng bằng C99.

---

## 1. Dữ liệu: `utf34_base4_1M_binary.md` (1.000.000 mã đầu tiên)

* **Tệp dữ liệu:** [`utf34_base4_1M_binary.md`](./utf34_base4_1M_binary.md) *(quản lý qua Git LFS, dung lượng ~137 MB)*
* **Dải giá trị:** $0 \dots 999.999$ trong codespace UTF-34 base-4:
  $$4^{34} = 2^{68} = 295.147.905.179.352.825.856$$
* **Định luật Waste:** Vì $\text{base} = 4 = 2^2$ (lũy thừa của 2) nên **$\partial W = 0$** (Waste = 0, phủ kín, không có mẫu cấm/reserved).
* **Cấu trúc trường:**
  * `dec`: Giá trị thập phân ($0 \dots 999.999$)
  * `quad34`: 34 chữ số base-4 ($0, 1, 2, 3$; MSB-first), $\text{val} = \sum d_i \cdot 4^i$
  * `bin68`: Mã nhị phân thuần: mỗi digit $\to$ 2 bit ($0=00, 1=01, 2=10, 3=11$) = 68 bit
  * `hex9`: 9 byte (72 bit, pad 4 bit cao)

---

## 2. Bảng tham số các base (N=34)

| Base $B$ | $w$ (bit/digit) | Mã nhị phân | Byte/mã | Codespace $B^N$ | Reserved | Waste | $\delta$ |
|---|---|---|---|---|---|---|---|
| **2** | 1 | 34 bit | 5 | $2^{34} \approx 1,72 \times 10^{10}$ | — | 0% | 0 |
| **3** | 2 | 68 bit | 7* | $3^{34} \approx 1,67 \times 10^{16}$ | mẫu `11` | 20,75%** | 1 |
| **4** | 2 | 68 bit | 9 | $4^{34} = 2^{68} \approx 2,95 \times 10^{20}$ | — | 0% | 0 |
| **100** | 7 | 238 bit | 30 | $100^{34} = 10^{68}$ | 100–127 | 5,09% | 1 |
| **128** | 7 | 238 bit | 30 | $128^{34} = 2^{238}$ | — | 0% | 0 |

*\* base-3 dùng MIN-WASTE 5-trit/byte = 7 byte (bin68 thuần thì 9 byte).*  
*\*\* waste 20,75% là của đóng gói 2-bit/trit; MIN-WASTE hạ còn 0,94%.*

---

## 3. Tốc độ Codec (Benchmark C99 thực tế)

| Biến thể | Byte/mã | Round-trip | Tốc độ | ns/mã |
|---|---|---|---|---|
| **UTF-34 base-4** | 9 | KHỚP | **31,1 Mchar/s** | 32 |
| **UTF-34 base-2** | 5 | KHỚP | **24,6 Mchar/s** | 41 |
| **UTF-34 base-128** | 30 | KHỚP | **8,9 Mchar/s** | 113 |
| **UTF-34 base-3** | 7 | KHỚP | **4,4 Mchar/s** | 228 |
| **UTF-34 base-100** | 30 | KHỚP | **1,0 Mchar/s** | 1036 |

---

## 4. Tài liệu liên quan

* [`utf-multibase-binary-formulas.md`](./utf-multibase-binary-formulas.md): Toàn bộ công thức toán học sinh mã nhị phân cho họ UTF đa-base.
* [`gen_utf34_binary.py`](./gen_utf34_binary.py): Script sinh dữ liệu.

---

∎ © 2026 HUA VAN ANH KHOA (TAO HUA) — LOGOS / Chiết tích (Ptyctics)
