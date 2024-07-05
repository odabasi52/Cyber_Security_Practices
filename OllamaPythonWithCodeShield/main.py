import ollama
from colorama import Fore, init
from codeshield.cs import CodeShield
import asyncio

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""
    {Fore.YELLOW}*******************************************************
    *                                                     *
    *          {Fore.CYAN}WELCOME TO OLLAMA PYTHON INTERFACE{Fore.YELLOW}         *
    *                                                     *
    *******************************************************
    {Fore.GREEN}Please start the Ollama service locally with command {Fore.CYAN}ollama serve
    {Fore.GREEN}and pull necessary models.
    """
    print(banner)

def list_models():
    models = ollama.list()["models"]
    for idx, model in enumerate(models, start=1):
        print(f"{Fore.BLUE}[{idx}] {model['name']}")
    print(f"{Fore.BLUE}[99] Exit")

def is_model_available(model_name):
    models = ollama.list()["models"]
    return any(model["name"] == model_name for model in models)

def chat_with_ollama(model_name, user_promt):
    prompt = """
        You are a coding assistant. Only respond with a code snippet. According to user input about Programming and Code write necessary Code Snippet in TXT format. Do not write anything else, just write the code snippet.
        Do not write name of given programming language, just write the code snippet.
        For example: if you write python function call it after function is implemented. Code should work if it is directly copied and pasted into a code editor.
        import hashlib   
        def get_md5_hash(input_string):
            return hashlib.md5(input_string.encode()).hexdigest()
        get_md5_hash("your_string_here")
        
        USER INPUT:
    """
    prompt += user_promt
    response = ollama.chat(model=model_name, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    return (response['message']['content'])


def main():
    print(f"{Fore.GREEN}Available models:")
    list_models()

    try:
        choice = int(input(f"{Fore.CYAN}Enter the number of the model you want to use or exit with 99: "))
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.")
        return

    if choice == 99:
        exit(0)
    else:
        available_models = ollama.list()["models"]
        if 1 <= choice <= len(available_models):
            model = available_models[choice - 1]["name"]
            print(f"{Fore.GREEN}You selected {model}")
            user_input = input("Enter your question about coding: ")
            llm_output_code = chat_with_ollama(model, user_input)
            llm_output_code = f'{Fore.CYAN}{llm_output_code.replace("```", "")}'
            print("\nLLM OUTPUT CODE: " + llm_output_code)
            print("\nScanning the code for security issues...\n")
            asyncio.run(scan_llm_output(llm_output_code))
        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid model number.")


async def scan_llm_output(llm_output_code):
    result = await CodeShield.scan_code(llm_output_code)
    if result.is_insecure:
        print(
            "Security issues found in code. Action needed to block or warn about insecure code."
        )
    else:
        print("No issues found while scanning for code security. No action needed")
        
if __name__ == "__main__":
    print_banner()
    main()