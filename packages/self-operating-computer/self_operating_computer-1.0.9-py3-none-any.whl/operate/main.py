"""
Self-Operating Computer
"""
import argparse
from operate.utils.ansi_colors import ANSI_BRIGHT_MAGENTA
from operate.dialogs.dialog import main 

def main_entry():
    parser = argparse.ArgumentParser(
        description="Run the self-operating-computer with a specified model."
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Specify the model to use",
        required=False,
        default="gpt-4-vision-preview",
    )

    # Add a voice flag
    parser.add_argument(
        "--voice",
        help="Use voice input mode",
        action="store_true",
    )

    parser.add_argument(
        "-accurate",
        help="Activate Reflective Mouse Click Mode",
        action="store_true",
        required=False,
    )

    # Allow for direct input of prompt
    parser.add_argument(
        "--prompt",
        help="Directly input the objective prompt",
        type=str,
        required=False,
    )

    try:
        args = parser.parse_args()
        main(
            args.model,
            accurate_mode=args.accurate,
            terminal_prompt=args.prompt,
            voice_mode=args.voice,
        )
    except KeyboardInterrupt:
        print(f"\n{ANSI_BRIGHT_MAGENTA}Exiting...")


if __name__ == "__main__":
    main_entry()
