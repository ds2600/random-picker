import secrets
import hashlib
import os
import time
import utils2
import random

parser = utils2.get_argument_parser()
parser.add_argument("--list", action="store_true", help="Just randomize the list of items")
args = parser.parse_args()
logger = utils2.setup_logging(debug=args.debug)


def get_list():
    logger.info("Getting items...")
    print("Enter your items one by one. Press Enter on an empty line to finish.")

    items = []

    while True:
        item = input("> ")
        if item.strip() == "":
            break
        items.append(item)
    logger.debug(f"Items:\n{items}")
    return items

def generate_seed():
    logger.info("Generating seed...")
    entropy_sources = (
        str(time.time_ns()) +
        str(os.getpid()) +
        str(os.urandom(64))
    )
    seed = int(hashlib.sha512(entropy_sources.encode()).hexdigest(), 16)
    logger.debug(f"Seed: {seed}")
    return seed

def pick_random_item(items):
    logger.info("Picking item...") 
    if not items:
        logger.warning("No items provided.")
        print("No items were provided.")
    else:
        seed = generate_seed()
        random.seed(seed)
        random.shuffle(items)
        if args.list:
            print(f"List:\n{items}")
        else:
            logger.debug(f"Seeded list:\n{items}")
            selected_item = secrets.choice(items)
            logger.info(f"Selected: {selected_item}")
            print(f"Selected: {selected_item}")

def main():
    logger.info("Starting...")
    items = get_list()
    pick_random_item(items)

if __name__ == "__main__":
    main()

