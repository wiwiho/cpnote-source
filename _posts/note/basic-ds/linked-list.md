# 鏈結串列

陣列和動態陣列都可以隨機存取，但如果要移除一個元素而不留空位，就得花 $O(n)$ 的時間把後面的元素往前移，在中間插入一個元素也是需要把後面所有元素後移，也要 $O(n)$ 的時間，那麼如果需要頻繁進行在序列中間刪除或插入的動作怎麼辦呢？

鏈結串列（Linked List）可以做到這件事，它把每一個元素放進一個節點裡，每個節點除了儲存元素的值外，也儲存一些指標，這些指標指向哪裡會根據你的需求而有所不同。

最基礎的鏈結串列是**單向鏈結串列**，每一個節點有一個指標，指向下一個元素所在的節點，如果沒有下一個，就指向 `nullptr`。

```cpp=
template<typename T>
struct Node{
    T value;
    Node* nxt = nullptr;
};
```

要插入一個元素的話，就把前一個元素的節點的下一個節點改成新插入的節點，而新插入的節點指向前一個節點本來的下一個節點。

```cpp=
template<typename T>
Node<T>* insert(Node<T>* node, int value){
    Node<T>* n = new Node<T>();
    n->nxt = node->nxt;
    n->value = value;
    node->nxt = n->value;
    return n;
}
```

要刪除節點的話，就把要刪除的節點的上一個節點，接到要刪除的節點的下一個節點。不過單向鏈結串列要找一個節點的上一個節點的話，必須從頭開始線性搜尋，會比較麻煩一點。這個時候就可以用雙向連結串列，也就是再存一個指向上個節點的指標，這樣就可以馬上知道上一個點是誰了。

還有很多種可能的狀況，像是你的鏈結串列是環狀的，就可以讓最後一個節點的下一個節點是第一個節點。

除了可以用指標來做外，也可以開兩個陣列，這兩個陣列中的相同位置一起表示一個節點，一個陣列用來存值、另一個存下一個節點的位置編號，如果要做雙向的話也可以再開一個陣列。

指標實作鏈結串列最大的缺點是不能隨機存取，但陣列實作可以彌補，雖然還是不能直接隨機存取串列裡第幾個元素，但你可以給位置編號特殊意義，像是在陣列裡的位置 $i$ 表示編號是 $i$ 的東西，這樣你就可以隨機存取每一個東西的上一個或下一個東西是什麼。

## STL

STL 中的 `list` 是雙向鏈結串列，但是很難用，沒什麼用處。