import sys

def main():
    if len(sys.argv) != 4:
        print("Webhook patcher v1 (beta)")
        print("Replaces your desired placeholder keyword with webhook")
        print("Usage: webhook_patcher.py <filename> <keyword> <webhook>")
        return

    filename = sys.argv[1]
    keyword = sys.argv[2]
    webhook = sys.argv[3]

    try:
        with open(filename, 'r') as file:
            content = file.read()

        content = content.replace(keyword, webhook)

        with open(filename, 'w') as file:
            file.write(content)

        print("Success")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

if __name__ == "__main__":
    main()
