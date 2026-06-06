import logging

from src.agent import run_agent
from src.actions import execute_action


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print(f'* An agentic tool that lives in your terminal.')
    print(f'* Press /exit to quit')

    while True:
        try:
            user_input = input('\nYou: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nBye！')
            break

        if not user_input:
            continue

        if user_input.lower() in ('/exit', '/q', '/quit'):
            print('\nBye！')
            break

        ai_response = run_agent(user_input)

        result = execute_action(ai_response)

        print(f'Agent: {result}')
