#!/usr/bin/env python3

import sys
from database_cli import DatabaseCLI


if __name__ == "__main__":
    cli = DatabaseCLI()
    EXIT_CODE = cli.run()
    sys.exit(EXIT_CODE)
