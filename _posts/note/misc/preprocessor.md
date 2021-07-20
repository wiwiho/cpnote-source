# 前置處理器

## 簡介

C++ 是一個編譯式語言，也就是程式碼要先經過編譯，變成執行檔才能執行。不過「編譯」的過程其實不光只有編譯這麼簡單，例如這個程式碼：

```cpp
#define test 123
#include<iostream>
```

這種以 `#` 為開頭的程式碼是**前置處理器**的指令，在編譯之前有一個階段就叫作前置處理，前置處理做的事情就是根據你的指令修改程式碼，然後再拿去編譯。

舉例來說，`#include` 會在編譯前將指定檔案裡的文字完全複製貼上到你 include 的那個地方，它可以用在任何地方，例如：

你開了一個檔案叫做 `hello.txt`，內容只有 `"hello"`，然後你在同目錄有另一個檔案 `test.cpp`，內容是：
```cpp
#include<iostream>
using namespace std;

int main(){
    cout <<
        #include "hello.txt"
        << "\n";
    return 0;
}
```
那麼會輸出 `hello`，在編譯之前，`#include "hello.txt"` 這一行就會被替換成 `"hello"`。

還有一個常見的指令是 `#define`，寫法是 `#define identifier 替換字串`，也被稱為「巨集」或「宏」（macro），有些人可能會說這是「常數」，然後你就會開始懷疑它跟 `const` 的差別，其實 `#define` 並不是在宣告一個常數，而是它會把整份程式碼中的一段特定文字替換，例如：

```cpp
#include<iosteam>
#define hello "hello"
using namespace std;

int main(){
    cout << hello << "\n";
    return 0;
}
```
在編譯之前，`hello` 就會被替換成 `"hello"`，接著才進行編譯，所以輸出會是 `hello`。它也有 function 的用法：

```cpp
#inlcude<iosteam>
#define say(a) cout << a << "\n"
using namespace std;

int main(){
    say("hello");
    return 0;
}
```
這樣會輸出 `hello`，在編譯前，`say("hello")` 會被替換成 `cout << a << "\n"`。

要特別注意的一點是，因為這是把文字原封不動貼上，所以 `#define` 替換的部分**不會**先做運算，而是在執行期按照前置處理器處理完的程式碼運算，例如：
```cpp
#include<iostream>
#define plus(a, b) a + b
using namespace std;

int main(){
    cout << (plus(1, 2) * 3) << "\n";
    return 0;
}
```
這樣的結果並不是 `9`，而是 `7`，因為替換完後的程式碼會是 `1 + 2 * 3`，`2 * 3` 會先被計算。所以建議都用個括號把它包起來。

以上是 `#define` 的「巨集」用法，而 `#define` 還有另一個功用，前置處理器也有 if 的語法，它們都和 `#define` 有關。

最單純的是 `#if`、`#elif`、`#else`、`#endif`，用法例如：
```cpp
#include<iostream>
#define A 3
using namespace std;

int main(){
    #if A == 3
    cout << "test\n";
    #elif A == 2
    cout << "hello\n";
    #else
    cout << "QQ\n";
    #endif

    return 0;
}
```
這就像是一般的 if 控制語法，只是以 `#endif` 結束區塊，要巢狀結構也可以。如果判斷結果是 `true`，那個區塊才會被留下來，否則會被刪掉，上述的範例中，只有 `A==3` 這個判斷會是 `true`，因此只有第 7 行會留下來，第 9 和 11 行不會。前置處理器的判斷只能判 `#define` 定義的東西，可以判等於、比大小等等。如果把第 2 行改成 `#define A 2`，那被留下的就會是第 9 行，如果 `A` 不是 `2` 也不是 `3`，那被留下的就會是第 11 行。

除了可以判斷值之外，也可以判斷一個 identifier 有無被定義，用 `defined(identifier)` 就可以得到指定的 identifier 有沒有 define 過，例如：
```cpp
#include<iostream>
#define A
using namespace std;

int main(){
    #if defined(A)
    cout << "test\n";
    #endif
    #if defined(B)
    cout << "hi\n";
    #endif

    return 0;
}
```
第 7 行會被留下來，而第 10 行不會。`#if defined(A)` 可以簡寫為 `#ifdef A`，而 `#if !defined(A)` 可以簡寫為 `#ifndef A`。至於已經 define 過的東西可以用 `#undef` 移除。

這通常會用來避免標頭檔被重複 include，至於競賽用途，如果你打了一大段測試用的程式碼，覺得要在 submit 前註解掉、WA 了又要取消註解很麻煩，那就可以用個 `#ifdef` 來處理，會方便許多。

## define 花式用法

其實通常也只會用到 define 而已 (?)，define 在競賽中最大的功能就是把常用的東西變得比較好寫，例如這是一個常見的 pair 模板：

```cpp
#define mp make_pair
#define F first
#define S second
using pii = pair<int, int>;
```

除了普通的把東西替換掉之外，function macro 還有一種特別的寫法：

```cpp
#define err(a) cerr << #a << ": " << a << "\n"

int num = 123;
err(num); // 輸出 num: 123
```

`#a` 就是把你在 `a` 打的東西變成字串替換上去，所以 `err(num);` 會被替換成：

```cpp
cerr << "num" << ": " << a << "\n";
```