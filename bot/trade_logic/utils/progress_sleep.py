
import logging,tqdm,time
def progress_sleep(seconds):
    """
    Displays a single progress bar for the specified time duration.
    :param seconds: Total time to wait, in seconds.
    """
    with tqdm.tqdm(total=seconds, desc="Waiting for next order", unit="s", leave=True) as pbar:
        for _ in range(seconds):
            time.sleep(1)
            pbar.update(1)