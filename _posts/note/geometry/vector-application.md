# 向量應用

## 三點共線

<img width="300px" src="/images/geometry/vector-application/collinearity.png">

有三個點 $P_1$、$P_2$、$P_3$，我們想知道這三個點是否共線，顯而易見，隨便選一個點，作指向另外兩個點的向量，這兩個向量所夾的平行四邊形面積應該要是 $0$，所以，假設我們選的點是 $P_2$：
$$\overrightarrow{P_2P_1}\times\overrightarrow{P_2P_3}=0$$

```cpp=
template<typename T>
bool collinearity(pair<T, T> p1, pair<T, T> p2, pair<T, T> p3){
    return cross(p1, p2) * cross(p1, p3) == 0;
}
```

## 點是否在線段上

<img width="300px" src="/images/geometry/vector-application/inline.png">

有三個點 $A$、$B$ 和 $P$，我們想知道 $P$ 是否在 $\overline{AB}$ 上，顯然三個點必須共線，所以首要條件是：
$$\overrightarrow{PA}\times\overrightarrow{PB}=0$$

在確定共線後，我們還不能確定 $P$ 是否在 $\overline{AB}$ 上，所以我們還要判斷 $A$、$B$ 是否在 $P$ 的兩側，這時可以用內積：
$$\overrightarrow{PA}\cdot\overrightarrow{PB} \leq 0$$
$=0$ 的狀況會發生在 $P$ 是 $A$ 或 $B$ 的時候。

```cpp=
template<typename T>
bool inLine(pair<T, T> a, pair<T, T> b, pair<T, T> p){
    return collinearity(a, b, p) && dot(a - p, b - p) <= 0;
}
```

## 線段相交

有四個點 $A$、$B$、$C$、$D$，請檢查線段 $\overline{AB}$ 是否和線段 $\overline{CD}$ 相交。

分成幾種情況：

1. 交點不是任一線段的端點
2. 交點是其中一線段的端點或兩個線段的端點
3. 兩個線段重疊
4. 兩線段不相交且兩線段不共線
5. 兩線段不相交但兩線段共線

先講最間單的，交點不是任一線段的端點：
<img width="300px" src="/images/geometry/vector-application/intersect.png">

很顯然地，如果 $\overline{AB}$ 與 $\overline{CD}$ 相交，那麼點 $A$、$B$ 會分別在 $\overline{CD}$ 的兩側，而點 $C$、$D$ 也會分別落在 $\overline{AB}$ 的兩側。要判斷方向，外積就派上用場了：
$$(\overrightarrow{AB}\times\overrightarrow{AC})(\overrightarrow{AB}\times\overrightarrow{AD})<0$$
$$(\overrightarrow{CD}\times\overrightarrow{CA})(\overrightarrow{CD}\times\overrightarrow{CB})<0$$
這兩個條件都符合，就表示兩線段相交且交點不是任一線段的端點。

如果 $C$、$D$ 其中一點在 $\overline{AB}$ 上，那麼 $\overrightarrow{AB}\times\overrightarrow{AC}$ 和 $\overrightarrow{AB}\times\overrightarrow{AD}$ 其中一個應該要是 $0$，但是不能簡單地用 $(\overrightarrow{AB}\times\overrightarrow{AC})(\overrightarrow{AB}\times\overrightarrow{AD})=0$ 來判斷，因為會有其中一點和點 $A$、$B$ 共線但沒有交點的狀況，因此最好的方式是判斷有沒有哪個端點落在另一個線段上，這樣可以解決剩下的狀況。

```cpp=
template<typename T>
bool intersect(pair<T, T> a, pair<T, T> b, pair<T, T> c, pair<T, T> d){
    return (cross(b - a, c - a) * cross(b - a, d - a) < 0 && cross(d - c, a - c) * cross(d - c, b - c) < 0)
            || inLine(a, b, c) || inLine(a, b, d) || inLine(c, d, a) || inLine(c, d, b);
}
```

## 線段交點

在知道兩個線段相交後，可能還要進一步求交點（記得先把四點共線，也就是兩線段重疊的狀況判掉）。

<img width="300px" src="/images/geometry/vector-application/intersection.png">

$P$ 是兩線段交點，先令 $\overrightarrow{A}+i\overrightarrow{AB}=\overrightarrow{P}$，$i$ 是一個純量，接著我們知道 $\overrightarrow{P}-\overrightarrow{C}=\overrightarrow{A}+i\overrightarrow{AB}-\overrightarrow{C}$，而 $C$、$P$、$D$ 三點共線，因此：
$$\overrightarrow{CP}\times\overrightarrow{CD}=0$$
$$(\overrightarrow{A}+i\overrightarrow{AB}-\overrightarrow{C}) \times \overrightarrow{CD}=0$$
$$(\overrightarrow{A}-\overrightarrow{C}+i\overrightarrow{AB}) \times \overrightarrow{CD}=0$$
$$(\overrightarrow{CA}+i\overrightarrow{AB}) \times \overrightarrow{CD} =0$$
$$\overrightarrow{CA} \times \overrightarrow{CD} + i\overrightarrow{AB} \times \overrightarrow{CD} = 0$$
$$\overrightarrow{CA} \times \overrightarrow{CD} = -(i\overrightarrow{AB} \times \overrightarrow{CD})$$
$$\frac{\overrightarrow{CA}\times\overrightarrow{CD}}{\overrightarrow{CD}\times\overrightarrow{AB}}=i$$

把 $i$ 求出來後，$\overrightarrow{A}+i\overrightarrow{AB}$ 就是 $P$ 了。

```cpp=
template<typename T>
pair<T, T> intersection(pair<T, T> a, pair<T, T> b, pair<T, T> c, pair<T, T> d){
    assert(intersect(a, b, c, d));
    return a + cross(a - c, d - c) * (b - a) / cross(d - c, b - a);
}
```

## 凸多邊形包含測試

給一個凸多邊形和一個點，問這個點有沒有在這個凸多邊形裡。

先讓問題簡單一些：只考慮三角形就好。令三角形三個點為 $A$、$B$ 和 $C$，先選定 $A$，接著作向量 $\overrightarrow{AB}$、$\overrightarrow{AC}$，如果點 $P$ 在這個三角形內（邊上也算），那麼應該會滿足這個條件：
$$(\overrightarrow{AP} \times \overrightarrow{AB})(\overrightarrow{AP} \times \overrightarrow{AC}) \leq 0$$

也就是說，由 $\overrightarrow{AP}$ 的方向往 $\overrightarrow{AB}$ 和 $\overrightarrow{AC}$ 轉，應該要是不同向。而如果 $P$ 在 $\overline{AB}$ 或 $\overline{AC}$ 上，則上面那個式子會等於 $0$。

不過會滿足上面那個式子的 $P$ 範圍其實是下圖紅色部分，等於 $0$ 的話，$P$ 會在紅色邊上：

<img width="400px" src="/images/geometry/vector-application/inpoly1.png">

但如果選定三個點都做一次這個判定，上述那樣的範圍聯集後就會恰好是這個三角形的範圍了：

<img width="400px" src="/images/geometry/vector-application/inpoly2.png">

如果滿足 $(\overrightarrow{AP} \times \overrightarrow{AB})(\overrightarrow{AP} \times \overrightarrow{AC}) \leq 0$，那 $P$ 會在紅色區塊，等於 $0$ 是在紅色區塊邊界上；  
如果滿足 $(\overrightarrow{BP} \times \overrightarrow{BA})(\overrightarrow{BP} \times \overrightarrow{BC}) \leq 0$，那 $P$ 會在綠色區塊，等於 $0$ 是在綠色區塊邊界上；  
如果滿足 $(\overrightarrow{CP} \times \overrightarrow{CA})(\overrightarrow{CP} \times \overrightarrow{CB}) \leq 0$，那 $P$ 會在藍色區塊，等於 $0$ 是在藍色區塊邊界上。

從圖上可以看出來，滿足以上那三個式的地方只有三角形內而已。如果以上有任何一式等於 $0$，那麼 $P$ 會在這個三角形邊上。

把這個想法放到凸多邊形上，會發現：只要這個凸多邊形的每一頂點 $P_0$ 和它相鄰的兩個頂點 $P_1$ 和 $P_2$ 都滿足 $(\overrightarrow{P_0P} \times \overrightarrow{P_0P_1})(\overrightarrow{P_0P} \times \overrightarrow{P_0P_2}) \leq 0$ （相同地，等於 $0$ 就表示在邊界上），那麼 $P$ 就會在這個凸多邊形內。

```cpp
template<typename T>
T inPolygon(vector<pair<T, T>> polygon, pair<T, T> p){
    for(int i = 0; i < polygon.size(); i++)
        if(cross(p - polygon[i], polygon[(i - 1 + polygon.size()) % polygon.size()] - polygon[i]) *
           cross(p - polygon[i], polygon[(i + 1) % polygon.size()] - polygon[i]) > 0)
            return false;
    return true;
}
```

## 三角形面積

給一個三角形 $\triangle ABC$，求此三角形面積。

這有兩種常見作法，第一種是用 Heron's formula（$a$、$b$、$c$ 是三邊邊長）：
$$s=\frac{a+b+c}{2}$$
$$\triangle ABC=\sqrt{s(s-a)(s-b)(s-c)}$$

不過要這麼做，就得先把邊長算出來，開根號的過程中也很有可能出現誤差（當然如果題目給的是邊長而非頂點座標就只能這樣做）。

用向量的作法是，還記得外積的絕對值等同於兩向量夾的平形四邊形面積嗎？平行四邊形面積的一半就是三角形面積了，所以這樣就可以得到三角形面積：
$$\triangle ABC = \frac{|\overrightarrow{AB} \times \overrightarrow{AC}|}{2}$$

```cpp
template<typename T>
T triangleArea(pair<T, T> a, pair<T, T> b, pair<T, T> c){
    return abs(cross(b - a, c - a));
}
```

## 多邊形面積

給一個 $n$ 邊形 $P_0P_1P_2...P_{n-1}$（頂點按逆時針排序），求此多邊形面積。

要算多邊形面積，最直觀的方式就是把多邊形切成一堆三角形，這樣面積會好算很多，最簡單的作法是選一個共同頂點，然後以每兩個相鄰頂點為另外兩個點作三角形。在做這件事之前，得先選一個點作這些三角形的共同頂點，不過共同頂點是哪個點其實無所謂，因為外積的結果是「有向」的，只要將頂點逆時針排序，再選隨便一個共同頂點 $P$，那麼這個多邊形的面積就是（令 $P_n=P_0$）：

$$\frac{1}{2} \sum_{i=0}^{n-1} \overrightarrow{PP_i} \times \overrightarrow{PP_{i+1}}$$

舉例來說，以原點為共同頂點，下圖中紅色部分的面積是負的，而藍色是正的（注意有重疊）：
<img width="600px" src="/images/geometry/vector-application/area.png">

不管共同頂點在哪裡，都可以用這個方法算出正確的面積。

這個作法有個名字，叫測量師公式：

$$\frac{1}{2}\sum\left|\begin{array}{cc} 
    x_i & x_{i+1} \\
    y_i & y_{i+1} \\
\end{array}\right|=\frac{1}{2}\sum_{i=1}x_iy_{i+1}-y_ix_{i+1}$$

```cpp=
template<typename T>
T area(vector<pair<T, T>> p){
    T ans = 0;
    for(int i = 0; i < p.size(); i++) ans += cross(p[i], p[(i + 1) % p.size()]);
    return ans / 2;
}
```

# 練習題
- [TIOJ 1205](https://tioj.ck.tp.edu.tw/problems/1205) - 給你一堆點，求有幾個直角三角形
- [ZeroJudge d489](https://zerojudge.tw/ShowProblem?problemid=d489) - 給你三角形三邊長，求面積。
- [ZeroJudge d269](https://zerojudge.tw/ShowProblem?problemid=d269)/[UVa 11579](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2626) - 給你一堆邊長，求這些邊長可圍出的最大三角形
- [AtCoder ABC 139 F](https://atcoder.jp/contests/abc139/tasks/abc139_f) - 給你一堆向量，把其中一些加起來使得得到的向量長度最長