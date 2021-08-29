---
title: 向量
---
# 向量

## 何謂向量

向量（Vector）表示特定的長度和方向，簡單來說，可以想成向量是一個箭頭。例如力、位移都算是向量。

向量可以是任何維度的，也就是說，有二維向量、也有三維向量、一維向量……，然後一個 $n$ 維向量可以用 $n$ 個數字來表示，第 $i$ 個數字表示要往第 $i$ 個維度的正向走多少距離（如果是負數，就是往負向走），而這個向量可以被看成是一個從起點指向終點的箭頭，舉例來說：

<img width="250px" src="/images/geometry/vector/vector.png">
這是一個二維向量，它表示向著 $x$ 軸正向走 $2$，並向著 $y$ 軸正向走 $3$，所以如果從原點開始走，會走到點 $(2,3)$。

向量有幾種表示方式，有把數字放在矩陣裡，寫成 
$\left[ \begin{array}{c}
v_1\\
v_2\\
...
\end{array} 
\right ]$ 
或 
$\left[ \begin{array}{ccc}
v1 & v2 & ...
\end{array} 
\right ]$ 
這種形式的，也有放在 tuple 裡，寫成 $(v_1, v_2, ...)$ 的，如果沒有特別需要用到矩陣，通常會用 tuple 來表示。

一個 $n$ 維向量 $(v_1,v_2,...,v_n)$ 的長度可以用畢氏定理來算：
$$\sqrt{\sum_{i=1}^n v_i^2}$$

長度為 $0$ 的向量稱為「零向量」，零向量可以是任意方向的。為了方便，除非特別註明，接下來提到的向量都不包含零向量。

基本符號：

- $\overrightarrow{AB}$，也就是 $\overrightarrow{B}-\overrightarrow{A}$，$A$、$B$ 是點，表示由 $A$ 指向 $B$ 的向量。（注意向量沒有特定的起終點，只能規定它的方向和長度）
- $\overrightarrow{A}$，$A$ 是點，等同於 $\overrightarrow{OA}$，$O$ 是原點。
- $|\overrightarrow{v}|$，向量 $\overrightarrow{v}$ 的長度。


## 基本運算

可以發現到，由原點指向某個點 $(x, y)$ 的向量，就是 $(x, y)$，所以也可以把點想成是向量、也可以把向量想成是點，這會有助於理解接下來的東西。

### 加減

兩個向量可以相加得到新的向量，就把所有維度的分量分別相加就好：
$$(u_1,u_2,u_3,...) + (v_1,v_2,v_3,...) = (u_1 + v_1, u_2 + v_2, u_3 + v_3, ...)$$

例如，$(2,3)+(3,1)=(5,4)$：

<img width="250px" src="/images/geometry/vector/plus.png">

兩個向量相加等同於兩個力的合力，可以發現到這張圖是個平行四邊形。

至於減法，就移項一下就可以暸解要怎麼做了，也可以想成是一個向量加上另一個向量的反向，或者是把兩個向量想成點，$\overrightarrow{A}-\overrightarrow{B}=\overrightarrow{BA}$，也就是一個從點 $B$ 指向點 $A$ 的向量，例如， $(2, 3)-(3, 1)=(-1, 2)$：

<img width="250px" src="/images/geometry/vector/minus.png">

### 純量乘法

沒有方向的量稱為純量，像是 $1$、$\frac{1}{2}$、$\pi$ 這些數字都是純量。向量可以乘上一個純量，得到一個新的向量，也就是將這個向量的長度乘上某一個數字，得到一個新的向量，這個動作非常簡單，就把每個維度的分量都乘上這個純量就好：
$$i(v_1, v_2, v_3, ...)=(iv_1, iv_2, iv_3, ...)$$

例如，$2 \times (2,3)=(4,6)$：  

<img width="250px" src="/images/geometry/vector/multiply.png">

### 內積（點積）

這是向量特有的運算，兩個夾角是 $\theta$ 的 $n$ 維向量 $\overrightarrow{u}=(u_1,u_2,...,u_n)$ 和 $\overrightarrow{v}=(v_1,v_2,...,v_n)$ 的內積記作 $\overrightarrow{u} \cdot \overrightarrow{v}$，結果是一個純量：
$$\overrightarrow{u} \cdot \overrightarrow{v} = |\overrightarrow{u}||\overrightarrow{v}|\cos\theta = \sum_{i=1}^{n} u_iv_i$$

其實就是把每一個維度的分量長相乘後相加，例如二維向量 $(x_1, y_1) \cdot (x_2, y_2) = x_1x_2 + y_1y_2$。意義是作一個 $\overrightarrow{u}$ 在 $\overrightarrow{v}$ 上垂直投影的向量，然後將這個向量的長和 $\overrightarrow{v}$ 的長相乘。

<img width="400px" src="/images/geometry/vector/dot.png">

（內積是 $|\overrightarrow{u}| \cos \theta$ 再乘上 $|\overrightarrow{v}|$，你想要 $\theta$ 是裡面那個角還是外面那個角都沒差，畢竟 $\cos \theta=\cos(2\pi-\theta)$。如果夾角超過直角，那麼投影會在另一邊，此時 $|\overrightarrow{u}|\cos\theta$ 會是負數。）

$\overrightarrow{F} \cdot \overrightarrow{S}$ 在力學上的意義是，對一個物體作一個力 $\overrightarrow{F}$，而物體的位移是 $\overrightarrow{S}$，則 $\overrightarrow{F} \cdot \overrightarrow{S}$ 是 $\overrightarrow{F}$ 對這個物體所作的功。

既然內積只是多維版本的乘法，那內積也和乘法一樣，有交換律、結合律且對加法有分配律。

接下來針對兩個向量的夾角 $\theta$ 大小來討論內積的結果為何：

- $\theta = 90^\circ = \frac{1}{2}\pi$  
    顯而易見地，如果作用在一個物體上的力和物體位移方向垂直，那麼這個力對這個物體不作功，且 $\cos 90^\circ=\cos \frac{1}{2}\pi$ 也確實為 $0$，因此我們知道，兩個垂直的向量內積是 $0$。

- $\theta = 0^\circ = 0$  
    如果作用在一個物體上的力和物體位移方向相同，那麼這個力作的功等同於力的大小乘上位移距離，同樣 $\cos 0^\circ = \cos 0$ 也是 $1$，因此兩個方向相同的向量 $\overrightarrow{u}$、$\overrightarrow{v}$ 的內積是 $|\overrightarrow{u}||\overrightarrow{v}|$。

- $\theta = 180^\circ = \pi$  
    如果作用在一個物體上的力和物體位移方向相反，那麼這個力作的會是負功，且這個負功的大小等於力的大小乘上位移距離，同樣 $\cos 180^\circ=\cos\pi$ 是 $-1$，因此兩個方向相反的向量 $\overrightarrow{u}$、$\overrightarrow{v}$ 內積是 $-|\overrightarrow{u}||\overrightarrow{v}|$。

- $0^\circ=0 < \theta < 90^\circ=\frac{1}{2}\pi$  
    也就是兩個向量方向在同一邊的時候，顯然如果作用在一個物體上的力和物體位移方向在同一邊，那麼這個力作的會是正功，同樣 $\cos \theta$ 的範圍會是 $(0,1)$，因此兩個夾角是 $\theta$、方向在同一邊的向量 $\overrightarrow{u}$、$\overrightarrow{v}$ 內積會是一個正數且 $0 < \overrightarrow{u} \cdot \overrightarrow{v} < |\overrightarrow{u}||\overrightarrow{v}|$。

- $90^\circ=\frac{1}{2}\pi < \theta < 180^\circ=\pi$  
    也就是兩個向量方向在不同邊的時候，如果作用在一個物體上的力和物體位移方向在不同邊，那麼這個力作的會是負功，同樣 $\cos \theta$ 的範圍會是 $(-1,0)$，因此兩個夾角是 $\theta$、方向在不同邊的向量 $\overrightarrow{u}$、$\overrightarrow{v}$ 內積會是一個負數且 $-|\overrightarrow{u}||\overrightarrow{v}| < \overrightarrow{u} \cdot \overrightarrow{v} < 0$。

兩向量在不同夾角時的內積：

<img width="600px" src="/images/geometry/vector/dot1.png">

兩個長度為 $1$ 的向量在不同夾角時的內積（$x$ 軸為夾角（弧度）、$y$ 軸為內積）：
<img width="400px" src="/images/geometry/vector/dot2.png">

內積常被用來判斷兩個向量是否垂直，也可以用來判斷兩個向量的方向是否在同一邊、是否相同或者相反。

### 外積（叉積）

向量特有的運算，在定義上，它只能用在三維，兩個三維向量 $\overrightarrow{u}=(x_1,y_1,z_1)$ 和 $\overrightarrow{v}=(x_2,y_2,z_2)$ 的外積記作 $\overrightarrow{u} \times \overrightarrow{v}$，是一個新的二維向量 （$x_3,y_3,z_3$）：  
$$\overrightarrow{u} \times \overrightarrow{v}=\left|\begin{array}{ccc} 
    \bf{i} & \bf{j} & \bf{k} \\
    x_1 & y_1 & z_1 \\
    x_2 & y_2 & z_2
\end{array}\right| = (y_1z_2-z_1y_2)\textbf{i}-(x_1z_2-z_1x_2)\textbf{j}+(x_1y_2-y_1x_2)\textbf{k}$$

其中，$\bf{i}$、$\bf{j}$、$\bf{k}$ 是三個維度的「基向量」，也就是 $(1,0,0)$、$(0,1,0)$、$(0,0,1)$。外積得到的向量會垂直於 $\overrightarrow{u}$ 和 $\overrightarrow{v}$ 構成的平面，且當 $\overrightarrow{u}$ 和 $\overrightarrow{v}$ 的夾角是 $\theta$，外積得到的向量長度是：
$$||\overrightarrow{u}||\overrightarrow{v}|\sin\theta|$$

它的長度等同於兩個向量所夾的平行四邊形面積。

至於它的方向，會依據右手定則，右手食指指向 $\overrightarrow{u}$，中指指向 $\overrightarrow{v}$，大姆指的方向就會是 $\overrightarrow{u} \times \overrightarrow{v}$ 的方向。

以上不重要 (?)。二維向量的外積比較常用，但剛剛不是說只能用在三維？你會發現把第三維全部代 $0$，就會變成：
$$\overrightarrow{u} \times \overrightarrow{v}=(x_1y_2-y_1x_2)\textbf{k}$$

$\textbf{k}$ 的部分我們不要管它，把二維外積定義為三維外積的長度（純量），如果三維外積的結果向量向上，那二維外積是正的，否則就是負的，可以得出：
$$\overrightarrow{u} \times \overrightarrow{v}=\left|\begin{array}{cc} 
    x_1 & y_1 \\
    x_2 & y_2 \\
\end{array}\right|=x_1y_2-y_1x_2=|\overrightarrow{u}||\overrightarrow{v}|\sin\theta$$

相同地，這個值等同於兩個向量所夾的平行四邊形面積，但它是「有向」的，如果 $\overrightarrow{u}$ 轉向 $\overrightarrow{v}$ 是逆時針，那會是正的，反之就會是負的（這邊的轉指往較近那邊轉），至於夾角 $\theta$ 是指 $\overrightarrow{u}$ 往逆時針轉到 $\overrightarrow{v}$ 的角度。

<img width="400px" src="/images/geometry/vector/cross.png">

外積沒有交換律，也就是說 $\overrightarrow{u}\times\overrightarrow{v}\neq\overrightarrow{v}\times\overrightarrow{u}$，但它滿足「負交換律」，也就是 $\overrightarrow{u}\times\overrightarrow{v}=-(\overrightarrow{v}\times\overrightarrow{u})$，因為：
$$(x_1,y_1)\times(x_2,y_2)=x_1y_2-x_2y_1\\
=-(x_2y_1-x_1y_2)=-(x_2,y_2)\times(x_1,y_1)$$

外積沒有結合律（甚至二維的外積算出來也不是向量），但對加法有分配律。

接下來我們針對各種夾角 $\theta$ 討論它的值：

- $\theta = 90^\circ=\frac{1}{2}\pi$  
    這樣兩個向量會夾一個長方形，且 $\sin 90^\circ=\sin \frac{1}{2}\pi=1$，因此兩個夾角為直角的向量 $\overrightarrow{u}$、$\overrightarrow{v}$ 外積為 $|\overrightarrow{u}||\overrightarrow{v}|$。

- $\theta = 270^\circ=\frac{3}{2}\pi$  
    這樣兩個向量會夾一個長方形，且 $\sin 270^\circ=\sin \frac{3}{2}\pi=-1$，但 $\overrightarrow{u}$ 轉向 $\overrightarrow{v}$ 是順時針，因此$\overrightarrow{u} \times \overrightarrow{v} = -|\overrightarrow{u}||\overrightarrow{v}|$。

- $\theta = 0^\circ = 0$  
    兩個向量同向，那麼它們夾的平行四邊形面積為 $0$，且 $\sin 0^\circ=\sin 0=0$，因此此時外積值為 $0$。

- $\theta = 180^\circ = \pi$  
    兩個向量反向，此時它們夾的平行四邊形面積也為 $0$，且 $\sin 180^\circ=\sin \pi = 0$，因此此時外積值為 $0$。

- $0^\circ=0 <\theta < 180^\circ = \pi$  
    $\overrightarrow{u}$ 往 $\overrightarrow{v}$ 轉是逆時針，且 $\sin \theta \in (0, 1]$，則 $\overrightarrow{u} \times \overrightarrow{v} > 0$。除非 $\theta=90^\circ=\frac{1}{2}\pi$，不然 $\sin \theta < 1$，則 $0 < \overrightarrow{u} \times \overrightarrow{v} < |\overrightarrow{u}||\overrightarrow{v}|$。

- $180^\circ=\pi <\theta < 360^\circ = 2\pi$  
    $\overrightarrow{u}$ 往 $\overrightarrow{v}$ 轉是順時針，且 $\sin \theta \in [-1, 0)$，則 $\overrightarrow{u} \times \overrightarrow{v} < 0$。除非 $\theta=270^\circ=\frac{1}{2}\pi$，不然 $\sin \theta > -1$，則 $-|\overrightarrow{u}||\overrightarrow{v}| < \overrightarrow{u} \times \overrightarrow{v} < 0$。

兩向量在不同夾角時的外積：
<img width="600x" src="/images/geometry/vector/cross1.png">

兩個長度為 $1$ 的向量在不同夾角時的外積（$x$ 軸為夾角（弧度）、$y$ 軸為外積）：
<img width="400px" src="/images/geometry/vector/cross2.png">


## 實作

有些人會把向量（或點）做成一個 class，不過我自己是習慣直接用 `pair`，然後再做運算子重載。

```cpp=
#define F first
#define S second
#define mp make_pair

template<typename T>
pair<T, T> operator+(pair<T, T> a, pair<T, T> b){
    return mp(a.F + b.F, a.S + b.S);
}

template<typename T>
pair<T, T> operator-(pair<T, T> a, pair<T, T> b){
    return mp(a.F - b.F, a.S - b.S);
}

template<typename T>
pair<T, T> operator*(pair<T, T> a, T b){
    return mp(a.F * b, a.S * b);
}

template<typename T>
pair<T, T> operator/(pair<T, T> a, T b){
    return mp(a.F / b, a.S / b);
}

template<typename T>
T dot(pair<T, T> a, pair<T, T> b){
    return a.F * b.F + a.S * b.S;
}

template<typename T>
T cross(pair<T, T> a, pair<T, T> b){
    return a.F * b.S - a.S * b.F;
}

template<typename T>
T abs2(pair<T, T> a){
    return a.F * a.F + a.S * a.S;
}
```

