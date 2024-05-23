test_dict = json.loads(input())

min_key = min(test_dict, key=test_dict.get)
max_key = max(test_dict, key=test_dict.get)

print("min:", min_key)
print("max:", max_key)
