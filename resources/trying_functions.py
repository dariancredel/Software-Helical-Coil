
def convert(nums, converted, not_converted):
    error = False
    for i in range(len(nums)):
        try:
            result = float(nums[i])
        except ValueError as val_err:
            print(f"Error converting '{result}'")
            not_converted.append(result)
            error = True
            continue
        else:
            converted.append(result)

    return False if error else True

converted = []
not_converted = []
nums = ["0", 0, 1, 1.2, "1,2", 1, 1, 1]

print(convert(nums, converted, not_converted))
print("nums", nums)
print("converted", converted)
print("not_converted", not_converted)