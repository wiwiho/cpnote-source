---
title: 快速冪
---
# 快速冪

要算 $a^n$，最暴力的方法就是乘 $n$ 次，不過這樣的時間複雜度是 $O(n)$，太慢了。

利用 $a^b \times a^c = a^{b+c}$ 的性質，我們可以把指數拆開，例如：
$$
\begin{align*}
13 &= 2^0 + 2^2 + 2^3 \\
a^{13} &= a^{2^0} \times a^{2^2} \times a^{2^3}
\end{align*}
$$

$a=a^{2^0}$ 乘上自己會得到 $a^{2^1}$、再乘自己會得到 $a^{2^2}$，每次指數都會變兩倍，只要做 $i$ 次就可以拿到 $a^{2^i}$ 了。因此，可以用這樣的方式在 $O(\log n)$ 的時間算出答案：

```cpp
const ll MOD = 1000000007;
ll fp(ll a, ll b){
    int ans = 1;
    while(b > 0){
        if(b & 1) ans = ans * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return ans;
}
```