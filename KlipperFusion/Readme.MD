# KlipperFusion: Configuration Insight Tool for Klipper

## Overview

KlipperFusion is a specialized tool designed to parse and analyze Klipper configuration files, particularly for complex setups that utilize multiple include files. Its primary purpose is to provide clarity on how configurations evolve - tracking changes, identifying where values are overridden, and pinpointing the final settings applied to the 3D printer's firmware. This tool is invaluable for users and developers who need to navigate and understand the intricacies of their Klipper configurations.

## Key Features

- **Deep Parsing**: Analyzes Klipper configuration files, delving into include files to construct a comprehensive overview of the printer's settings.
- **Change Tracking**: Identifies and tracks changes across multiple configuration files, highlighting how and where specific settings are overridden.
- **Configuration Insights**: Offers insights into the final applied settings, making it easier to understand complex configurations and the impact of included files.
- **Simplified Troubleshooting**: Aids in troubleshooting configuration issues by providing a clear lineage of setting adjustments.

## How It Works

KlipperFusion scans the specified Klipper configuration file, traversing through any included files to gather a detailed account of all settings. It then produces an output file that documents the source and evolution of each setting, including G-codes and key values. This output is crucial for unraveling the final configuration applied to the printer, especially in setups where settings are layered across multiple files.

## Usage

To use KlipperFusion, simply invoke it from the command line with the path to your main Klipper configuration file. The tool offers options to tailor the output to your needs.

### Command Syntax

```bash
python klipper_fusion.py [OPTIONS] FILENAME
```

- `FILENAME`: The path to the Klipper configuration file to analyze.

Options:

- `--overwrite`: If specified, the tool will overwrite the output file if it already exists.
- `--output`: Designates a custom path and name for the output file. Defaults to `output.cfg` in the same directory as the input file.
- `--hide-unmodified`: When set, the output will only include gcode macros that have been modified or overridden, streamlining the output for easier analysis.

### Example Command

Analyze `printer.cfg` and save the detailed report to `config_analysis.cfg`:

```bash
python klipper_fusion.py --overwrite --output config_analysis.cfg printer.cfg
```

This command parses `printer.cfg`, follows any include directives within, and produces a report in `config_analysis.cfg` that details the evolution of settings across the configuration files.

## Getting Started

No special setup is required beyond having Python installed. Download the KlipperFusion script, and run it from your terminal or command line interface.

## Contributing

Feedback, bug reports, and contributions to KlipperFusion are always welcome. If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request on GitHub.

## License

KlipperFusion is released under the MIT License. For more details, see the LICENSE file included with the tool.
