# class Solution:
#     def remove_duplicates(self, A, N):
#         if N == 0:
#             return 0

#         result = 0

#         for i in range(1, N):
#             if A[i] != A[i - 1]:
#                 result += 1
#                 A[result] = A[i]

#         return result + 1

# sorted_array = [1, 1, 2, 2, 2, 3, 4, 4, 5]
# solution = Solution()
# N = solution.remove_duplicates(sorted_array, len(sorted_array))
# print(sorted_array[:N])

# class Solution:
#     def subArraySum(self,arr, n, s): 
#         left = 0
#         current_sum = 0

#         for right in range(n):
#             current_sum += arr[right]

#             while current_sum > s:
#                 current_sum -= arr[left]
#                 left += 1

#             if current_sum == s:
#                 if right == 0:
#                     return -1
                    
#                 elif left > right:
#                     return -1
#                 else:
#                 # Adding 1 to the indices for 1-based indexing
#                     return [left + 1, right + 1]


# # Example usage with multiple test cases:
# test_cases = [
#     ([1, 2, 3, 4], 4, 9),
#     ([1, 2, 3, 4], 4, 0),
# ]

# solution = Solution()

# for arr, n, s in test_cases:
#     result = solution.subArraySum(arr, n, s)
#     print(result)



def numberOfTokens(expiryLimit, commands):
    active = {}

    for command, token_id, T in commands:
        if command == 0: # get
            active[token_id] = T + expiryLimit
        else: # reset
            if token_id in active:
                if active[token_id] >= T:
                    active[token_id] = T + expiryLimit
                else:
                    del active[token_id]

    for token_id, time in active.items():
        if time < T:
            del active[token_id]
            
    return len(active)


expiryLimit = 3
commands = [[0,1,1],[1,1,5]]

# result = numberOfTokens(expiryLimit, commands)
# print(result)

def getMinSubsequences(input_str):
    count = 0
    i = 0
    n = len(input_str)
    
    while i < n:
        count += 1
        if i < n - 1 and input_str[i] == input_str[i + 1]:
            i += 1
        i += 1
    
    return count

# # Example usage
# input_str = "101"
# result = getMinSubsequences(input_str)
# print("Minimum number of special subsequences:", result)


# -----------------------------------------------------------------


# def split_and_check_special_strings(binary_string):
#     result = []
#     n = len(binary_string)
    
#     # Split the binary string into sequences of 3 characters.
#     for i in range(0, n, 3):
#         sequence = binary_string[i:i+3]
#         result.append(sequence)

#     for i in range(0, len(result)):
#         if len(result[i]) == 1:
#             print(f'Special string : {result[i]}')
#         elif result[i] == result[i - 1]:
#             print(f'Special string : {result[i]}')
#         else:
#             print(f'Non special string : {result[i]}')

#     return result

# binary_string = '0110011'
# sequences = split_and_check_special_strings(binary_string)

# print(sequences)

# ---------------------------------------------------------------------------------------------------

# def is_special_sequence(sequence):
#     # Check if the sequence is a special sequence.
#     for i in range(1, len(sequence)):
#         if sequence[i] == sequence[i - 1]:
#             return False
#     return True

# def split_and_find_min_special_sequences(binary_string):
#     n = len(binary_string)
#     min_special_sequences = n  # Initialize with a large value.

#     # Try splitting the binary string into sequences of decreasing lengths.
#     for seq_length in range(3, 0, -1):
#         result = []
#         for i in range(0, n, seq_length):
#             sequence = binary_string[i:i+seq_length]
#             result.append(sequence)
        
#         print(f"The splits are : {result}")
#         special_sequences = [seq for seq in result if is_special_sequence(seq)]
#         print(f"The special sequences are : {special_sequences}")
#         num_special_sequences = len(special_sequences)

#         if num_special_sequences < min_special_sequences:
#             min_special_sequences = num_special_sequences

#     print(f'The result : {num_special_sequences}')

#     return num_special_sequences

# binary_string = '0110011'
# min_special_sequences = split_and_find_min_special_sequences(binary_string)

# print(f'Minimum number of special sequences: {min_special_sequences}')

def equalize(nums):
    n = len(nums)

    # Step 1: Find the median
    nums.sort()
    median = nums[n // 2]

    # Step 2: Calculate the cost
    total_cost = sum(abs(num - median) for num in nums)

    return total_cost


# def equalize(power):
#     n = len(power)
#     total_power = sum(power)
#     target_power = total_power // n  # Calculate the target power for all robots.
#     minutes = 0


#     for p in power:
#         minutes += abs(p - target_power)  # Calculate the time to adjust each robot.



#     return minutes

 

# Example usage:
# power = [10,10,20,30,40,50,51,52,53,54,55]
# result = equalize(power)
# print(result)  # This will output 12

# [12:14] Xavier, Benson P


# def compareStrings(s1, s2):
#     def removeBackspace(s):
#         n = len(s)
#         idx = 0
#         for i in range(0, n):
#             if(s[i] != '#'):
#                 s = s[:idx] + s[i] + s[idx+1:]
#                 idx += 1
#             elif(s[i] == '#' and idx >= 0):
#                 idx -= 1
#             if(idx < 0):
#                 idx = 0
#         ans = ""
#         for i in range(0, idx):
#             ans += s[i]
#         return ans


#     red_string1 = removeBackspace(s1)
#     red_string2 = removeBackspace(s2)

#     if red_string1 == red_string2:
#         return 1

#     return 0

# s1 = 'yf#c#'
# s2 = 'yy#k#pp##' 
# # compareStrings(s1, s2)
# result = compareStrings(s1, s2)
# print(result)


def is_vowel(char):
    return char in 'aeiou'

def build_prefix_array(strArr):
    n = len(strArr)
    prefix_count = [0] * (n + 1)

    for i in range(1, n + 1):
        prefix_count[i] = prefix_count[i - 1] + int(is_vowel(strArr[i - 1][0]))

    return prefix_count

def hasVowels(strArr, query):
    prefix_count = build_prefix_array(strArr)
    start, end = map(int, query.split('-'))
    
    # Check if the indices are within bounds
    if 1 <= start <= end <= len(strArr):
        result = prefix_count[end] - prefix_count[start - 1]
        return result
    else:
        return 0

# Example usage
# strArr = ['abal', 'boblece', 'aa', 'eg']
# queries = ['1-3', '2-5', '11-12', '2-2', '7-7']

# results = [hasVowels(strArr, query) for query in queries]
# print(results)  # Output: [2, 3, 0, 0, 1]


# def hasVowels(strArr, queries):
#     vowels = set('aeiou')
#     result = []
    
#     for query in queries:
#         l, r = map(int, query.split('-'))
#         count = 0
#         for i in range(l - 1, r):
#             if strArr[i][0] in vowels and strArr[i][-1] in vowels:
#                 count += 1
#         result.append(count)
    
#     return result

# strArr = ['aba', 'bcb', 'ece', 'aa', 'e']
# queries = ['1-3', '2-5', '2-2']

# result = hasVowels(strArr, queries)
# print(result)  # Output: [2, 3, 0]


def hasVowels(strArr, queries):
    vowels = set('aeiou')
    result = []
    
    n = len(strArr)
    vowel_starts = [0] * n
    for i in range(n):
        if strArr[i][0] in vowels:
            vowel_starts[i] = 1
        if i > 0:
            vowel_starts[i] += vowel_starts[i - 1]
    
    for query in queries:
        l, r = map(int, query.split('-'))
        if l == 1:
            count = vowel_starts[r - 1]
        else:
            count = vowel_starts[r - 1] - vowel_starts[l - 2]
        result.append(count)
    
    return result

strArr = ['aba', 'bcb', 'ece', 'aa', 'e']
queries = ['1-3', '2-5', '2-2']

result = hasVowels(strArr, queries)
print(result)  # Output: [2, 3, 0]



def swap_case()