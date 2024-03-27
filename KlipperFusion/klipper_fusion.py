# MIT License
#
# Copyright (c) 2024 Kamil Ercan Turkarslan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
import os
import sys
from config_parser import ConfigParser


# This script serves as the main entry point for KlipperFusion, a tool designed to merge, track, and update Klipper
# configuration files.

@click.command()
@click.argument('filename')
@click.option('--overwrite', is_flag=True, help='Overwrite the output file if it exists without prompting.')
@click.option('--output', default=None, help='Optional custom output file path and name.')
@click.option('--hide-unmodified', is_flag=True,
              help='Show detailed modifications for each section. If not set, unmodified sections are simply marked '
                   'as UNMODIFIED.')
def main(filename, overwrite, output, hide_unmodified):
    """
    The main function that processes the command-line arguments and options.

    Args:
        filename: The path to the input configuration file to be processed.
        overwrite: A boolean flag to indicate whether the output file should be overwritten without prompting if it
            already exists.
        output: An optional custom path and name for the output file. If not specified, defaults to 'output.cfg' in
            the same directory as the input file.
        hide_unmodified: A boolean flag to control whether unmodified sections are simply marked as 'UNMODIFIED' or
            if their details are fully shown in the output.

    This function initializes the configuration parser, processes the input file, and writes the combined and updated
    configuration to the output file. Error handling is included to manage issues such as file not found or other
    exceptions.
    """

    # Ensure the filename is not null or empty
    if not filename:
        sys.exit("Please provide a valid filename.")

    try:
        # Retrieve the base path and input file
        base_path, input_file = os.path.split(os.path.abspath(filename))
    except FileNotFoundError:
        # If the file is not found, exit the script
        sys.exit("The specified file was not found. Please check the path and try again.")
    except Exception as e:
        # If any other exception is encountered, exit the script with the error message
        sys.exit(f"An unexpected error occurred: {str(e)}")

    # Use the specified output file and path if provided, otherwise default to output.cfg in the input file's directory
    output_file = output if output else os.path.join(base_path, "output.cfg")

    # Check if the output file exists
    if os.path.exists(output_file) and not overwrite:
        # Prompt the user for overwrite permission if not specified by the command line option
        click.confirm(f"{output_file} exists. Overwrite?", abort=True)

    # Initialize ConfigParser with error handling
    try:
        parser = ConfigParser(base_path)
    except Exception as e:
        sys.exit(f"An error occurred while creating the parser: {str(e)}")

    # Try to parse the file using the parser object with error handling
    try:
        parser.parse_file(filename)
    except Exception as e:
        sys.exit(f"Could not parse the file: {str(e)}")

    # Finally, try to write the parsed content to the output file with error handling
    try:
        parser.write_output(output_file, hide_unmodified)  # Write the parsed content to the output file
    except Exception as e:
        sys.exit(f"An error occurred when writing the output: {str(e)}")

    # If no exceptions were encountered, print a success message
    print("File written successfully.")


if __name__ == '__main__':
    main()
