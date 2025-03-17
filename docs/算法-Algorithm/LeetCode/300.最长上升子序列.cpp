/*
 * @lc app=leetcode.cn id=300 lang=cpp
 *
 * [300] 最长上升子序列
 *
 * https://leetcode-cn.com/problems/longest-increasing-subsequence/description/
 *
 * algorithms
 * Medium (43.35%)
 * Likes:    374
 * Dislikes: 0
 * Total Accepted:    40.4K
 * Total Submissions: 92.8K
 * Testcase Example:  '[10,9,2,5,3,7,101,18]'
 *
 * 给定一个无序的整数数组，找到其中最长上升子序列的长度。
 * 
 * 示例:
 * 
 * 输入: [10,9,2,5,3,7,101,18]
 * 输出: 4 
 * 解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
 * 
 * 说明:
 * 
 * 
 * 可能会有多种最长上升子序列的组合，你只需要输出对应的长度即可。
 * 你算法的时间复杂度应该为 O(n^2) 。
 * 
 * 
 * 进阶: 你能将算法的时间复杂度降低到 O(n log n) 吗?
 * 
 */
#include <vector>

// @lc code=start
class Solution
{
public:
    /* 24/24 cases passed (40 ms)
     * Your runtime beats 69.9 % of cpp submissions
     * Your memory usage beats 42.44 % of cpp submissions (8.6 MB)
     */
    int lengthOfLIS(vector<int> &nums)
    {
        vector<int> seq_len;
        int max_len = 0;
        for (int i = 0; i < nums.size(); i++)
        {
            auto x = nums[i];
            int max_len_x = 1;
            for (int j = 0; j < i; j++)
            {
                auto y = nums[j];
                if (x > y)
                {
                    int len_x = 1 + seq_len[j];
                    if (max_len_x < len_x)
                        max_len_x = len_x;
                }
            }
            seq_len.push_back(max_len_x);
            if (max_len < max_len_x)
                max_len = max_len_x;
        }
        return max_len;
    };
};
// @lc code=end
