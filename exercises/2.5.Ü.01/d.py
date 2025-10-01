# Extract first two from list, add tuple's last if not present, then print
list_var = [1, "Zwei", 3.0]
tuple_var = (1, "Zwei", 3.0)
new_list = list_var[:2]
if tuple_var[-1] not in new_list:
    new_list.append(tuple_var[-1])
print(new_list)