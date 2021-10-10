---
title: 歐幾里得演算法
---
# 歐幾里得演算法

歐幾里德演算法也叫輾轉相除法，用來求 $\gcd(a,b)$，它運用了一個性質：

> 對於 $a \geq b$，$\gcd(a,b)=\gcd(a-b,b)$（$\gcd(a,0)=a$）。
> 
> Proof.  
> $d \mid a \land d \mid b \iff d \mid (a-b) \land d \mid b$，所以 $a$、$b$ 的公因數和 $a$、$a-b$ 是一樣的。

從這個性質可以推出 $\gcd(a,b)=\gcd(a-b,b)=\gcd(a-2,b)=\dots=\gcd(b, a \bmod b)$，遞迴直到 $\gcd(a,0)=a$。

因為 $a \bmod b \leq \frac{a}{2}$，所以每過兩次 $a$ 會變小至少一半（$\gcd(a,b)=\gcd(b, a \bmod b) = \gcd(a \bmod b, b \bmod (a \bmod b))$），得出這個演算法的時間複雜度是 $O(\log \max(a,b))$。

```cpp
int gcd(int a, int b){
    while(b > 0){
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
```

實作上可以用迴圈，常數比較小，不過在 C++ 裡不用自己寫，可以用 `__gcd(a,b)`。

## 擴展歐幾里德演算法

擴展歐幾里德演算法用來求 $ax+by=c$ 的整數解。

> 貝祖定理：
>
> 對於整數 $a,b,c$，$ax+by=c$ 有解若且唯若 $\gcd(a,b) \mid c$。

由此可知只要 $c$ 不是 $\gcd(a,b)$ 的倍數就無解。有解的話，令 $g=gcd(a,b)$，可以先找 $ax+by=g$ 的解，擴展歐幾里德演算法的作法是嘗試從輾轉相除法的遞迴式，做出一個長得差不多的式子：

$$\begin{align*}
    ax+by & =\gcd(a,b) \\
    & = \gcd(b, a \bmod b) \\
    & = \gcd(b, a - \lfloor \frac{a}{b} \rfloor b) \\
    & = bx' + (a - \lfloor \frac{a}{b} \rfloor b)y' \\
    & = ay' + b(x' - \lfloor \frac{a}{b} \rfloor y)
\end{align*}$$

得出 $x=y'$、$y=x' - \lfloor \frac{a}{b} \rfloor y'$，所以先求 $x',y'$ 就可以算出 $x,y$，終止條件一樣是當 $b=0$ 時，回傳 $(1,0)$ 即可。

```cpp
pii exgcd(int a, int b){
    if(b == 0) return mp(1, 0);
    pii ans = exgcd(b, a % b);
    return mp(ans.S, ans.F - a / b * ans.S);
}
```

最後得到的答案只要乘上 $\frac{c}{g}$ 倍，就可以變成 $ax+by=c$ 的答案。

### 其他的解

擴展歐幾里德演算法只會拿到其中一組解。先來看看兩組解會有什麼關係：有兩組整數解 $(x_1,y_1)$、$(x_2,y_2)$，我們知道

$$ax_1+by_1=ax_2+by_2 \implies \frac{a}{g}(x_1-x_2) = \frac{b}{g}(y_2-y_1)$$

因為 $\frac{a}{g}$ 和 $\frac{b}{g}$ 互質，因此 $x_1-x_2 = k\frac{b}{g}$、$y_2-y_1 = k\frac{a}{g}$，也就是說有了一組解 $(x,y)$ 後，其他解都可以寫成 $(x+k\frac{b}{g}, y-k\frac{a}{g})$，$k \in \mathbb{Z}$。

### 負數的狀況

這裡有一些小小細節，因為係數常常有可能是負的，所以特別討論一下負數的狀況。在上面的式子裡面，寫的都是 $a \bmod b = a - \lfloor\frac{a}{b}\rfloor b$，但是程式碼裡的 `a % b` 實際上是 `a - a / b * b`，而 `a / b` 是向零取整而非向下取整。在不同的除法（向下、向下、向零）定義下，`gcd(a,b)` 給出的結果正負會不一樣。

要避免這個問題發生，就要確保 `gcd` 和 `exgcd` 的遞迴過程完全一樣。如果好好照上面那樣寫，並且算 $\gcd$ 用的是 `__gcd` 就不會出任何問題，但是如果你在 `exgcd` 不小心把 `a / b` 變成向下取整，還繼續用 `__gcd` 就會出事了。

如果不喜歡有負數的話，可以把負號移到變數上，例如 $-3x+y=1$ 可以變成 $3(-x)+y=1$。

### 解的範圍

另外還有溢位的問題，事實上可以不用擔心運算過程發生溢位。因為貝祖定理其實還告訴我們：

> 一定存在恰兩組整數解 $(x,y)$ 滿足 $\lvert x \rvert \leq \lvert \frac{b}{g} \rvert$、$\lvert y \rvert \leq \lvert \frac{a}{g} \rvert$，而且擴展歐幾里德演算法得出的是其中一組。

所以不只可以知道運算過程數字都會保持在一個範圍內，而且還可以知道如果你想要拿到最小正數解之類的，只要把得到的解移動幾次就可以了。