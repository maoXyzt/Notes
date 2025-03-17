#
# @lc app=leetcode.cn id=162 lang=python3
#
# [162] 寻找峰值
#
# https://leetcode-cn.com/problems/find-peak-element/description/
#
# algorithms
# Medium (43.09%)
# Likes:    129
# Dislikes: 0
# Total Accepted:    23.7K
# Total Submissions: 54.5K
# Testcase Example:  '[1,2,3,1]'
#
# 峰值元素是指其值大于左右相邻值的元素。
# 
# 给定一个输入数组 nums，其中 nums[i] ≠ nums[i+1]，找到峰值元素并返回其索引。
# 
# 数组可能包含多个峰值，在这种情况下，返回任何一个峰值所在位置即可。
# 
# 你可以假设 nums[-1] = nums[n] = -∞。
# 
# 示例 1:
# 
# 输入: nums = [1,2,3,1]
# 输出: 2
# 解释: 3 是峰值元素，你的函数应该返回其索引 2。
# 
# 示例 2:
# 
# 输入: nums = [1,2,1,3,5,6,4]
# 输出: 1 或 5 
# 解释: 你的函数可以返回索引 1，其峰值元素为 2；
# 或者返回索引 5， 其峰值元素为 6。
# 
# 
# 说明:
# 
# 你的解法应该是 O(logN) 时间复杂度的。
# 
#

# @lc code=start
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        return self.solution_2(nums)
    
    def solution_1(self, nums: List[int]) -> int:
        """
        59/59 cases passed (32 ms)
        Your runtime beats 98.4 % of python3 submissions
        Your memory usage beats 57.91 % of python3 submissions (13.1 MB)
        """
        n = len(nums)
        res = 0
        for i in range(1, n):
            a = nums[i - 1]
            b = nums[i]
            if a < b:
                if i + 1 >= n or nums[i+1] < b:
                    res = i
                    break
        return res
    
    def solution_2(self, nums: List[int]) -> int:
        """
        59/59 cases passed (28 ms)
        Your runtime beats 99.4 % of python3 submissions
        Your memory usage beats 57.34 % of python3 submissions (13.3 MB)
        """
        a = 0
        b = len(nums) - 1
        while True:
            if (b - a) <= 1:
                return a if nums[a] > nums[b] else b
            mid = (b + a) // 2
            if nums[mid - 1] > nums[mid]:
                b = mid
            else:
                a = mid

# @lc code=end

