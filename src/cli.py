#!/usr/bin/env python3

import sys
from database_cli import DatabaseCLI


if __name__ == "__main__":
    cli = DatabaseCLI()
    exit_code = cli.run()
    sys.exit(exit_code)
