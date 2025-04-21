import time
import multiprocessing
import string
import os
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
symbols = string.punctuation
all_charset = lowercase + uppercase + digits + symbols
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')
def get_position_charset(password):
    position_charsets = []
    for char in password:
        if char in lowercase:
            position_charsets.append(lowercase)
        elif char in uppercase:
            position_charsets.append(uppercase)
        elif char in digits:
            position_charsets.append(digits)
        elif char in symbols:
            position_charsets.append(symbols)
        else:
            position_charsets.append(all_charset) 
    return position_charsets
def brute_force_chunk_mp(start_index, chunk_size, target_password, position_charsets):
    chars_at_positions = [len(c) for c in position_charsets]
    current_combo = [0] * len(position_charsets)
    for _ in range(start_index):
        for i in range(len(position_charsets) - 1, -1, -1):
            current_combo[i] += 1
            if current_combo[i] >= chars_at_positions[i]:
                current_combo[i] = 0
            else:
                break
    for _ in range(chunk_size):
        guess = ''.join(position_charsets[i][current_combo[i]] for i in range(len(position_charsets)))
        if guess == target_password:
            return guess
        for i in range(len(position_charsets) - 1, -1, -1):
            current_combo[i] += 1
            if current_combo[i] >= chars_at_positions[i]:
                current_combo[i] = 0
            else:
                break
    return None
def brute_force_parallel_mp(target_password):
    position_charsets = get_position_charset(target_password)
    num_workers = multiprocessing.cpu_count()
    chunk_size = 100000 
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.starmap(
            brute_force_chunk_mp,
            [(i * chunk_size, chunk_size, target_password, position_charsets)
             for i in range(num_workers)])

        for result in results:
            if result:
                print(f"Found password: {result}")
                return result
    return None
def main():
    target_password = input("Enter the password to brute-force: ").strip()
    start_time = time.time()
    print("Starting brute-force attack...")
    found_password = brute_force_parallel_mp(target_password) 
    if found_password:
        print(f"Password found: {found_password}")
    else:
        print("")
    print(f"Combination has been located in {time.time() - start_time:.2f} seconds")
if __name__ == "__main__":
    main()
