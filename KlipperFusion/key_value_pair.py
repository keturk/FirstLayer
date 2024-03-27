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


class KeyValuePair:
    def __init__(self, key, filename, value, inline_comment, preceding_comments):
        """
        Initializes a new KeyValuePair with a key, filename, value, and optional comments.
        """

        self.key = key
        self.filename = filename
        self.value = value
        self.inline_comment = inline_comment
        self.preceding_comments = preceding_comments
        self.occurrences = []

    def add_occurrence(self, filename, value, inline_comment, preceding_comments):
        """
        Records a new occurrence of the key-value pair, updating its value and associated comments,
        while preserving the history of previous values and their metadata.
        """

        try:
            self.occurrences.append({
                'filename': self.filename,
                'value': self.value,
                'inline_comment': self.inline_comment,
                'preceding_comments': self.preceding_comments
            })
            self.filename = filename
            self.value = value
            self.inline_comment = inline_comment
            self.preceding_comments = preceding_comments
        except Exception as e:
            print(f"Error adding occurrence to KeyValuePair '{self.key}': {e}")

    def get_latest_value(self):
        """
        Returns the most recent value associated with this key-value pair.
        """

        return self.value

    def get_all_values(self):
        """
        Returns a list of all values (including the current and all previous values) associated with this key.
        """

        return [occurrence['value'] for occurrence in self.occurrences] + [self.value]

    def get_occurrence_details(self):
        """
        Provides detailed information about all occurrences of this key-value pair, including the filenames
        where they were defined, their values, inline comments, and any preceding comments.
        """

        # Include all occurrences plus the current state as part of the details
        return self.occurrences + [{
            'filename': self.filename,
            'value': self.value,
            'inline_comment': self.inline_comment,
            'preceding_comments': self.preceding_comments,
            'duplicate_flag': False  # The latest occurrence is not considered a duplicate of itself
        }]

    def format_for_output(self, base_path):
        """
        Generates a formatted string representation of the key-value pair for output, including the history
        of values and comments, adjusted relative to a specified base path.
        """

        try:
            output = ""
            # Print preceding comments for the latest value
            for comment in self.preceding_comments:
                output += f"# {comment}\n"

            # Print previous values as comments with their source file and inline comments
            for occ in self.occurrences:
                relative_filename = os.path.relpath(occ['filename'], base_path)
                prev_val_line = f"# {self.key}: {occ['value']} <- {relative_filename}:"
                if occ['inline_comment']:
                    prev_val_line += f" # {occ['inline_comment']}"
                output += prev_val_line + "\n"

            # Print the current (latest) value with its inline comment
            current_val_line = f"{self.key}: {self.value}"
            if self.inline_comment:
                current_val_line += f" # {self.inline_comment}"
            output += current_val_line

            return output
        except Exception as e:
            print(f"Error generating output for KeyValuePair '{self.key}': {e}")
            return ""
