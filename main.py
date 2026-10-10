import os, argparse, json, sys
from dotenv import load_dotenv
from openai import OpenAI
from functions import get_files_info
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("No api key found")


client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

def main():

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]


    for _ in range(20):

        response = client.chat.completions.create(
                model = "openrouter/free",
                messages = messages,
                tools = available_functions
            )
        if not response.usage:
            raise RuntimeError("API request failed.")

       
        message = response.choices[0].message
        messages.append(message)

        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        user_prompt = response.choices[0].message.content

        if args.verbose:
            print(f"User prompt: {user_prompt}/n /n{prompt_tokens} /n{completion_tokens}")
        else:
            print(user_prompt)


        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose = args.verbose)
                if not result_message.get("content"):
                    raise RuntimeError(
                            f"Tool message content is empty for {tool_call.function.name}"
                    )
                if args.verbose:
                    print(f"->{result_message["content"]}")
                messages.append(result_message)
        else:
            print(f"Final response:\n{message.content}")
            return

    print("error: Reached maximum iterations without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
