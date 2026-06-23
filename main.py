from src import utils


def main():
    print(utils.clamp(15, 0, 10))
    print(utils.word_count("hello hello world"))

    print("Hello from my-project!")


if __name__ == "__main__":
    main()
