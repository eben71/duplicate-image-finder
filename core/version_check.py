import subprocess
import logging
from importlib.metadata import version, PackageNotFoundError

logger = logging.getLogger(__name__)


def check_playwright_version():
    try:
        pip_version = version("playwright")
    except PackageNotFoundError:
        logger.warning(
            "Playwright (Python package) not installed – skipping version check"
        )
        return

    try:
        cli_output = subprocess.getoutput("playwright --version")
        cli_version = (
            cli_output.strip().split()[-1] if "Version" in cli_output else "unknown"
        )
    except Exception as ex:
        logger.warning(f"Failed to run playwright CLI: {ex}")
        cli_version = "unknown"

    if pip_version != cli_version:
        raise RuntimeError(
            f"[Playwright Version Mismatch] pip: {pip_version}, CLI: {cli_version}"
        )

    logger.info(f"✅ Playwright version verified: {pip_version}")
