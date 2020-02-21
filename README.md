# chico-and-dico

> Chico 和 Dico 是两位魔术师，他们有一个经典魔术。但完成这个魔术不需要任何作弊技巧，因为它完全建立在数学原理之上。只需要一点数学原理和一颗能够快速计算的大脑，你也能实现这个魔术！

### Chico 和 Dico 的魔术

Chico 和 Dico 是两位魔术师，他们有一个魔术是这样的：Chico 将一副 52 张的扑克牌交给一位观众，让他随机抽取其中的 5 张。然后 Chico 将这 5 张牌按一定的规则重新排序，再将其还给观众。上述整个过程 Dico 都是看不见的。然而，当观众按 Chico 排好的顺序依次展示前四张牌之后，Dico 能奇迹般地说出第五张牌是什么。

乍一看这个魔术很神奇。随机抽取 5 张牌，你能从前 4 张牌中看出第 5 张牌是什么吗？如果你只是个普通人，那么肯定不能。Chico 和 Dico 的魔术的秘诀在于 Chico 有机会将牌重新排序。如果两人事先约定好某种协议，Dico 是可能从 Chico 排列的牌组顺序中看出第五张牌是什么的。

关键在于如何实现这种协议。

### 数学模型

魔术本身提供了一些建模信息。我们假设一共有 n 张牌，从中抽取 k 张。在对牌组进行某种排序之后，我们需要利用前 (k - j) 张牌的信息，推测后 j 张牌是什么。其中，中间那步排序操作，本质上是利用前 (k - j) 张牌的顺序信息对后 j 张牌进行编码。

现在我们有 n, j, k 三个变量，下一步来探究三个变量之间服从何种关系。

首先，我们知道从 n 张牌中抽取 k 张牌一共有 C(n, k) 种组合方式，而 (k - j) 张牌的排列方式有 A(n, k-j) 种。按照模型的要求，我们要用后者对前者进行编码。根据信息论中的信源编码理论，至少有：C(n, k) <= A(n, k-j)。

根据上述不等式方程，我们有：
`$$ C(n, k) = \frac{n!}{(n-k)!k!} \leq \frac{n!}{(n-k+j)!} = A(n, k-j), \\ 即 (n - k + j)! \leq k!(n - k)!$$`
故 n, j, k 三个变量至少需要满足：
`$$ (n - k + j)! \leq k!(n - k)! $$`

### 算法实现

为了更好地理解 Chico 对牌组的编码，以及 Dico 对牌组的解码。我们用一个实例复现一下魔术现场的情形。

根据我们的模型和文章开头对魔术的描述，我们有 n = 52, k = 5, j = 1。

此外我们还作如下约定：

1. cards 代表所有 52 张牌构成的列表；
2. selected_cards 代表观众选出的 5 张牌构成的列表；
3. 被 Chico 排好序的牌组放入列表 reordered_cards 中；
4. 约定 s = sum(selected_cards) mod k!；
5. 一般情况下，q 代表商（初始化那次除外），r 代表余数。

好了，现在我宣布，从这里开始，这个广场就叫作魔术广场 <img src="/img/hanser/png/cece.png" class="my-emoji" style = "height: 32px;">

第一步，我们让观众取出 5 张牌 {18, 50, 12, 19, 4}，然后对这副牌从小到大进行排序。

```python
selected_cards = [18, 50, 12, 19, 4]
selected_cards = sorted(selected_cards)
# selected_cards = [4, 12, 18, 19, 50]
```

第二步，计算 s = sum(selected_cards) mod k!

```python
s = sum(selected_cards) % factorial(5)
# s = 103
```

第三步，我们要对这 5 张牌按如下规则进行编码：

```python
q = s
for i in range(5, 0, -1):
    q, r = divmod(q, i)
    reordered_cards.append(selected_cards.pop(r))
```

为了理解这一步做了什么，我们将上述循环过程展开。

<details>
<summary style="outline: none;"><font color='blueviolet'>点击查看每轮迭代中的细节</font></summary>

初始化，s = 103：

| i | 1 | 2 | 3 | 4 | 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | null | null | null | null | null ||
| q | null | null | null | null | null | s = 103 |
| r | null | null | null | null | null ||

当 i = 5 时，被除数初始化为 s。因此有 `q_5 = s / i = 103/5 = 20, r_5 = s % i = 103%5 = 3`。将列表 selected_cards 中的索引为 r_5（= 3）的扑克，放入列表 reordered_cards 中。现在列表 selected_cards 为 [4, 12, 18, 50]，列表 reordered_cards 为 [19]。具体结果如下：

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | null | null | null | null | reordered_cards[0] = 19 ||
| q | null | null | null | null | q_5 = s / i_5 =  20 | s = 103 |
| r | null | null | null | null | r_5 = s % i_5 = 3 ||

当 i = 4 时，有 `q_4 = q_5 / i = 20/4 = 5, r_4 = q_5 % i = 20%4 = 0`。也就是把上一轮的商作为本轮的被除数。本轮之后列表 selected_cards 为 [12, 18, 50]。

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | null | null | null | reordered_cards[1] = 4 | 19 ||
| q | null | null | null | q_4 = q_5 / i_4 = 5 | q_5 = 20 | s = 103 |
| r | null | null | null | r_4 = q_5 % i_4 = 0 | r_5 = 3 ||

当 i = 3 时，有 `q_3 = q_4 / i = 5/3 = 1, r_3 = q_4 % i = 5%3 = 2`。本轮之后列表 selected_cards 为 [12, 18]。

| i | 1 | 2 | 3 | 4 | 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | null | null | 50 | 4 | 19 ||
| q | null | null | q_3 = 1 | q_4 = 5 | q_5 = 20 | s = 103 |
| r | null | null | r_3 = 2 | r_4 = 0 | r_5 = 3 ||

当 i = 2 时，有 `q_2 = q_3 / i = 1/2 = 0, r_2 = q_3 % i = 1%2 = 1`。本轮之后列表 selected_cards 为 [12]。

| i | 1 | 2 | 3 | 4 | 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | null | 18 | 50 | 4 | 19 ||
| q | null | q_2 = 0  | q_3 = 1 | q_4 = 5 | q_5 = 20 | s = 103 |
| r | null | r_2 = 1  | r_3 = 2 | r_4 = 0 | r_5 = 3 ||

当 i = 2 时，有 `q_1 = q_2 / i = 0/1 = 0, r_1 = q_2 % i = 0%1 = 0`。本轮之后列表 selected_cards 为 []。

| i | 1 | 2 | 3 | 4 | 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | 19 ||
| q | q_1 = 0 | q_2 = 0  | q_3 = 1 | q_4 = 5 | q_5 = 20 | s = 103 |
| r | r_1 = 0 | r_2 = 1  | r_3 = 2 | r_4 = 0 | r_5 = 3 ||

</details>

最终，输出一个列表 reordered_cards = [12, 18, 50, 4, 19]

第四步，我们对第三步中得到的编码好的列表 [12, 18, 50, 4, 19] 进行分割，前 4 张牌送入解码器中，看看解码器能否算出第 5 张牌是什么。

第五步，将前 4 张牌解码。此步相当于第三步的逆过程。我们将牌组按如下规则进行解码：

```python
for i in range(1, 5, 1):
    q_list[i] = i * q_list[i-1] + r_list[i-1]
    if i != 4:
        visible_cards.append(first_four[i])
        r_list[i] = sorted(visible_cards).index(first_four[i])
    else:
        continue
```

为了理解这一步做了什么，我们将上述循环过程展开。

<details>
<summary style="outline: none;"><font color='blueviolet'>点击查看每轮迭代中的细节</font></summary>

当 i = 1 时，有 q_1 = 0, r_1 = 0（证明略，提示：s < 5!）。其次，由已知的前 4 张牌 [12, 18, 50, 4]，我们知道：

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | null ||
| q | q_1 = 0 | null | null | null | null | s = null |
| r | r_1 = 0 | null | null | null | null ||

当 i = 2 时，有 `q_2 = i_1 * q_1 + r_1 = 0, r_2 = [12, 18].index(18) = 1`。

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | null ||
| q | q_1 = 0 | q_2 = 0 | null | null | null | s = null |
| r | r_1 = 0 | r_2 = 1 | null | null | null ||

当 i = 3 时，有 `q_3 = i_2 * q_2 + r_2 = 1, r_3 = [12, 18, 50].index(50) = 2`。

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | null ||
| q | q_1 = 0 | q_2 = 0 | q_3 = 1 | null | null | s = null |
| r | r_1 = 0 | r_2 = 1 | r_3 = 2 | null | null ||

当 i = 4 时，有 `q_4 = i_3 * q_3 + r_3 = 5, r_4 = [4, 12, 18, 50].index(4) = 0`。

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | null ||
| q | q_1 = 0 | q_2 = 0 | q_3 = 1 | q_4 = 5 | null | s = null |
| r | r_1 = 0 | r_2 = 1 | r_3 = 2 | r_4 = 0 | null ||

当 i = 5 时，有 `q_5 = i_4 * q_4 + r_4 = 20`。

| i | i_1 = 1 | i_2 = 2 | i_3 = 3 | i_4 = 4 | i_5 = 5 ||
| --- | --- | --- | --- | --- | --- | --- |
| card | 12 | 18 | 50 | 4 | null ||
| q | q_1 = 0 | q_2 = 0 | q_3 = 1 | q_4 = 5 | q_5 = 20 | s = null |
| r | r_1 = 0 | r_2 = 1 | r_3 = 2 | r_4 = 0 | r_5 = null ||

</details>

第六步，推测第五张牌的取值范围。

经过迭代后，我们知道 `$ q_5 = 20 $`，虽然不知道 r_5 等于多少，但是我们知道 r_5 的范围为 `$ 0 \leq r_5 \leq 4 $`。又因为 `$s = 5 * q_5 + r_5 $`, 故有 `$ 100 \leq s \leq 104 $`。

此外，我们还知道一个不等式。设第五张牌的值为 v。由于 s = (v + sum([12, 18, 50, 4]))，我们有：
`$$ 100 \leq (v + sum([12, 18, 50, 4])) \bmod 5! \leq 104 \\ 100 \leq (v + 84) \bmod 5! \leq 104 \\ 16 \leq v \bmod 120 \leq 20 $$`
又 `$ 1 \leq v \leq 52 $`，故：
`$$ 16 \leq v \leq 20 $$`
上述过程的代码如下：
```python
# 总结当前信息
sum_of_first_four = sum(first_four)
q = q_list[-1]

# 计算编码时q的初始值s的范围
range_l = 5 * q_list[-1]  # range_l <= s的值
range_r = 5 * q_list[-1] + 4  # s的值 <= range_r

# 计算第五张牌的值v的范围
times = 0
while True:
    v_l = range_l + times * factorial(5) - sum_of_first_four
    v_r = range_r + times * factorial(5) - sum_of_first_four
    times += 1
    if (v_r >= 1) and (v_l <= 52):
        break
    elif times > 2:
        raise ValueError('can not find the range of v.')
```
第七步，尝试可行域中的每一种取值。唯一可行取值即为第五张牌的值。
```python
# 猜解码时第五次迭代的余数r
for v in range(v_l, v_r+1):
    if v not in first_four:
        temp = first_four[:]
        temp.append(v)
        test_r = sorted(temp).index(v)
        s = 5 * q + test_r
        guess_v = s + (times - 1) * factorial(5) - sum_of_first_four
        if v == guess_v:
            return v
```

参考：

1. [Chico and Dico](https://www.brand.site.co.il/riddles/200705q.html)
2. [Chico and Dico —— 根据任意4张扑克猜第5张牌](https://blog.csdn.net/makeway123/article/details/48055189)
