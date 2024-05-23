groups = ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C']
num_groups = int(input())
group_sizes = [int(input()) for _ in range(num_groups)]
group_dict = {groups[i]: group_sizes[i] if i < num_groups else None for i in range(len(groups))}
print(group_dict)
