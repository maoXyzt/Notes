#
# @lc app=leetcode.cn id=5 lang=python3
#
# [5] 最长回文子串
#
# https://leetcode-cn.com/problems/longest-palindromic-substring/description/
#
# algorithms
# Medium (28.59%)
# Likes:    1775
# Dislikes: 0
# Total Accepted:    186.6K
# Total Submissions: 652.8K
# Testcase Example:  '"babad"'
#
# 给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。
# 
# 示例 1：
# 
# 输入: "babad"
# 输出: "bab"
# 注意: "aba" 也是一个有效答案。
# 
# 
# 示例 2：
# 
# 输入: "cbbd"
# 输出: "bb"
# 
# 
#

# @lc code=start
class Solution:
    def longestPalindrome(self, s: str) -> str:
        return self.solution_2(s)

    def solution_1(self, s: str) -> str:
        """
        动态规划方法
        103/103 cases passed (3684 ms)
        Your runtime beats 38.25 % of python3 submissions
        Your memory usage beats 43.29 % of python3 submissions (13.5 MB)
        """
        if not s:
            return ''

        # 在字符中间插入0，将字符串转成奇数长度的列表,
        # 插入的算上0后，回文子串一定是奇数长度。
        sl = []
        for x in s:
            sl.append(0)
            sl.append(x)
        sl.append(0)
        n = len(sl)

        n_longest = 1
        longest = [sl[1]]
        for i in range(1, n-1):
            # 判断以i位置为中心的，向左右延展j个字符的子串是否是回文子串
            j = 1
            while 0 <= i - j and i + j < n:
                if sl[i-j] == sl[i+j]:
                    if 2*j+1 > n_longest:
                        n_longest = 2*j+1
                        longest = sl[i-j:i+j+1]
                else:
                    break
                j += 1

        res = [x for x in longest if x != 0]
        return ''.join(res)

    def solution_2(self, s):
        """
        Manacher算法
        103/103 cases passed (92 ms)
        Your runtime beats 94.76 % of python3 submissions
        Your memory usage beats 42.86 % of python3 submissions (13.6 MB)
        """
        if not s:
            return ''

        # 在字符中间插入0，将字符串转成奇数长度的列表,
        # 插入的算上0后，回文子串一定是奇数长度。
        sl = []
        for x in s:
            sl.append(0)
            sl.append(x)
        sl.append(0)
        n = len(sl)

        # i位置的最长回文子串半径(从i-r[i]到i+r[i]的子串是回文)
        r = [0]*n
        i_longest = 0
        r_longest = 0

        # 当前已找出的可以构成回文子串的元素中，位置最后的元素的索引y
        #   以及该子串的中心元素位置i_y
        i_y = 0
        i_yc = 0
        for i in range(1, n-1):
            # 利用回文子串的对称性，判断半径的最小值，从而减少判断次数
            k_r = r[2*i_yc - i]
            if i + k_r < i_y:
                r[i] = k_r
                continue

            j = i_y - i
            # 判断以i位置为中心的，向左右延展j个字符的子串是否是回文子串
            while 0 <= i - j and i + j < n:
                if sl[i-j] == sl[i+j]:
                    r[i] = j
                    if j > r_longest:
                        i_longest = i
                        r_longest = j
                    if i+j > i_y:
                        i_y = i+j
                        i_yc = i
                else:
                    break
                j += 1

        res = [
            x
            for x in sl[i_longest-r[i_longest]:i_longest+r[i_longest]+1]
            if x != 0
        ]
        return ''.join(res)


# @lc code=end

