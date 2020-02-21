import random


def factorial(n):
    """计算n的阶乘"""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)


def encode(selected_cards):
    """将第五张牌的牌面信息编码到前四张牌的排列顺序中"""

    # 初始化
    selected_cards = sorted(selected_cards)
    reordered_cards = []
    s = sum(selected_cards) % factorial(5)
    # print('real s:', s)

    q = s  # 一般情况下，q 代表商（本次除外），r 代表余数。
    for i in range(5, 0, -1):
        q, r = divmod(q, i)
        reordered_cards.append(selected_cards.pop(r))

    return reordered_cards


def process(reordered_cards):
    """将牌组翻转，并取出前四张牌"""
    reordered_cards.reverse()
    return reordered_cards[:-1], reordered_cards[-1]


def decode(first_four):
    """将第五张牌的牌面信息从前四张牌的排列顺序中解码出来"""

    # 初始化
    visible_cards = [first_four[0]]  # 解码时每轮迭代能看到的所有牌
    q_list = [0, None, None, None, None]  # 解码时第一轮迭代的商为0，故q_list[0] = 0
    r_list = [0, None, None, None, None]  # 解码时第一轮迭代的余数为0，故r_list[0] = 0

    # 依次解码出每轮迭代中的商和余数
    # 从第二轮开始迭代
    for i in range(1, 5, 1):
        q_list[i] = i * q_list[i-1] + r_list[i-1]
        if i != 4:
            visible_cards.append(first_four[i])
            r_list[i] = sorted(visible_cards).index(first_four[i])
        else:
            continue

    # 总结当前信息
    sum_of_first_four = sum(first_four)
    q = q_list[-1]
    # print('sum_of_first_four:', sum_of_first_four)
    # print('q:', q_list[-1])

    # 计算编码时q的初始值s的范围
    range_l = 5 * q_list[-1]  # range_l <= s的值
    range_r = 5 * q_list[-1] + 4  # s的值 <= range_r
    # print(range_l, '<= s <=', range_r)

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

    return -1


def main():
    """主函数"""

    cards = [c for c in range(1, 53)]
    selected_cards = random.sample(cards, 5)
    # selectedCards = [13, 19, 28, 44, 49]
    # selectedCards = [32, 22, 38, 2, 46]
    # selectedCards = [34, 6, 44, 35, 7]
    # selectedCards = [15, 22, 10, 30, 14]
    # selected_cards = [19, 37, 34, 21, 24]
    # selected_cards = [18, 50, 12, 19, 4]

    print('selected_cards:', selected_cards)
    # print('sorted_cards:', sorted(selected_cards))
    reordered_cards = encode(selected_cards)
    first_four, answer = process(reordered_cards)
    print('first_four:', first_four)
    # print('answer:', answer)
    # print('*' * 30)
    value = decode(first_four)
    print('guess_value:', value)
    # print('*' * 30)
    print('success:', answer == value)
    return value


if __name__ == '__main__':
    pass
    # main()
