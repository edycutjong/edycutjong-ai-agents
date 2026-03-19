import sys

def should_block_pr(is_breaking: bool, force_block: bool = False) -> bool:
    """
    Determines if the PR should be blocked.
    """
    if force_block:  # pragma: no cover
        return True  # pragma: no cover
    if is_breaking:  # pragma: no cover
        return True  # pragma: no cover
    return False  # pragma: no cover

def fail_build(reason: str):
    """
    Exits the process with a failure code to signal CI/CD to block the merge.
    """
    print(f"\n[PR Blocker] FAILURE: {reason}")
    sys.exit(1)
