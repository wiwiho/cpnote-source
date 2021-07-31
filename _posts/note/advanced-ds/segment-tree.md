# 線段樹

> 有一個序列 $A$，有 $Q$ 筆詢問，詢問有兩種：
> 
> 1. 把 $A_{l..r}$ 加上 $v_i$
> 2. 求 $A_{l..r}$ 總和

像這樣有修改有查詢的問題，就需要用上線段樹了。

用把區間分割的方式去想，整個序列是一個大區間，然後這一個區間可以二等分成兩個小區間（如果長度是奇數，就看你喜歡放哪一邊），每一小區間又可以再二等分，這樣一直二等分下去，到最後會分到每一區間都剩下一個元素。先把這樣分出來的每個區間中的答案（所有會被詢問的資訊）算出來，詢問的時候在把一些區間合併。

這樣可以畫成一棵二元樹：根節點表示整個序列，它的左子節點表示它的左半部，右子節點表示它的右半部，然後每個節點的左子節點都表示該節點所表示範圍的左半部，右子節點表示右半部，葉節點則表示只有一個元素的區間。如此一來，每一個節點都表示一個區間，而每個節點表示的區間都完整包含了其子節點所表示的區間。

舉例來說，這是一個長度為 $9$ 的線段樹，然後奇數長的塊，我習慣在分割後把中間那個放到左邊去：
<img width="600px" src="/images/advanced-ds/segment-tree/segment-tree.png">

順帶一提，序列 index 要從 $0$ 或從 $1$ 開始的實作沒差，看習慣就好，然後區間表示也有分左閉右閉（$[l,r]$）或左閉右開($[l,r)$)，看習慣。接下來的範例都會是索引從 $0$ 開始且區間都用左閉右閉來表示。

在每一個節點上，儲存在那個區間中我們想要的答案，例如最大值、最小值、區間和……等等的，然後父節點的答案可以從兩個子節點來得到，而每個葉節點所表示的區間中都只有一個數字，所以葉節點的答案只要考慮那個數字就好。

## 儲存

接著來討論一下線段樹該如何儲存，線段樹是一個接近完全二元樹的樹，所以可以用和完全二元樹一樣的方式存，也叫陣列型線段樹。完全二元樹是除了最深那層外每一層都全滿、最深那層的結點都靠右的樹，然後節點由淺至深、由左至右編號為 0、1、2……，這樣一來，節點 $i$ 的子節點就是 $2i+1$ 和 $2i+2$。也可以用 1、2、3……編號，子節點是 $2i$ 和 $2i+1$。

雖然它並不真的是完全二元樹，但其實不會浪費太多空間。來想一下陣列該開多大，也就是節點編號最多會用到多少。一棵有 $2^i$（$i$ 是非負整數）個葉節點的 perfect binary tree，它的非葉節點會有 $2^i-1$ 個，因此它的總節點數是 $2^{i+1}-1$。線段樹的葉節點數和序列長度是一樣的，如果這個數字是 $n$，那麼葉節點會有 $n$ 個，最後一層填滿的話，應該會有 $2^{\lceil\log_2n\rceil}$ 個葉節點，因此整棵樹會有 $2^{\lceil\log_2n\rceil+1}-1$ 個節點。

如果 $n=2^i+a$，$0<a<2^i$，那麼 $2^{\lceil\log_2n\rceil}=2^{i+1}$，$2^{\lceil\log_2n\rceil+1}-1=2^{i+2}-1<2^{i+2}$，由此可知，$4n$ 一定會大於總節點數，因此陣列大小要取 $4n$，而且用到接近 $4n$ 會發生在 $a$ 很小的狀況。

有時候節點資訊會有很多，像是在打懶標的時候，可以用 struct 包節點資訊。

除了用這種存法外，也可以用指標的存法，可以放在 struct 裡，例如：
```cpp
struct Node{
    Node *l, *r; // 子節點指標
    // 節點資訊 ...
};
```

還有一種我很喜歡的作法，我把它叫偽指標，就是用一個陣列當作 memory pool，把在陣列上的位置當成指標：
```cpp
struct Node{
    int l, r; // 子節點編號
    // 節點資訊 ...
};
vector<Node> st; // memory pool
int pos = 0; // memory pool 用到哪了
```

指標型線段樹用的空間，也就是線段樹的節點數是剛好 $2n-1$，可以用數學歸納法證明，令 $f(n)$ 是序列長度 $n$ 的線段樹的節點數：

- 顯然 $f(1)=1=2 \times 1 - 1$。
- 如果當 $n < k$，$f(n)=2n-1$，那麼當 $n=k$ 時，我們知道 $f(n)=f(\lceil \frac{n}{2} \rceil) + f(\lfloor \frac{n}{2} \rfloor) + 1$，然後
    - 如果 $n$ 是偶數，$f(n)=2f(\frac{n}{2})+1=2(n-1)+1=2n-1$
    - 如果 $n$ 是奇數，$f(n)=f(\frac{n+1}{2}) + f(\frac{n-1}{2}) + 1 = n+1-1 + n-1-1 +1= 2n-1$

不過要注意指標型線段樹的空間不一定比較省，因為會多用兩個指標的空間，也就是 8 bit，所以在本來節點大小不大的狀況，陣列型的空間還是會用比較少。

在用指標型線段樹的時候，可以讓 `build()` 回傳新建的節點的指標，然後直接寫
```cpp
目前節點的左子節點 = build(左子節點);
目前節點的右子節點 = build(右子節點);
```
也可以在動態開點的時候讓 `modify` 回傳節點的指標。

## 建構

建立一棵線段樹很簡單，就一直遞迴去把區間二等分填數字就好。

為了方便，以下都使用 pseudo code。

```cpp
array a; // 序列初始值

// v 的區間是 [L,R]
void build(int L, int R, vertex v){
    if(L == R){
        v 的答案 = 用 a[L] 得出答案;
        return;
    }
    int M = (L + R) / 2;
    //把區間二等分
    build(L, M, v 的左子節點);
    build(M + 1, R, v 的右子節點);
}
```

複雜度就和節點數一樣，是 $O(n)$。

## 單點修改

修改一個位置的時候，會改到所有包含它的區間，而這些區間就是「表示它的葉節點」和這個點的所有祖先，可以用遞迴的方式處理：

```cpp
// 節點 v 的區間範圍是 [L,R]，要修改的地方是 pos，新值是 value
void modify(type value, int pos, int L, int R, vertex v){
    if(L == R){ //找到了葉節點
        修改 v;
        return;
    }
    int M = (L + R) / 2; // [L,R] 區間的中點
    // 將這個區間二等分，左半的範圍是 [L,M]，右半是 [M+1,R]
    if(pos >= L && pos <= M) // pos 在左半部
        modify(value, pos, L, M, v的左子節點);
    else // pos 在右半部
        modify(value, pos, M+1, R, v的右子節點);
    根據v的左子節點和右子節點的答案更改v的答案;
}
```

線段樹的深度最深就是 $\lceil\log_2n\rceil$，因此遞迴次數為 $O(\log n)$，時間複雜度 $O(\log n)$。

## 區間查詢

如果遇到有一個節點的範圍被完整包含在查詢範圍內，就可以直接取這個節點記錄的答案，而不用往下找。這也可以用遞迴來做：

```cpp
// 查詢範圍是 [l,r]，節點 v 的區間範圍是 [L,R]
type query(int l, int r, int L, int R, vertex v){
    if(l == L && r == R) // [L,R] 完整被查詢區間所包含
        return ans of v;
    int M = (L + R) / 2;
    if(r <= M) // 如果查詢區間都在左半部，就只查左半部
        return query(l, r, L, M, v的左子節點);
    else if(l > M) // 如果查詢區間都在右半部，就只查右半部
        return query(l, r, M + 1, R, v的右子節點);
    else{
        // 如果查詢區間跨越兩半部，那就也把查詢區間切半
        // 這樣可以確保遞迴後 [l,r] 一定在 [L,R] 之內
        return 用query(l, M, L, M, v的左子節點)
            和query(M + 1, r, M + 1, R, v的右子節點)
            得出區間[l,r]的答案;
    }
}
```

<img width="600px" src="/images/advanced-ds/segment-tree/query.png">

舉例來說，如果查詢區間是 $[2,7]$，被遞迴到的會是上圖紅色的點。可以發現到，遞迴到的點一開始會是一條路徑，直到表示兩個端點的葉節點的 LCA，然後開始分叉成兩條到兩個端點的路徑，還有左邊路徑上的每一個節點的右子節點與右邊路徑上的每一個節點的左子節點。

（示意圖）

<img width="300px" src="/images/advanced-ds/segment-tree/query2.png">

可以發現這數量最多就深度的四倍而已，所以複雜度也是 $O(\log n)$。也可以得出遞迴的終點最多只有 $O(\log n)$ 個，事實上，線段樹的功能就是「把一個區間變成 $O(\log n)$ 個區間」，而這些區間就是遞迴到的終點，它們的聯集會是整個查詢區間。

## 區間修改

要做區間修改的話，可以用到懶人標記（可以參加[分塊法](/sqrt-decomposition/)的懶人標記），作法就是如果某個節點的區間被修改的區間完全包含，那麼就先在這個節點上記錄「整個節點的區間都被做了同樣的修改」，並且直接終止，而不再遞迴下去。至於打了懶人標記的節點，這個區間的答案要可以用懶人標記和原本的答案算出來。節點上要記錄原本的答案和懶人標記，至於真正的答案可以多寫一個 function 來算。

在詢問的時候，遇到有懶人標記的節點，要再往它的子節點走時，必須先把懶人標記下推，這樣在子節點算的答案才會是對的。在修改沒有交換律的時候（也就是修改順序不能改變，例如區間改值沒有交換律，而區間加值有交換律），之後的修改經過有懶人標記的節點，也要把懶人標記往下推，才能確保修改的順序是正確的。

下推的時候，先對子節點打懶標，然後再把這個節點記錄的答案變成真正的答案，例如：

```cpp
void push(vertex v){
    對 v 的左子節點打 v 的懶標;
    對 v 的右子節點打 v 的懶標;
    v 的答案 = v 真正的答案;
    v 的懶標 = 預設值;
}
```

遞迴的方式和區間詢問相同，概念是一樣的，也是「將修改的區間變成 $O(\log n)$ 個區間，對這些區間做事」。

```cpp
//新值是 value，修改區間是 [l,r]，節點 v 的範圍是 [L,R]
void modify(type value, int l, int r, int L, int R, vertex v){
    if(l == L && r == R){
        打懶標在v上;
        return;
    }
    把節點 v 的懶標下推; // 修改有交換律的時候可以不用
    int M = (L + R) / 2;
    if(r <= M) modify(value, l, r, L, M, v的左子節點);
    else if(l > M) modify(value, l, r, M + 1, R, v的右子節點);
    else{
        modify(value, l, M, L, M, v的左子節點);
        modify(value, M + 1, r, M + 1, R, v的右子節點);
    }
    用兩個子節點的「真正的答案」更新v的答案;
}
```

含懶標的區間查詢：
```cpp
// 查詢範圍是 [l,r]，節點 v 的區間範圍是 [L,R]
type query(int l, int r, int L, int R, vertex v){
    if(l == L && r == R)
        return ans of v;
    把節點v的懶標下推; // <----
    int M = (L + R) / 2;
    if(r <= M)
        return query(l, r, L, M, v的左子節點);
    else if(l > M)
        return query(l, r, M + 1, R, v的右子節點);
    else{
        return 用query(l, M, L, M, v的左子節點)
            和query(M + 1, r, M + 1, R, v的右子節點)
            得出區間[l,r]的答案;
    }
}
```

這樣一來，區間修改的複雜度就和區間查詢一樣，是 $O(\log n)$。

## 範例

這是一個支援區間加值、區間詢問和的陣列型線段樹：

```cpp
struct Node{
    // v = 不算懶標的答案，tag = 這個區間被加了多少，sz = 區間大小
    int v = 0, tag = 0, sz;
    int rv(){ // 算上懶標的答案
        return v + tag * sz;
    }
};

vector<Node> st; // 記得 resize 成 4n
vector<int> a; // 序列初始值

void build(int l, int r, int id){
    st[id].sz = r - l + 1;
    if(l == r){
        st[id].v = a[l];
        return;
    }
    int m = (l + r) / 2;
    build(l, m, 2 * id + 1);
    build(m + 1, r, 2 * id + 2);
    st[id].v = st[2 * id + 1].v + st[2 * id + 2].v;
}

// 把節點 id 的懶標下推
void push(int id){
    st[2 * id + 1].tag += st[id].tag;
    st[2 * id + 2].tag += st[id].tag;
    st[id].v = st[id].rv();
    st[id].tag = 0;
}

// 把 [l,r] 加上 v
void modify(int l, int r, int v, int L, int R, int id){
    if(l == L && r == R){
        st[id].tag += v;
        return;
    }
    int M = (L + R) / 2;
    if(r <= M) modify(l, r, v, L, M, 2 * id + 1);
    else if(l > M) modify(l, r, v, M + 1, R, 2 * id + 2);
    else{
        modify(l, M, v, L, M, 2 * id + 1);
        modify(M + 1, r, v, M + 1, R, 2 * id + 2);
    }
    st[id].v = st[2 * id + 1].rv() + st[2 * id + 2].rv();
}

// 詢問 [l,r] 的和
int query(int l, int r, int L, int R, int id){
    if(l == L && r == R) return st[id].rv();
    push(id);
    int M = (L + R) / 2;
    if(r <= M) return query(l, r, L, M, 2 * id + 1);
    else if(l > M) return query(l, r, M + 1, R, 2 * id + 2);
    else return query(l, M, L, M, 2 * id + 1) + query(M + 1, r, M + 1, R, 2 * id + 2);
}
```

## 動態開點

> 有一個長度是 $10^9$ 的序列，一開始裡面的元素都是 $0$，有 $Q$ 筆操作，每一個操作是以下其中兩種：
>
> 1. 把 $[l,r]$ 之間的值都加上 $v$
> 2. 詢問 $[l,r]$ 的區間和

像這種範圍超大的狀況，直接開線段樹會 MLE，這時候有兩種作法，第一種是離散化，也就是只管會用到的位置，第二種就是動態開點線段樹。

在這種狀況中，其實有很多節點是沒用的，可以不要把它們開出來，浪費記憶體空間，這個時候必須用指標型線段樹，偽指標也可以用，不過用偽指標線段樹的話，要先把空間開好，空間的用量大約是 $Q \log n$，記憶體限制允許的話可以多乘個幾倍常數。

實作的部分可以像前面偽指標線段樹讓 `build()` 回傳偽指標一樣，也可以讓 `modify()` 回傳節點指標。

指標版實作範例：

```cpp
struct Node{
    Node *l = nullptr, *r = nullptr; // 左右子節點
    // 節點資訊 ...
};

Node *rt = new Node(); // 根節點

// 不用寫 build

Node *modify(操作資訊..., int L, int R, Node *v){
    if(v == nullptr){ // 如果這個節點沒開出來，就開一個
        v = new Node();
    }
    if(L == R){
        // 做操作
        return v;
    }
    // 跟一般的修改一樣
    return v; // 記得 return
}

type query(詢問資訊..., int L, int R, Node *v){
    // 如果這節點沒開出來，表示這個區間完全沒修改過
    if(v == nullptr) return 預設答案;
    // 跟一般的詢問一樣
}
```

## 練習題

- [ZeroJudge d539](https://zerojudge.tw/ShowProblem?problemid=d539) - 區間詢問最大值
- [ZeroJudge d799](https://zerojudge.tw/ShowProblem?problemid=d799) - 區間加值、區間求和
- [TIOJ 1224](https://tioj.ck.tp.edu.tw/problems/1224) - 給你一堆矩形，求這些矩形的聯集面積