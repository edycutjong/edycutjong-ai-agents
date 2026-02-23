import sys

def should_block_pr(is_breaking: bool, force_block: bool = False) -> bool:
    """
    Determines if the PR should be blocked.
    """
    if force_block:
        return True
    if is_breaking:
        return True
    return False

def fail_build(reason: str):
    """
    Exits the process with a failure code to signal CI/CD to block the merge.
    """
    print(f"\n[PR Blocker] FAILURE: {reason}")
    sys.exit(1)
