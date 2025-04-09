# Label to ID Extension for Inkscape

This extension allows you to automatically set the ID attribute of SVG elements to match their Inkscape labels, making your SVG more consistent and easier to work with in code.

## Features

-   Converts Inkscape labels to valid SVG IDs
-   Normalizes accented characters
-   Converts to lowercase for consistency
-   Replaces invalid characters with underscores
-   Prevents ID collisions
-   Provides detailed feedback on processed elements

## Installation

1. Download the file (`label_to_id.zip`) from the [Releases tab](https://github.com/davej/inkscape-label-to-id/releases)
2. Place it in your Inkscape extensions folder:
    - Windows: `%APPDATA%\Inkscape\extensions\`
    - Linux: `~/.config/inkscape/extensions/`
    - Mac OS: `~/Library/Application Support/Inkscape/extensions/`
3. Extract the zip file
4. Restart Inkscape

## Usage

1. Select one or more elements in your drawing
2. Go to Extensions → .Custom → Label to ID
3. Click Apply

The extension will process your selected elements and display a summary of the changes made.
