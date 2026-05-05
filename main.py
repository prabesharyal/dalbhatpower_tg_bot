"""DalBhatPower bot entry point."""
import dotenv

dotenv.load_dotenv()

from bot.app import run


def main() -> None:
    print("Starting bot...")
    run()


if __name__ == "__main__":
    main()
