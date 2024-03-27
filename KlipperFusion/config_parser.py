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

import os
from configuration_section import ConfigurationSection
from gcode_macro import GCodeMacro
import glob


class ConfigParser:
    """Parses configuration files for a custom configuration setup.

    This parser supports reading from multiple files, handling include directives,
    parsing sections, and processing gcode macros. It is designed to be flexible and
    extendable for different configuration formats."""

    def __init__(self, base_path=''):
        """
        Initializes the parser with an optional base directory path.
        """

        self.current_element = None
        self.sections = {}
        self.current_section = None
        self.base_path = os.path.abspath(base_path)
        self.preceding_comments = []
        self.in_gcode_block = False
        self.gcode_block_lines = []
        self.gcode_block_name = ''  # Initialize gcode_block_name here

    def parse_file(self, filepath, parent_dir=''):
        """
        Parses a single file or multiple files (using glob patterns) for configuration data.
        """

        try:
            if not os.path.isabs(filepath):
                filepath = os.path.join(parent_dir or self.base_path, filepath)
            normalized_path = os.path.normpath(filepath)

            if '*' in normalized_path:
                for matching_file in glob.glob(normalized_path):
                    self.parse_file(matching_file, os.path.dirname(matching_file))
            elif os.path.exists(normalized_path):
                with open(normalized_path, 'r') as file:
                    for line in file:
                        self.parse_line(line, normalized_path, os.path.dirname(normalized_path))
            else:
                print(f"Warning: File {normalized_path} not found.")
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
        except IOError as e:
            print(f"I/O error: {e}")
        except Exception as e:
            print(f"Unexpected error while reading file {filepath}: {e}")

    def parse_line(self, line, filename, current_dir):
        """
        Processes each line of the configuration file.
        """

        try:
            trimmed_line = line.strip()
            command_part, *comment_part = trimmed_line.split('#', 1)
            trimmed_command = command_part.strip()
            inline_comment = comment_part[0].strip() if comment_part else ''

            if self.in_gcode_block:
                # Check if the current line indicates the end or continuation of a gcode block
                if self.is_new_block_or_section_start(trimmed_command):
                    # Finalize current gcode block if starting a new block or section
                    self.finalize_gcode_block()
                    self.in_gcode_block = False

            # Handling gcode block start or continuation
            if self.is_gcode_block_start(trimmed_command):
                self.start_new_gcode_block(trimmed_command)
            elif trimmed_line.startswith('['):
                if self.in_gcode_block:
                    # Finalize the gcode block if we're starting a new section
                    self.finalize_gcode_block()
                self.handle_section_or_include(trimmed_command, current_dir, filename)
            elif self.in_gcode_block:
                # Continue accumulating lines within a gcode block
                self.gcode_block_lines.append(line)
            elif ':' in command_part:
                self.handle_key_value_pair(trimmed_command, filename, inline_comment)
            else:
                if comment_part:
                    self.preceding_comments.append(comment_part[0].strip())
        except ValueError as e:
            print(f"Value error encountered in file {filename}, line '{line}': {e}")
        except Exception as e:
            print(f"Unexpected error while processing line in file {filename}: {e}")

    def handle_section_or_include(self, command, current_dir, filename):
        """
        Handles the beginning of a new section or an include directive.

        This method determines whether the parsed command indicates the start of a new section
        or an include directive. It then delegates to the appropriate handler function.
        """

        # Adjusted method to correctly pass and handle 'filename' and 'current_dir'
        if command.startswith('[include '):
            self.handle_include_directive(command, current_dir)
        else:
            self.handle_section_start(command, filename)
        self.preceding_comments = []

    def handle_include_directive(self, command, current_dir):
        """
        Processes include directives found within configuration files.

        When an include directive is encountered, this method parses the specified file
        as part of the current configuration, allowing for modular configuration setups.
        """

        full_include_path = ''
        try:
            # Extract the filename from the include directive
            include_filename = command.split('include ')[1].strip().strip('[]')

            # Combine the current directory with the include filename
            full_include_path = os.path.join(current_dir, include_filename)

            # Parse the included file. The parent directory of the included file
            # is passed as the second argument to correctly handle nested includes
            # relative to the current included file's location.
            self.parse_file(full_include_path, current_dir)
        except FileNotFoundError:
            print(f"Error: The file specified in the include directive ({full_include_path}) does not exist.")
        except RecursionError:
            print(f"Recursive include detected in file {command}.")
        except Exception as e:
            print(f"Error processing include directive in file {command}: {e}")

    def handle_section_start(self, trimmed_command, filename):
        """
        Initiates a new section within the configuration.

        This method is called when the parser identifies the start of a new section, based on
        the command syntax. It prepares the parser to handle the entries within this new section.
        """
        
        if self.in_gcode_block:
            self.finalize_gcode_block()
        section_name = trimmed_command.strip('[]')
        self.start_new_section(section_name, filename)

    def is_new_block_or_section_start(self, command):
        # Returns True if the command signifies the start of a new block or section, which can be used
        # to determine if the current gcode block should be finalized.
        return command.startswith('[') or self.is_gcode_block_start(command)

    @staticmethod
    def is_gcode_block_start(command):
        """
        Determines if a command marks the beginning of a gcode block.
        """
        
        return command.endswith(':') and not any(command.startswith(x) for x in ['[include ', '[gcode_macro '])

    def start_new_gcode_block(self, command):
        """
        Begins processing a new gcode block.
        """
        
        self.in_gcode_block = True
        self.gcode_block_name = command.rstrip(':').strip()
        self.gcode_block_lines = []

    def handle_gcode_block_start(self):
        """
        Marks the beginning of a gcode block parsing process.

        This is used to initiate the collection of gcode lines into a block, preparing
        for their subsequent processing and inclusion in the final configuration.
        """
        
        self.in_gcode_block = True
        self.gcode_block_lines = []
        self.gcode_block_name = 'default_gcode_block'  # Set a default or specific name as needed

    def handle_gcode_line(self, trimmed_command):
        """
        Appends gcode line to the end of current gcode block.
        """

        self.gcode_block_lines.append(trimmed_command)

    def finalize_gcode_block(self):
        """
        Finalizes the parsing of a gcode block.

        Once the end of a gcode block is identified, this method is called to process
        and store the collected gcode lines, associating them with the current section.
        """
        try:
            if self.current_section and self.in_gcode_block:
                self.current_section.add_gcode_block(self.gcode_block_name, self.gcode_block_lines)
            self.in_gcode_block = False
            self.gcode_block_lines = []
            self.gcode_block_name = ''  # Reset gcode_block_name after finalizing the block
        except Exception as e:
            print(f"Error finalizing G-code block: {e}")

    def handle_key_value_pair(self, command_part, filename, inline_comment):
        """
        Processes key-value pairs within the configuration.

        Key-value pairs are fundamental elements of the configuration, representing settings
        or parameters. This method extracts these pairs and assigns them to the current section.
        """
        
        key, value = command_part.split(':', 1)
        if self.current_section:
            self.current_section.add_key_value_pair(key.strip(), filename, value.strip(), inline_comment,
                                                    self.preceding_comments)
        self.preceding_comments = []

    def add_macro_key_value(self, line):
        """
        Processes key-value pairs within the configuration.

        Key-value pairs are fundamental elements of the configuration, representing settings
        or parameters. This method extracts these pairs and assigns them to the current section.
        """
        
        key, value = line.split(':', 1)
        if self.current_section and isinstance(self.current_section, GCodeMacro):
            self.current_section.add_parameter(key.strip(), value.strip())

    def start_new_section(self, name, filename):
        """
        Begins a new section within the configuration parsing process.

        This method is invoked when a new section is identified, setting up a new context
        for the subsequent lines to be processed as part of this section.
        """
        try:
            if name in self.sections:
                self.current_section = self.sections[name]
                self.current_section.add_file(filename)
            else:
                self.current_section = ConfigurationSection(name, filename)
                self.sections[name] = self.current_section
        except Exception as e:
            print(f"Error starting new section '{name}' in file {filename}: {e}")

    def write_output(self, output_filepath, hide_unmodified=True):
        """
        Writes the parsed configuration to a file.

        After parsing is complete, this method generates the final output, writing the processed
        configuration data to the specified file, optionally filtering out unmodified sections.
        """
        
        with open(output_filepath, 'w') as file:
            for section_name, section in self.sections.items():
                file.write(section.write_output(self.base_path, hide_unmodified))
