# def getOpenApplication(commands):
#     open_apps = []
#     for cmd in commands:
#         tokens = cmd.split()
#         if tokens[0] == "open":
#             app = tokens[1]
#             open_apps.append(app)
#         elif tokens[0]=="close":
#             k = int(tokens[1])
#             if k>=len(open_apps):
#                 open_apps=[]
#             else:
#                 open_apps=open_apps[:k]
#         elif tokens[0] == "clear":
#             open_apps = []

#     print(open_apps)
#     return open_apps

# if __name__ == '__main__':
#     get_commands = getOpenApplication(["open firefox","open terminal","opem curl","close 2","open ps"])

def has_repeated_digits(number):
    # Convert the number to a string to check for repeated digits
    num_str = str(number)
    return len(num_str) != len(set(num_str))

def numbers_with_no_repeated_digits(m, n):
    result = []
    for num in range(m, n + 1):
        if not has_repeated_digits(num):
            result.append(num)
    return result
m = 80
n = 120

result_numbers = numbers_with_no_repeated_digits(m, n)
count = len(result_numbers)

print(f'The number of numbers between {m} and {n} with no repeated digits is: {count}')
print(f'These numbers are: {result_numbers}')




