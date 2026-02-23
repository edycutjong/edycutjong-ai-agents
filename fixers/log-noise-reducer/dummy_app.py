import logging

def process_items(items):
    for item in items:
        logging.info(f"Processing item {item}")
        print(f"Start processing {item}")
        if item % 2 == 0:
            logging.debug(f"Detail for item {item}")
        if item == 3:
            logging.error(f"Failed to process item {item}")

if __name__ == "__main__":
    process_items(range(20))
