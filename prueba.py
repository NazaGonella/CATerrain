def get_max_key(d):
    return max(d, key=d.get)

# Example usage
data = {"hello": 4, "bye": 10, "yes": 9}
print(get_max_key(data))  # Output: "yes"
