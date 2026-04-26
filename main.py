import random

def calculate_luhn_check_digit(number_str):
    """
    Calculates the required check digit to make the number Luhn-valid.
    """
    digits = [int(d) for d in number_str]
    # Multiply every second digit by 2 starting from the right
    for i in range(len(digits) - 1, -1, -2):
        val = digits[i] * 2
        digits[i] = val if val < 10 else val - 9
    
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    return check_digit

def generate_imeis(prefix, count=50000):
    """
    Generates N IMEIs based on a prefix using the Luhn Algorithm.
    """
    imeis = []
    # IMEI is usually 15 digits. Prefix is 8 digits, we need 6 random + 1 check digit.
    for _ in range(count):
        # Generate 6 random digits
        body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Calculate the 15th digit (Luhn)
        check_digit = calculate_luhn_check_digit(body)
        imeis.append(body + str(check_digit))
    return imeis

# Execution
if __name__ == "__main__":
    PREFIX = "35390744"
    QUANTITY = 50000
    
    print(f"[*] Generating {QUANTITY} IMEIs starting with {PREFIX}...")
    generated_list = generate_imeis(PREFIX, QUANTITY)
    
    # Save to file for performance (printing 50k lines is slow)
    with open("imeis_generated.txt", "w") as f:
        f.write("\n".join(generated_list))
    
    print(f"[+] Done! Sample: {generated_list[0]}")