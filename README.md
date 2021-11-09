Sublime CMake Format
============

[![Build Status](https://travis-ci.com/jasjuang/sublime_cmake_format.svg?branch=master)](https://travis-ci.com/jasjuang/sublime_cmake_format)
[![Package Control](https://packagecontrol.herokuapp.com/downloads/CMakeFormat.svg?style=flat-square)](https://packagecontrol.io/packages/CMakeFormat)

What it does
------------
CMake-format is a tool for formatting CMake files. This is a
package that allows you to run it easily from within Sublime Text.

Installing
----------

- This plugin is dependent on [cmake_format](https://github.com/cheshirekow/cmake_format)
  and [Sublime CMake](https://packagecontrol.io/packages/CMake) plugin.

To install `cmake_format`, do the following:

1. Install [Python](http://python.org/download/) and [pip](http://www.pip-installer.org/en/latest/installing.html).

2. Install `cmake_format` by typing the following in a terminal:
   ```
   [sudo] pip install cmake_format
   ```

- Please install Sublime CMake and this package through Package Control in the 
  usual way.

- Set the path to the cmake-format binaries. You can do this from within Sublime
  Text by choosing `CMake Format - Set Path` from the command palette.  Hint:
  the path should look something like this `/usr/local/bin/cmake-format`.
  If cmake-format is in your system path, you shouldn't need to do anything.

Use
---
- Default shortcut is `ctrl+shift+c`.
  This will apply cmake-format to the selection.
- It is possible to run the formatter on every save to a file, change settings
  to `"format_on_save": true`.
- To change settings on a per-package basis, add them under `CMakeFormat` key,
  example project.sublime-settings:
- To use style from a file (for example `.cmake-format`), change settings to `"style": "file"`. Otherwise `custom` style is used.

```json
{
  "folders": [],
  "settings": {
    "CMakeFormat": {
      "style": "file",
      "format_on_save": true
    }
  }
}
```


If You Liked This
-----------------
- ... And want to contribute, PR's gladly accepted!

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Credits
-------
Thanks to [cheshirekow](https://github.com/cheshirekow/) for writing
 cmake format!
