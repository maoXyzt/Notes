#
# @lc app=leetcode.cn id=300 lang=python3
#
# [300] 最长上升子序列
#
# https://leetcode-cn.com/problems/longest-increasing-subsequence/description/
#
# algorithms
# Medium (43.35%)
# Likes:    374
# Dislikes: 0
# Total Accepted:    40.4K
# Total Submissions: 92.8K
# Testcase Example:  '[10,9,2,5,3,7,101,18]'
#
# 给定一个无序的整数数组，找到其中最长上升子序列的长度。
#
# 示例:
#
# 输入: [10,9,2,5,3,7,101,18]
# 输出: 4
# 解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
#
# 说明:
#
#
# 可能会有多种最长上升子序列的组合，你只需要输出对应的长度即可。
# 你算法的时间复杂度应该为 O(n^2) 。
#
#
# 进阶: 你能将算法的时间复杂度降低到 O(n log n) 吗?
#
#
from typing import List

# @lc code=start


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        return self.solution2(nums)
    
    def solution1(self, nums: List[int]) -> int:
        """
        动态规划法，最差情况（输入序列有序）的时间复杂度为O(n^2)
        结果：
        24/24 cases passed (1196 ms)
        - Your runtime beats 33.13 % of python3 submissions
        - Your memory usage beats 99.54 % of python3 submissions (12.8 MB)
        """
        seq_len = []    # 列表第i位表示以第i个数结尾的序列的长度
        max_len = 0
        # 遍历输入数组的每个数字x，如果当前数字x比之前的数字y大，则x可以接在y后面组成新的上升子序列，
        # 新的子序列长度是以y结尾的最长子序列的长度+1。
        for i in range(len(nums)):
            x = nums[i]
            max_len_end_with_x = 1
            for j in range(i):
                y = nums[j]
                if y < x:
                    len_end_with_x = seq_len[j] + 1
                    if len_end_with_x > max_len_end_with_x:
                        max_len_end_with_x = len_end_with_x
            seq_len.append(max_len_end_with_x)
            if max_len_end_with_x > max_len:
                max_len = max_len_end_with_x
        return max_len

    def solution2(self, nums: List[int]) -> int:
        """
        O(nlogn)的解法
        关键思路：
        seq_x 列表第i位表示长度为i+1的上升子序列中，末尾值最小的那一个值。
        seq_x 中的后一个值一定比前一个值大，即seq_x是有序的。
        在遍历nums的过程中，用二分查找法找到当前值x在seq_x中的位置i。
        x接在位置i表示的的序列（长度为i+1）后面可以构成长度为i+2的序列，而且这个序列比原来的长度为i+2的序列的最后一个值小。

        24/24 cases passed (48 ms)
        Your runtime beats 91.8 % of python3 submissions
        Your memory usage beats 99.54 % of python3 submissions (12.7 MB)
        """
        size = len(nums)
        seq_x = []      # 列表第i位表示长度为i+1的上升子序列中，末尾值最小的那一个值
        for i in range(size):
            x = nums[i]
            # 用二分查找法确定x在seq_x中的哪个位置
            # 时间复杂度：O(logn)
            i_low = 0
            i_high = len(seq_x)
            k = (i_low + i_high) // 2
            while(i_low < i_high):
                if seq_x[k] < x:
                    i_low = k + 1
                else:
                    i_high = k
                k = (i_low + i_high) // 2
            if i_low == len(seq_x):
                seq_x.append(x)
            else:
                seq_x[i_low] = x

        return len(seq_x)

# @lc code=end