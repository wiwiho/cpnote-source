---
title: 最長迴文子字串
---
# 最長迴文子字串（Longest Palindromic Substring, LPS）

給一個字串 $S$，求 $S$ 中最長的為迴文的子字串長度。

## Manacher's Algorithm

為了方便，接下來的索引值都是從 0 開始，也就是說，$S$ 的第一個字元是 $S_0$。

首先，先求出以每個字元為中心點的最長迴文長度，但偶數長度的迴文沒有中心點，所以這邊做一個操作：在每個字元中間和 $S$ 兩端加上一個 $S$ 中沒有的字元 $c$，結果會是：$c S_0 c S_1 c S_2 c S_3 ... S_{|S|-1} c$。

這個加工過的字串為 $T$，長度是 $2 \times |S| + 1$，可以用一個簡單的方式來得到 $T_i$：
$$
T_i = 
    \begin{cases}
        S_{\lfloor \frac{i}{2} \rfloor} &\quad \text{if }i \bmod 2 = 1 \\
        c &\quad \text{else}
    \end{cases}
$$
接下來的程式碼會用 $c$ 為 `.` 作為範例。
```cpp
#define T(x) ((x) % 2 ? s[(x) / 2] : '.')
```

接下來，我們用 $R_i$ 來表示以 $T_i$ 為中心點的最長迴文半徑（含中心點）。再來的重點是要如何快速求出 $R_i$，先從 $T$ 的左邊讀到右邊，並且一邊計算 $R_i$ 為何。

令 $\text{mx}$ 為目前為止，我們找到的迴文子字串的**最右邊的結尾**，也就是：$\max \{i+R_i-1\}$，而 $\text{center}$ 為這個**結尾在最右邊**的迴文子字串的中心點，也就是：$\text{mx}=\text{center}+R_\text{center}-1$。

先寫一個 function 來方便等等的計算，$\text{ex}(l,r)$ 表示從 $l$ 往左和 $r$ 往右的最長對稱字串長度，也就是說：令 $t=\text{ex}(l,r)$，$T_{(l-t+1)..l}=T_{r..(r+t-1)}$，且 $t$ 盡可能地大。
```cpp
int ex(int l, int r){
    int i = 0;
    while(l - i >= 0 && r + i < n && T(l - i) == T(r + i)) i++;
    return i;
}
```

如果我們已經算好了前 $i-1$ 項，現在要算第 $i$ 項，我們會遇到幾種狀況：  

- $T_i$ 沒有被任何中心點在前面的迴文覆蓋（$i > \text{mx}$）  
    在這樣的情況下，我們不能用先前算好的東西來得到 $R_i$，所以只能硬算：
    ```cpp
    r[i] = ex(i, i);
    center = i;
    mx = i + r[i] - 1;
    ```
- $T_i$ 有被中心點在前面的迴文覆蓋（$i \leq \text{mx}$）  
    如果這樣的話，我們可以利用覆蓋 $T_i$ 的迴文另一邊的對稱字串來得到 $R_i$。令 $i'$ 為迴文另一邊的對稱點，也就是說：$i'=\text{center}-(i-\text{center})$，接著我們令 $\text{len}$ 為 $T_i$ 到這個迴文結尾的長，也就是 $\text{len}=\text{mx}-i+1$。再來又分成了幾種情況：
    - 以 $T_{i'}$ 為中心的最長迴文剛好貼齊以 $T_{\text{center}}$ 為中心的迴文邊界（$R_{i'}=\text{len}$）  
        這樣子我們只能確保 $R_i \geq R_{i'}$，因為我們並不知道 $T_i+R_{i'}$ 是否等於 $T_i-R_{i'}$，所以只好接著算：$R_i=R_{i'}+\text{ex}(i-R_{i'}, i+R_{i'})$。
    - 以 $T_{i'}$ 為中心的最長迴文在 $T_{\text{center}}$ 為中心的迴文範圍以內（$R_{i'}<\text{len}$）  
        這樣我們直接確定 $R_i=R_{i'}$ 了，因為以 $T_{\text{center}}$ 為中心的迴文兩邊是對稱的。
    - 以 $T_{i'}$ 為中心的最長迴文超出 $T_{\text{center}}$ 為中心的迴文範圍（$R_{i'}>\text{len}$）  
        仔細想一下會發現：
        $$
        T_{\text{center}-R_\text{center}} \neq T_{\text{center}+R_\text{center}}\\
        T_{\text{center}-R_\text{center}} = T_{i'-\text{len}} = T_{i'+\text{len}} = T_{i-\text{len}} \\
        T_{\text{center}+R_\text{center}} = T_{i+\text{len}} \\
        T_{i-\text{len}} \neq T_{i+\text{len}}
        $$
        由此可知，$R_i$ 不會超過 $\text{len}$，而我們知道以 $T_{i'}$ 為中心的最長迴文是 $R_{i'}$，而 $R_{i'} > \text{len}$也就是說，存在以 $T_i$ 為中心，長度為 $\text{len}$ 的迴文，因此，$R_{i}=\text{len}$。  
    ```cpp
    int ii = center - (i - center);
    int len = mx - i + 1;
    if(i > mx){
        r[i] = ex(i, i);
        center = i;
        mx = i + r[i] - 1;
    }
    else if(r[ii] == len){
        r[i] = len + ex(i - len, i + len);
        center = i;
        mx = i + r[i] - 1;
    }
    else{
        r[i] = min(r[ii], len);
    }
    ```
    
最後，只要算怎麼把最大的 $R_i$ 轉成 $S$ 中最大迴文子字串的長度就好了。我們知道 $S$ 的每一個字元在 $T$ 中，前方都會有一個字元 $c$，而 $T$ 最後也有一個 $c$，剛好以 $T_i$ 為中心的最長迴文，兩端也會是 $c$，所以我們可以用一樣的想法來轉回去：令以 $T_i$ 為中心的最長迴文長度為 $t=R_i \times 2 - 1$，轉回去 $S$ 的長度就是 $\frac{(t-1)}{2}$（注意 $t$ 必為奇數），化簡後得到 $R_i-1$。

```cpp
#define T(x) ((x) % 2 ? s[(x) / 2] : '.')

string s;
int n;

int ex(int l, int r){
    int i = 0;
    while(l - i >= 0 && r + i < n && T(l - i) == T(r + i)) i++;
    return i;
}

int main(){
    cin >> s;
    n = 2 * s.size() + 1;

    int mx = 0;
    int center = 0;
    vector<int> r(n);
    int ans = 1;
    r[0] = 1;
    for(int i = 1; i < n; i++){
        int ii = center - (i - center);
        int len = mx - i + 1;
        if(i > mx){
            r[i] = ex(i, i);
            center = i;
            mx = i + r[i] - 1;
        }
        else if(r[ii] == len){
            r[i] = len + ex(i - len, i + len);
            center = i;
            mx = i + r[i] - 1;
        }
        else{
            r[i] = min(r[ii], len);
        }
        ans = max(ans, r[i]);
    }

    cout << ans - 1 << "\n";
    return 0;
}
```

仔細觀察會發現，這個過程只是不斷把 $\text{mx}$ 往右移，因此複雜度是漂亮的 $O(|S|)$。