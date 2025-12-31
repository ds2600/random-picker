import secrets
import hashlib
import os
import time
import utils2
import random
import sys

parser = utils2.get_argument_parser()
parser.add_argument("--list", action="store_true", help="Just randomize the list of items")
parser.add_argument("--animate", action="store_true", help="Display spinning animation")
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
    logger.info("Entropy sources: Unix Epoch time, Process ID, 64 byte random string from OS cryptographic entropy sources.")
    entropy_sources = (
        str(time.time_ns()) +
        str(os.getpid()) +
        str(os.urandom(64))
    )
    logger.info("Running SHA512 on entropy string")
    seed = int(hashlib.sha512(entropy_sources.encode()).hexdigest(), 16)
    logger.debug(f"Seed: {seed}")
    return seed

def animate_selection(items, final_choice):
    print("\nSpinning...\n")
    spin_cycles = 30
    delay = 0.05

    for i in range(spin_cycles):
        pick = random.choice(items)
        sys.stdout.write(f"\r{pick}  ")
        sys.stdout.flush()
        time.sleep(delay)
        delay += 0.02

    sys.stdout.write(f"\rSelected: {final_choice}    \n")
    sys.stdout.flush()

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
            if args.animate:
                animate_selection(items, selected_item)
            else:
                print(f"Selected: {selected_item}")

def main():
    logger.info("Starting...")
    items = get_list()
    pick_random_item(items)

if __name__ == "__main__":
    main()

