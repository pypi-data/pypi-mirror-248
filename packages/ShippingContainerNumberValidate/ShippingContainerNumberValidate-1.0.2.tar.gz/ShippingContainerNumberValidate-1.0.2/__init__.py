cntr_no_length = 11
letters_weight = {
    "A": 10, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16, "G": 17, "H": 18, "I": 19,
    "J": 20, "K": 21, "L": 23, "M": 24, "N": 25, "O": 26, "P": 27, "Q": 28, "R": 29,
    "S": 30, "T": 31, "U": 32, "V": 34, "W": 35, "X": 36, "Y": 37, "Z": 38
}
pow_two = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
letters_weight_keys = letters_weight.keys()

def validate_container_number(cntr_no):
    # Validate the length of the container number
    if len(cntr_no) != cntr_no_length:
        return "Not a valid container"
    # Split the string into first 4 characters
    final_sum = 0
    for ind, char in enumerate(cntr_no[:-1]):
        if char in letters_weight_keys:
            final_sum += letters_weight[char.upper()] * pow_two[ind]
        else:
            final_sum += int(char) * pow_two[ind]
    divided_by_eleven = final_sum//11
    multiply_by_eleven = divided_by_eleven * 11
    check_digit = final_sum - multiply_by_eleven
    if check_digit == int(cntr_no[-1]):
        return True
    return False

# class CntrLengthException(Exception):
#     def __init__(self, error):
#         self.error = error
