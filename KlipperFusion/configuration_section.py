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

from gcode_block import GCodeBlock
from key_value_pair import KeyValuePair


class ConfigurationSection:
    def __init__(self, name, filename):
        """
        Initializes a new ConfigurationSection with the given name and filename.
        """

        self.name = name
        self.filename = filename
        self.filenames = {filename}
        self.key_value_pairs = {}
        self.gcode_blocks = {}

    def add_file(self, filename):
        """
        Adds a filename to the set of filenames associated with this configuration section.
        """

        self.filenames.add(filename)

    def add_gcode_block(self, block_name, gcode_lines, preceding_comments=None):
        """
        Adds a new GCodeBlock to this section. If a block with the same name exists,
        appends the new lines to it. Optionally includes preceding comments.
        """

        try:
            # Check if a GCodeBlock with the same name already exists
            if preceding_comments is None:
                preceding_comments = []
            if block_name not in self.gcode_blocks:
                self.gcode_blocks[block_name] = []

            # Create a new GCodeBlock instance for the new lines
            new_block = GCodeBlock(block_name)
            for line in gcode_lines:
                new_block.add_line(line)
            new_block.set_preceding_comments(preceding_comments)

            # Append the new GCodeBlock instance to the list associated with block_name
            self.gcode_blocks[block_name].append(new_block)
        except Exception as e:
            print(f"Error adding GCodeBlock '{block_name}': {e}")

    def add_key_value_pair(self, key, filename, value, inline_comment, preceding_comments):
        """
        Adds a key-value pair to this section. If the key already exists, updates its
        value and associates the new filename, inline comment, and preceding comments.
        """
        try:
            self.add_file(filename)
            if key in self.key_value_pairs:
                self.key_value_pairs[key].add_occurrence(filename, value, inline_comment, preceding_comments)
            else:
                self.key_value_pairs[key] = KeyValuePair(key, filename, value, inline_comment, preceding_comments)
        except Exception as e:
            print(f"Error adding or updating KeyValuePair '{key}': {e}")

    def get_filenames(self):
        """
        Returns a list of all filenames associated with this configuration section.
        """

        return list(self.filenames)

    def get_latest_filename(self):
        """
        Returns the most recent filename added to this configuration section.
        """

        return self.filename

    def get_key_value_pairs(self):
        """
        Returns a dictionary of all key-value pairs associated with this configuration section.
        """

        return self.key_value_pairs

    def write_output(self, base_path, hide_unmodified=True):
        """
        Generates and returns the textual representation of this configuration section,
        optionally hiding unmodified sections.
        """

        try:
            output = "\n"
            relative_filenames = [os.path.relpath(filename, base_path) for filename in self.filenames]
            for filename in relative_filenames:
                output += f"# {filename}\n"
            output += f"[{self.name}]\n"
            for key, kvp in self.key_value_pairs.items():
                output += kvp.format_for_output(base_path) + "\n"
            # Handle gcode blocks output
            for block_name, blocks in self.gcode_blocks.items():
                for block in blocks:
                    output += block.write_block(hide_unmodified)

            return output
        except Exception as e:
            print(f"Error generating output for ConfigurationSection '{self.name}': {e}")
            return ""
