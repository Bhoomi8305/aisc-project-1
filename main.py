from toolformer import Toolformer

def main():
    toolformer = Toolformer()

    print("Welcome to Toolformer!")
    while True:
        user_input = input("Enter a query (type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        response = toolformer.process_input(user_input)
        print(response)

if __name__ == "__main__":
    main()
