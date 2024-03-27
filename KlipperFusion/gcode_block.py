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

class GCodeBlock:
    def __init__(self, name, filename=''):
        """
        Initializes a new GCodeBlock with a name and optionally a filename where the block is defined.
        """

        self.name = name
        self.filename = filename  # Track the filename where the block is defined
        self.lines = []
        self.preceding_comments = []
        self.older_versions = []

    def add_line(self, line):
        """
        Appends a new line of G-code to the current block.
        """

        self.lines.append(line)

    def set_preceding_comments(self, comments):
        """
        Sets the preceding comments for the G-code block. These comments appear in the output before the block itself.
        """

        self.preceding_comments = comments

    def finalize(self):
        """
        Finalizes the G-code block for output. This creates a snapshot of the block as an older version if it contains
        any lines or comments.
        """

        try:
            if self.lines or self.preceding_comments:
                old_version = GCodeBlock(self.name, self.filename)
                old_version.lines = self.lines.copy()
                old_version.preceding_comments = self.preceding_comments.copy()
                self.older_versions.append(old_version)
        except Exception as e:
            print(f"Error finalizing GCodeBlock '{self.name}': {e}")

    def has_modifications(self):
        """
        Determines whether the G-code block has been modified by checking if there are any older versions.
        """

        return len(self.older_versions) > 0

    def write_block(self, hide_unmodified=True):
        """
        Generates and returns the textual representation of the G-code block. If `hide_unmodified` is True, unmodified
        blocks are marked accordingly.
        """

        try:
            if hide_unmodified and not self.has_modifications():
                return f"{self.name}: # UNMODIFIED\n\n"

            output = ""
            if self.older_versions:
                output += "\n"  # Ensure there's a starting newline for separation
                for version in self.older_versions:
                    output += "# Previous version defined in {}\n".format(version.filename)
                    for comment in version.preceding_comments:
                        output += "# {}\n".format(comment.rstrip('\n'))
                    for line in version.lines:
                        output += "# {}\n".format(line.rstrip('\n'))
            if output:
                output += "\n"
            output += "{}:\n".format(self.name)
            for line in self.lines:
                output += "{}\n".format(line.rstrip('\n'))
            return output

        except Exception as e:
            print(f"Error writing GCodeBlock '{self.name}': {e}")
            return ""
