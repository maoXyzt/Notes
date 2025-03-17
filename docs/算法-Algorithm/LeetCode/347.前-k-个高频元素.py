#
# @lc app=leetcode.cn id=347 lang=python3
#
# [347] 前 K 个高频元素
#
# https://leetcode-cn.com/problems/top-k-frequent-elements/description/
#
# algorithms
# Medium (59.01%)
# Likes:    210
# Dislikes: 0
# Total Accepted:    29.5K
# Total Submissions: 49.9K
# Testcase Example:  '[1,1,1,2,2,3]\n2'
#
# 给定一个非空的整数数组，返回其中出现频率前 k 高的元素。
# 
# 示例 1:
# 
# 输入: nums = [1,1,1,2,2,3], k = 2
# 输出: [1,2]
# 
# 
# 示例 2:
# 
# 输入: nums = [1], k = 1
# 输出: [1]
# 
# 说明：
# 
# 
# 你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。
# 你的算法的时间复杂度必须优于 O(n log n) , n 是数组的大小。
# 
# 
#

"""
思路：
可将这个问题分解为2个问题：
1) 统计每个整数出现的次数;
2) 获取前k个最大的值。

第一步，确定每个整数出现的次数，可以简单地用一个字典对象维护每个值出现的次数。
遍历数组，每个数字出现时就给它的计数+1。

第二步，将每个整数出现的次数构建一个堆，依次取出堆的前k个元素。
"""
from typing import List
import heapq

# @lc code=start
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return self.solution_2(nums, k)

    def solution_1(self, nums: List[int], k: int) -> List[int]:
        """
        自行实现堆结构
        结果：
        - 21/21 cases passed (148 ms)
        - Your runtime beats 37 % of python3 submissions
        - Your memory usage beats 7.35 % of python3 submissions (17.4 MB)
        """
        # 第一步：遍历数组，统计整数的出现次数
        # 时间复杂度：O(n)
        counts = {}
        for n in nums:
            counts[n] = counts.get(n, 0) + 1

        # 第二步：构建大根堆
        # 时间复杂度：O(nlogn)
        heap = BigRootHeap()
        for n, count in counts.items():
            node = Node(count, n)
            heap.push(node)

        # 第三步：依次取出前k个元素
        # 时间复杂度：O(logn)
        result = [heap.pop().value for _ in range(k)]
        return result

    def solution_2(self, nums: List[int], k: int) -> List[int]:
        """
        改进：使用小根堆，仅将最小的k个元素入堆，减小空间
        结果：
        - 21/21 cases passed (128 ms)
        - Your runtime beats 74.31 % of python3 submissions
        - Your memory usage beats 7.35 % of python3 submissions (17 MB)
        """
        # 第一步：遍历数组，统计整数的出现次数
        # 时间复杂度：O(n)
        counts = {}
        for n in nums:
            counts[n] = counts.get(n, 0) + 1

        # 第二步：构建小根堆
        # 时间复杂度：O(nlogn)
        # 堆的空间复杂度为常数级
        heap = SmallRootHeap()
        for n, count in counts.items():
            node = Node(count, n)
            if len(heap) >= k:
                if heap.root > node:
                    # 堆已经有k个元素，且新元素比堆中的最小元素小，则不需要入堆
                    continue
                else:
                    # 堆中最小元素出堆
                    heap.pop()
            heap.push(node)

        # 第三步：依次取出前k个元素，然后逆序
        # 时间复杂度：O(n)
        result = [heap.pop().value for _ in range(k)]
        result.reverse()
        return result

    def solution_3(self, nums: List[int], k: int) -> List[int]:
        """
        用python自带的堆结构
        结果：
        - 21/21 cases passed (124 ms)
        - Your runtime beats 81.98 % of python3 submissions
        - Your memory usage beats 7.35 % of python3 submissions (17.3 MB)
        """
        # 第一步：遍历数组，统计整数的出现次数
        counts = {}
        for n in nums:
            counts[n] = counts.get(n, 0) + 1
        nodes = (Node(count, num) for num, count in counts.items())

        # 第二步，用python自带的堆结构完成建堆和取前k个值
        n_largest = heapq.nlargest(k, nodes)
        return [x.value for x in n_largest]

    def solution_4(self, nums: List[int], k: int) -> List[int]:
        """
        用python自带的Counter类
        结果：
        - 21/21 cases passed (116 ms)
        - Your runtime beats 94.86 % of python3 submissions
        - Your memory usage beats 7.35 % of python3 submissions (17.3 MB)
        """
        from collections import Counter
        return [x[0] for x in Counter(nums).most_common(k)]


class Node:
    """堆节点对象"""
    __slots__ = ('value', '_order')

    def __init__(self, order, value):
        self._order = order
        self.value = value

    def __gt__(self, other):
        """定义 > 操作符"""
        return self._order > other._order

    def __lt__(self, other):
        """定义 < 操作符"""
        return self._order < other._order


class BigRootHeap:
    """基于数组实现的大根堆"""
    def __init__(self):
        self._nodes = []

    def __len__(self):
        return len(self._nodes)

    @property
    def root(self):
        if self._nodes:
            return self._nodes[0]
        else:
            return None

    @staticmethod
    def get_parent_rank(rank: int):
        """获取父节点"""
        if rank > 0:
            return (rank - 1) // 2
        else:
            return None

    @staticmethod
    def get_left_child_rank(rank: int):
        """获取左子节点"""
        return rank * 2 + 1

    @staticmethod
    def get_right_child_rank(rank: int):
        """获取右子节点"""
        return rank * 2 + 2

    def push(self, node: Node):
        """向堆添加节点"""
        if not self._nodes:
            self._nodes = [node]
        else:
            # 添加到堆的末尾
            self._nodes.append(node)
            # 添加新元素后调整堆，以维持堆的性质
            self.heapify_up(len(self._nodes) - 1)

    def heapify_up(self, rank: int):
        """检查节点与其父节点是否满足大根堆的性质，如果不满足则调整"""
        if rank == 0:
            # 已经是根节点，不用调整
            return
        else:
            parent_rank = self.get_parent_rank(rank)
            if self._nodes[rank] > self._nodes[parent_rank]:
                # 将节点与父节点交换
                self._nodes[rank], self._nodes[parent_rank] = \
                    self._nodes[parent_rank], self._nodes[rank]
                # 递归对祖先节点进行调整，最大调整次数：logn
                self.heapify_up(parent_rank)
            else:
                # 当前节点与其父节点的关系不需要调整
                return

    def pop(self):
        """弹出当前堆顶元素"""
        if self._nodes:
            # 将末位元素交换到堆顶，取出最后一个元素
            self._nodes[0], self._nodes[-1] = self._nodes[-1], self._nodes[0]
            res = self._nodes.pop()
            # 从堆顶开始调整，维持堆性质
            self.heapify_down(0)
            return res

    def heapify_down(self, rank: int):
        """检查节点与其子节点是否满足大根堆的性质，如果不满足则调整"""
        if rank >= len(self._nodes) // 2:
            # 当前节点已经没有子节点了
            return
        else:
            lc_child_rank = self.get_left_child_rank(rank)
            # 如果当前节点比左子节点或右子节点小，则将其与最大的子节点交换，然后到相应的子节点位置继续调整。最大调整次数：logn
            biggest_rank = rank
            if self._nodes[biggest_rank] < self._nodes[lc_child_rank]:
                biggest_rank = lc_child_rank
            rc_child_rank = self.get_right_child_rank(rank)
            if rc_child_rank < len(self._nodes) and self._nodes[biggest_rank] < self._nodes[rc_child_rank]:
                biggest_rank = rc_child_rank

            if biggest_rank != rank:
                self._nodes[rank], self._nodes[biggest_rank] = \
                        self._nodes[biggest_rank], self._nodes[rank]
                self.heapify_down(biggest_rank)
            else:
                return


class SmallRootHeap(BigRootHeap):
    def heapify_up(self, rank: int):
        """检查节点与其父节点是否满足小根堆的性质，如果不满足则调整"""
        if rank == 0:
            # 已经是根节点，不用调整
            return
        else:
            parent_rank = self.get_parent_rank(rank)
            if self._nodes[rank] < self._nodes[parent_rank]:
                # 将节点与父节点交换
                self._nodes[rank], self._nodes[parent_rank] = \
                    self._nodes[parent_rank], self._nodes[rank]
                # 递归对祖先节点进行调整，最大调整次数：logn
                self.heapify_up(parent_rank)
            else:
                # 当前节点与其父节点的关系不需要调整
                return

    def heapify_down(self, rank: int):
        """检查节点与其子节点是否满足大根堆的性质，如果不满足则调整"""
        if rank >= len(self._nodes) // 2:
            # 当前节点已经没有子节点了
            return
        else:
            lc_child_rank = self.get_left_child_rank(rank)
            # 如果当前节点比左子节点或右子节点小，则将其与最大的子节点交换，然后到相应的子节点位置继续调整。最大调整次数：logn
            smallest_rank = rank
            if self._nodes[smallest_rank] > self._nodes[lc_child_rank]:
                smallest_rank = lc_child_rank
            rc_child_rank = self.get_right_child_rank(rank)
            if rc_child_rank < len(self._nodes) and self._nodes[smallest_rank] > self._nodes[rc_child_rank]:
                smallest_rank = rc_child_rank

            if smallest_rank != rank:
                self._nodes[rank], self._nodes[smallest_rank] = \
                        self._nodes[smallest_rank], self._nodes[rank]
                self.heapify_down(smallest_rank)
            else:
                return

# @lc code=end
