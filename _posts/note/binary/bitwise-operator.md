---
title: 位元運算
---
# 位元運算

位元運算就是對二進位的 `0` 和 `1` 做一些處理，然後會有一些很神奇的性質和用途。

## bool 運算

`bool` 只有 `true` 跟 `false`，然後可以對它們做一些運算：

| |符號|C++|
|--|------|-----|
|AND| $\land$ | `a && b` |
|NOT| $\lnot$ | `!a` |
|OR| $\lor$ | `a || b` |
|XOR| $\oplus$ | `a != b` |

其中比較奇怪的東西是 xor 在兩個運算元中有恰一個是 `true` 時，結果是 `true`，反之就是 `false`。你可能會想蛤 `!=` 不是不等於嗎，其實只有兩個運算元的 xor 就是不等於的意思。（有時候會遇到超過兩個東西一起 xor，這個時候 XOR 的定義是有奇數個是 `true` 時結果為 `true`。）

## 位元運算

進入正題，除了 `bool` 可以做以上那些運算以外，`int`、`long long` 這樣的整數型態也可以做這些運算，做法就是每個位元分別做運算，例如：

$(100110)_2$ 和 $(011000)_2$ 做 or 運算會是：

|bit|5|4|3|2|1|0|
|-|-|-|-|-|-|-|
|A|1|0|0|1|1|0|
|B|0|1|1|0|0|0|
|ANS|1|1|1|1|1|0|

這叫做 bitwise operation。

以下是 C++ 的位元運算子列表：

| |運算子| 說明 |
|-|-----|-----|
|AND|`A & B`| bitwise and|
|OR|`A | B`| bitwise or|
|XOR| `A ^ B` | bitwise xor|
|左移| `A << n` | 將 A 的每個位元左移 $n$ 位，右方補 `0` |
|右移| `A >> n` | 將 A 的每個位元右移 $n$ 位，右方補 `0` 或 `1` 依 A 本來的最高位決定 |
|NOT| `~A` | bitwise not，將 A 為 `0` 的位元換成 `1`，為 `1` 換成 `0`，也就是取補數 |

一些範例：

- 要判斷一個數 $A$ 的右方數來第 $n$ 位是 `0` 還是 `1`：
    ```cpp
    A & (1 << n) //>0 的話為 1，否則為 0
    ```
- 把一個數 $A$ 用很怪的方式換成相反數：
    ```cpp
    ~A+1
    ```
- 把 $A$ 除了最低位的 `1` 以外的 `1` 都換成 `0`：
    ```cpp
    A & -A
    ```
- 乘以 2 和除以 2
    ```cpp
    a <<= 1 // a *= 2
    a >>= 1 // a /= 2
    ```
    
### Bitwise xor

因為 xor 太多常用性質，所以特別拿出來講。先來幾個基本原則：

- $A \oplus B = B \oplus A$，$(A \oplus B) \oplus C = A \oplus (B \oplus C)$，也就是有交換律和結合律。
- $A \oplus A = 0$
- 若 $A \oplus B = C$，則 $A \oplus C = B$
- $A \oplus 0 = A$

這些只要稍微想一下就可以得出來了，如果覺得很難想，可以先用只有一個 bit 的狀況來想，反正每一個位元互不干擾。

舉例來說，把兩個變數 `a`、`b` 互換可以這樣做：
```cpp
a = a ^ b;
b = a ^ b;
a = a ^ b;
```

> 稍微解釋一下，若 `a`、`b` 的原始值分別為 $a_0$、$b_0$，新值為 $a_1$、$b_1$，那麼：  
> 設 $t = a_0 \oplus b_0$  
> $b_1 = t \oplus b_0 = a_0 \oplus b_0 \oplus b_0 = a_0$  
> $a_1 = t \oplus b_1 = a_0 \oplus b_0 \oplus a_0 = b_0$

可以發現到在做 xor 時，每個人都是自己的反元素，因為 $A \oplus A = 0$，既然如此，就可以拿去做前綴 xor：
$$S_l \oplus S_{l + 1} \oplus \dots \oplus S_{r - 1} \oplus S_r = (S_1 \oplus S_2 \oplus \dots \oplus S_{r - 1} \oplus S_r) \oplus (S_1 \oplus S_2 \oplus \dots \oplus S_{l - 2} \oplus S_{l - 1})$$
