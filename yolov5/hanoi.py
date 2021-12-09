def hanoi(n):
    """
    非递归求解汉诺塔
    时间复杂度O(2^n)
    空间复杂度O(2^n)
        步骤列表的长度是2^n-1
        如果不返回步骤列表，只是打印出来，那么用到了一个长度为n的列表（pillar里面），空间复杂度为O(n)
    非递归说明：
        准备：
            首先把三根柱子按顺序排成品字型，把所有的圆盘按从大到小的顺序放在柱子0上。
            根据圆盘的数量确定柱子的排放顺序
                > 若n为偶数，按顺时针方向依次摆放 0 1 2；
                > 若n为奇数，按顺时针方向依次摆放 0 2 1。
        1. 按顺时针方向把最小的圆盘从当前的柱子移动到下一根柱子
        2. 把另外两根柱子上可以移动的圆盘移动到新的柱子上。
            即把非空柱子上的圆盘移动到空柱子上；
            当两根柱子都非空时，移动较小的圆盘。
        3. 反复进行步骤1、2，最后就能按规定完成汉诺塔的移动。
    :param n: 汉诺塔层数
    """

    names = ['A', 'B', 'C'] # 三根柱子的名字（从左到右）
    pillar = [list(range(n + 1, 0, -1)), [n + 1], [n + 1]]  # 三个柱子（均添加一个更大的盘，方便判断步骤2的移动方向）

    if n % 2 == 1:
        p = (0, 2, 1)
    else:
        p = (0, 1, 2)

    j, k = 0, 1  # j,k供步骤1使用：步骤一从p[j]号柱子 移动到 p[k]号柱子
    while True:
        # 1
        print(f'{names[p[j]]} --> {names[p[k]]}')  # 显示步骤
        pillar[p[k]].append(pillar[p[j]].pop())  # 移动
        j = k  # 更新j
        k += 1 if k != 2 else -2  # 更新k

        if len(pillar[-1]) == n + 1:  # 移动完成条件
            break

        # 2
        x, y = set(p) - {p[j]}  # 剩余两个柱子号
        if pillar[x][-1] < pillar[y][-1]:  # 小的向大的移动
            pillar[y].append(pillar[x].pop())  # 移动
            print(f'{names[x]} --> {names[y]}')  # 显示步骤
        else:
            pillar[x].append(pillar[y].pop())
            print(f'{names[y]} --> {names[x]}')


hanoi(3)

