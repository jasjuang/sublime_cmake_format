CMake Format
============

What it does
------------
CMake-format is a tool for formatting CMake files. This is a
package that allows you to run it easily from within Sublime Text.

Installing
----------

- This plugin is dependent on the [cmake_format](https://github.com/cheshirekow/cmake_format)
  and the [Sublime CMake](https://packagecontrol.io/packages/CMake) plugin.

- Please install cmake_format by 

```
sudo pip install cmake_format
```

- Please install Sublime CMake and this package through Package Control in the 
  usual way.

- Set the path to the cmake-format binaries. You can do this from within Sublime
  Text by choosing `CMake Format - Set Path` from the command palette.  Hint:
  the path should look something like this `[path/to/cmake]/cmake/bin/cmake-format`.
  If cmake-format is in your system path, you shouldn't need to do anything.

Use
---
- Default shortcut is `ctrl+shift+c`.
  This will apply cmake-format to the selection.
- It is possible to run the formatter on every save to a file, change settings
  to `"format_on_save": true`.
- To change settings on a per-package basis, add them under `CMakeFormat` key,
  example project.sublime-settings:

```json
{
  "folders": [],
  "settings": {
    "CMakeFormat": {
      "format_on_save": true
    }
  }
}
```


If You Liked This
-----------------
- ... And want to contribute, PR's gladly accepted!

- Otherwise, why not pop on over and star this repo on GitHub?

Credits
-------
Thanks to [cheshirekow](https://github.com/cheshirekow/) for writing
 cmake format!