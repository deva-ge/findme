def read_token_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"ფაილი '{filename}' ვერ მოიძებნა.")
        return None

if __name__ == "__main__":
    filename = 'token.txt'  # ტოკენის ფაილის სახელი
    access_token = read_token_from_file(filename)

    if access_token:
        print("ტოკენი წაკითხულია.")
        print("ᲢᲝᲙᲔᲜᲘ:", access_token)
    else:
        print("ᲢᲝᲙᲔᲜᲘ ᲕᲔᲠ ᲬᲐᲘᲙᲘᲗᲮᲐ ᲤᲐᲘᲚᲘᲓᲐᲜ.")
