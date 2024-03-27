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

class GCodeMacro:
    def __init__(self, name, filename):
        """
        Initializes a new GCodeMacro with a name and filename.
        """

        self.name = name
        self.filename = filename
        self.definitions = []
        self.current_gcode_lines = []  # Temporary storage for accumulating gcode lines
        self.parameters = {}  # Initialize parameters dictionary here

    def add_parameter(self, key, value):
        """
        Adds or updates a parameter for the G-code macro with the specified key and value.
        """

        self.parameters[key] = value

    def add_gcode_line(self, line):
        """
        Appends a line of G-code to the current macro definition.
        """

        self.current_gcode_lines.append(line)

    def finalize_definition(self, preceding_comments=None):
        """
        Finalizes the current G-code macro definition, optionally including preceding comments, and prepares for a new
        definition if any.
        """

        try:
            if preceding_comments is None:
                preceding_comments = []
            if self.current_gcode_lines:
                self.definitions.append({
                    'filename': self.filename,
                    'gcode_lines': self.current_gcode_lines,
                    'preceding_comments': preceding_comments
                })
                # Reset for the next definition
                self.current_gcode_lines = []
        except Exception as e:
            print(f"Error finalizing definition for GCodeMacro '{self.name}': {e}")

    def get_latest_definition(self):
        """
        Returns the most recent definition of the G-code macro, if available.
        """

        return self.definitions[-1] if self.definitions else None

    def is_modified(self):
        """
        Determines whether the macro has been modified, indicated by having more than one definition.
        """

        return len(self.definitions) > 1

    def write_output(self, hide_unmodified=True):
        """
        Generates and returns the textual representation of the G-code macro. Unmodified macros can be marked as such
        based on the hide_unmodified flag.
        """

        try:
            if hide_unmodified and not self.is_modified():
                return f"UNMODIFIED [gcode_macro {self.name}]\n"

            output = f"[gcode_macro {self.name}]\n"
            for param, value in self.parameters.items():
                output += f"{param}: {value}\n"
            for definition in self.definitions:
                output += "\n".join(definition['gcode_lines']) + "\n"
            output += "\n"
            return output
        except Exception as e:
            print(f"Error generating output for GCodeMacro '{self.name}': {e}")
            return ""

    def print_all_definitions(self):
        """
        Prints all definitions of the macro, including preceding comments and G-code lines, starting with the oldest.
        """

        try:
            for definition in self.definitions:
                print(f"Defined in {definition['filename']}:")
                for comment in definition['preceding_comments']:
                    print(comment)
                for line in definition['gcode_lines']:
                    print(line)
                print()  # Add a blank line between definitions
        except Exception as e:
            print(f"Error printing definitions for GCodeMacro '{self.name}': {e}")
