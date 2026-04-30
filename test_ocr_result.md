The user wants a high-fidelity OCR conversion of the provided image into structured Markdown.
The image is a page from a Vietnamese textbook about percentages (Tỉ số phần trăm).

- Header: "Bài 56 TỈ SỐ PHẦN TRĂM"
- Illustration: A grandmother and a child in a chicken coop.
    - Child's speech bubble: "Bà ơi! Trong đàn gà, số gà trống luôn ít hơn số gà mái."
    - Grandmother's speech bubble: "Số gà trống thường chiếm khoảng *mười hai phần trăm* số con gà của cả đàn."
- Section: "Giới thiệu Tỉ số phần trăm"
    - Example (Ví dụ): "Đàn gà có 100 con, trong đó có 12 con gà trống. Tỉ số của số con gà trống và số con gà cả đàn là:"
    - Calculation: $12 : 100$ hay $\frac{12}{100}$
    - Formula: $\frac{12}{100} = 12\%$
    - Reading: "đọc là: *mười hai phần trăm*."
    - Statement: "Ta nói: *Tỉ số phần trăm* của số con gà trống và số con gà cả đàn là $12\%$; hay: Số con gà trống chiếm $12\%$ số con gà của cả đàn."
- Exercise section:
    - Number 1 marker: Blue triangle with "1".
    - Text: "Thực hiện theo mẫu. Có 100 hộp nước trái cây các loại (mỗi ô vuông nhỏ thể hiện một hộp). Viết tỉ số phần trăm của số hộp nước trái cây mỗi loại và tổng số hộp."
    - Image: A grid with colored areas representing different juices:
        - Nước ổi (guava juice): Yellow area (top left).
        - Nước dâu (strawberry juice): Pink area (right side).
        - Nước nho (grape juice): Purple area (middle left).
        - Nước cam (orange juice): Orange/Yellow area (bottom).
    - Example (Mẫu):
        - $\text{Nước ổi: } \frac{10}{100} = 10\%$
        - Speech bubble: "Số hộp nước ổi chiếm $10\%$ tổng số hộp nước trái cây."
    - Questions to answer:
        - a) Nước nho.
        - b) Nước dâu.
        - c) Nước cam.
- Footer: Page number "7".

- Use # for the main title.
- Use ## for the "Giới thiệu" section.
- Use LaTeX for fractions and percentages.
- Keep the bold and italic styles.
- Organize as clean Markdown.

- "TỈ SỐ PHẦN TRĂM"
- "Bà ơi! Trong đàn gà, số gà trống luôn ít hơn số gà mái."
- "Số gà trống thường chiếm khoảng mười hai phần trăm số con gà của cả đàn."
- "Giới thiệu Tỉ số phần trăm"
- "Ví dụ: Đàn gà có 100 con, trong đó có 12 con gà trống. Tỉ số của số con gà trống và số con gà cả đàn là:"
- $12 : 100$ hay $\frac{12}{100}$
- "Ta viết: $\frac{12}{100} = 12\%$ đọc là: *mười hai phần trăm*."
- "Ta nói: *Tỉ số phần trăm* của số con gà trống và số con gà cả đàn là $12\%$; hay: Số con gà trống chiếm $12\%$ số con gà của cả đàn."
- "1 Thực hiện theo mẫu. Có 100 hộp nước trái cây các loại (mỗi ô vuông nhỏ thể hiện một hộp). Viết tỉ số phần trăm của số hộp nước trái cây mỗi loại và tổng số hộp."
- "Mẫu: Nước ổi: $\frac{10}{100} = 10\%$"
- "Số hộp nước ổi chiếm $10\%$ tổng số hộp nước trái cây."
- "a) Nước nho."
- "b) Nước dâu."
- "c) Nước cam."

Check diacritics carefully.
- "Tỉ số phần trăm" - correct.
- "mười hai phần trăm" - correct.
- "nước trái cây" - correct.

Final check of the image elements:
- There's a grid for the example of 12% (12 green squares in a 10x10 grid).
- There's a grid for the exercise.
    - Nước ổi: 2 columns x 5 rows = 10 squares (10%) -> matches sample.
    - Nước nho: 2 columns x 5 rows = 10 squares (10%).
    - Nước dâu: 5 columns x 8 rows? No, wait. Let's look closer.
    - Grid is 10x10.
    - Nước ổi: Top left, 2x5 block = 10.
    - Nước nho: Middle left, 2x5 block = 10.
    - Nước dâu: Top right, 8x8 block? No, it's 8 columns wide and 8 rows high? No, it's the remaining space on the right.
    - Actually, looking at the image:
        - Yellow (Ổi): top left $2 \times 5$.
        - Purple (Nho): middle left $2 \times 5$.
        - Pink (Dâu): right side $8 \times 8$? Wait, let's count. Total grid is $10 \times 10$.
        - Bottom orange (Cam): $10 \times 2$ = 20 squares.
        - Pink (Dâu) seems to be $8 \times 8 = 64$? No, the height of Oii + Nho is 10. But there's Cam at the bottom.
        - Let's re-examine the grid:
            - Total height is 10.
            - Bottom orange "Nước cam" is 2 rows high. So the remaining height is 8.
            - Top left yellow "Nước ổi" is 2 cols wide, 5 rows high? No, if Cam is 2, and the rest is 8. Oii is 4 rows? Let's count the small squares.
            - Bottom block (Cam): 10 wide, 2 high = 20.
            - Top section is 8 high.
            - Left side: Oii is $2 \times 4 = 8$? No, it looks like 5 rows. Let's count.
            - Let's count cells:
                - Cam: $10 \times 2 = 20$.
                - Oii: $2 \times 4 = 8$.
                - Nho: $2 \times 4 = 8$.
                - Dâu: $8 \times 8 = 64$.
                - $20 + 8 + 8 + 64 = 100$. Yes.
                - Wait, the example says "Nước ổi: 10/100 = 10%".
                - Let's re-count Oii cells. $2 \times 5 = 10$.
                - If Oii is $2 \times 5$ and Nho is $2 \times 5$, that's $10 + 10 = 20$.
                - Then the height for the top section is 10? But there is a bottom section.
                - Let's look at the grid again.
                - Bottom orange area is 2 units high.
                - The remaining height is 8 units.
                - If Oii is 10 cells, and it's 2 cells wide, it must be 5 units high.
                - If Nho is also 2 cells wide and 5 units high, that's $5+5 = 10$ height.
                - But total height is $8 (\text{top}) + 2 (\text{bottom}) = 10$.
                - Maybe Oii is $2 \times 5 = 10$ and Nho is $2 \times 3 = 6$?
                - Let's look at the purple area. It looks slightly shorter than the yellow area.
                - Yellow: 5 rows.
                - Purple: 3 rows.
                - $5 + 3 = 8$ rows. Perfect.
                - Then Pink (Dâu) is $8 \times 8 = 64$ cells.
                - Orange (Cam) is $10 \times 2 = 20$ cells.
                - Total: $10 + 6 + 64 + 20 = 100$.
                - Wait, let's re-read the Oii count. The "Mẫu" says $10/100 = 10\%$. So Oii is definitely 10.
                - Let's re-count the purple (Nho). It looks like 3 rows. $2 \times 3 = 6$.
                - Let's re-count the pink (Dâu). 8 columns, 8 rows. $8 \times 8 = 64$.
                - Orange (Cam). 10 columns, 2 rows. $10 \times 2 = 20$.
                - $10 + 6 + 64 + 20 = 100$.
                - However, for the OCR task, I don't need to solve the problem, just transcribe the text. The user wants a conversion of the content, not the answers to the exercise.

- Header: # Bài 56 TỈ SỐ PHẦN TRĂM
- Dialogues:’ Use a format that reflects the speech bubbles.
- Introduction: ## Giới thiệu Tỉ số phần trăm
- Example: **Ví dụ:** ...
- Math: $\frac{12}{100} = 12\%$
- Exercise: ### 1. Thực hiện theo mẫu...
- Sample: **Mẫu:** ...
- List: a), b), c).

Let's execute.
# Bài 56 TỈ SỐ PHẦN TRĂM

**Bà ơi! Trong đàn gà, số gà trống luôn ít hơn số gà mái.**
**Số gà trống thường chiếm khoảng *mười hai phần trăm* số con gà của cả đàn.**

## Giới thiệu Tỉ số phần trăm

**Ví dụ:** Đàn gà có 100 con, trong đó có 12 con gà trống. Tỉ số của số con gà trống và số con gà cả đàn là:
$$12 : 100 \text{ hay } \frac{12}{100}$$
Ta viết: $\frac{12}{100} = 12\%$ đọc là: *mười hai phần trăm*.

Ta nói: *Tỉ số phần trăm* của số con gà trống và số con gà cả đàn là $12\%$; hay: Số con gà trống chiếm $12\%$ số con gà của cả đàn.

***

### 1. Thực hiện theo mẫu.
Có 100 hộp nước trái cây các loại (mỗi ô vuông nhỏ thể hiện một hộp). Viết tỉ số phần trăm của số hộp nước trái cây mỗi loại và tổng số hộp.

*(Hình ảnh minh họa: Một lưới $10 \times 10$ ô vuông chia thành 4 vùng màu: Nước ổi (vàng), Nước nho (tím), Nước dâu (hồng) và Nước cam (cam).)*

**Mẫu:**
$\text{Nước ổi: } \frac{10}{100} = 10\%$
$\rightarrow$ Số hộp nước ổi chiếm $10\%$ tổng số hộp nước trái cây.

a) Nước nho.
b) Nước dâu.
c) Nước cam.

7