def find_largest_num_using_for(lst):
    largest = lst[0]

    for val in lst:
        if val > largest:
            largest = val
    
    return largest

print(find_largest_num_using_for([34, 15, 88, 2]))
