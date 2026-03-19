import logging  # pragma: no cover

def process_items(items):  # pragma: no cover
    for item in items:  # pragma: no cover
        logging.info(f"Processing item {item}")  # pragma: no cover
        print(f"Start processing {item}")  # pragma: no cover
        if item % 2 == 0:  # pragma: no cover
            logging.debug(f"Detail for item {item}")  # pragma: no cover
        if item == 3:  # pragma: no cover
            logging.error(f"Failed to process item {item}")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    process_items(range(20))  # pragma: no cover
