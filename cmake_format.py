#
# cmake_format.py
# Autoformatter for CMakefiles
#
# Written by Jason Juang,,,
# Copyright (c) 2018 Jason Juang,,,
#
# License: MIT
#

"""This module applies cmake_format in sublime."""

import sublime
import sublime_plugin
import subprocess
import os

# Settings file locations.
settings_file = 'cmake_format.sublime-settings'
custom_style_settings = 'cmake_format_custom.sublime-settings'

st_encodings_trans = {
   "UTF-8": "utf-8",
   "UTF-8 with BOM": "utf-8-sig",
   "UTF-16 LE": "utf-16-le",
   "UTF-16 LE with BOM": "utf-16",
   "UTF-16 BE": "utf-16-be",
   "UTF-16 BE with BOM": "utf-16",
   "Western (Windows 1252)": "cp1252",
   "Western (ISO 8859-1)": "iso8859-1",
   "Western (ISO 8859-3)": "iso8859-3",
   "Western (ISO 8859-15)": "iso8859-15",
   "Western (Mac Roman)": "mac-roman",
   "DOS (CP 437)": "cp437",
   "Arabic (Windows 1256)": "cp1256",
   "Arabic (ISO 8859-6)": "iso8859-6",
   "Baltic (Windows 1257)": "cp1257",
   "Baltic (ISO 8859-4)": "iso8859-4",
   "Celtic (ISO 8859-14)": "iso8859-14",
   "Central European (Windows 1250)": "cp1250",
   "Central European (ISO 8859-2)": "iso8859-2",
   "Cyrillic (Windows 1251)": "cp1251",
   "Cyrillic (Windows 866)": "cp866",
   "Cyrillic (ISO 8859-5)": "iso8859-5",
   "Cyrillic (KOI8-R)": "koi8-r",
   "Cyrillic (KOI8-U)": "koi8-u",
   "Estonian (ISO 8859-13)": "iso8859-13",
   "Greek (Windows 1253)": "cp1253",
   "Greek (ISO 8859-7)": "iso8859-7",
   "Hebrew (Windows 1255)": "cp1255",
   "Hebrew (ISO 8859-8)": "iso8859-8",
   "Nordic (ISO 8859-10)": "iso8859-10",
   "Romanian (ISO 8859-16)": "iso8859-16",
   "Turkish (Windows 1254)": "cp1254",
   "Turkish (ISO 8859-9)": "iso8859-9",
   "Vietnamese (Windows 1258)":  "cp1258",
   "Hexadecimal": None,
   "Undefined": None
}


# Check if we are running on a Windows operating system
os_is_windows = os.name == 'nt'


# The default name of the cmake-format executable
default_binary = 'cmake-format.exe' if os_is_windows else 'cmake-format'


def which(program):
    """http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python."""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def set_path(path):
    """Set the path to the binary in the settings file."""

    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    sublime.save_settings(settings_file)
    # Make sure the globals are updated.
    load_settings()


def update_path():
    """Display input panel to update the path."""

    load_settings()
    w = sublime.active_window()
    w.show_input_panel("Path to cmake-format: ", binary, set_path, None, None)


def check_binary():
    """Check that the binary can be found and is executable."""

    # If we couldn't find the binary.
    if (which(binary) is None):
        # Try to guess the correct setting.
        if (which(default_binary) is not None):
            # Looks like cmake-format is in the path, remember that.
            set_path(default_binary)
            return True
        # We suggest setting a new path using an input panel.
        msg = "The cmake-format binary was not found. Set a new path?"
        if sublime.ok_cancel_dialog(msg):
            update_path()
            return True
        else:
            return False
    return True


def load_settings():
    """Load settings and put their values into global scope."""

    # We set these globals.
    global binary
    global format_on_save
    global style
    global config_file
    global line_width
    global tab_size
    global max_subgroups_hwrap
    global max_pargs_hwrap
    global separate_ctrl_name_with_space
    global separate_fn_name_with_space
    global dangle_parens
    global dangle_align
    global min_prefix_chars
    global max_prefix_chars
    global max_lines_hwrap
    global line_ending
    global command_case
    global keyword_case
    global always_wrap
    global enable_sort
    global autosort
    global hashruler_min_length
    global bullet_char
    global enum_char
    global enable_markup
    global first_comment_is_literal
    global literal_comment_pattern
    global fence_pattern
    global ruler_pattern
    global canonicalize_hashrulers
    global emit_byteorder_mark
    global input_encoding
    global output_encoding
    settings_global = sublime.load_settings(settings_file)
    settings_local = sublime.active_window().active_view().settings().get('CMakeFormat', {})

    def load(name, default): return settings_local.get(name, settings_global.get(name, default))
    # Load settings, with defaults.
    binary = load('binary', default_binary)
    format_on_save = load('format_on_save', False)
    style = load('style', 'default')
    config_file = load('config_file', '')
    line_width = load('line_width', 80)
    tab_size = load('tab_size', 2)
    max_subgroups_hwrap = load('max_subgroups_hwrap', 2)
    max_pargs_hwrap = load('max_pargs_hwrap', 6)
    separate_ctrl_name_with_space = load('separate_ctrl_name_with_space', False)
    separate_fn_name_with_space = load('separate_fn_name_with_space', False)
    dangle_parens = load('dangle_parens', False)
    dangle_align = load('dangle_align', 'prefix')
    min_prefix_chars = load('min_prefix_chars', 4)
    max_prefix_chars = load('max_prefix_chars', 10)
    max_lines_hwrap = load('max_lines_hwrap', 2)
    line_ending = load('line_ending', 'unix')
    command_case = load('command_case', 'canonical')
    keyword_case = load('keyword_case', 'unchanged')
    always_wrap = load('always_wrap', '[]')
    enable_sort = load('enable_sort', True)
    autosort = load('autosort', False)
    hashruler_min_length = load('hashruler_min_lengths', 10)
    bullet_char = load('bullet_char', '*')
    enum_char = load('enum_char', '.')
    enable_markup = load('enable_markup', True)
    first_comment_is_literal = load('first_comment_is_literal', False)
    literal_comment_pattern = load('literal_comment_pattern', 'None')
    fence_pattern = load('fence_pattern', '^\\s*([`~]{{3}}[`~]*)(.*)$')
    ruler_pattern = load('ruler_pattern', '^\\s*[^\\w\\s]{{3}}.*[^\\w\\s]{{3}}$')
    canonicalize_hashrulers = load('canonicalize_hashrulers', True)
    emit_byteorder_mark = load('emit_byteorder_mark', False)
    input_encoding = load('input_encoding', 'utf-8')
    output_encoding = load('output_encoding', 'utf-8')


def is_supported(lang):
    """Check whether the file is CMake related."""

    load_settings()
    return lang.endswith(('CMake' + '.tmLanguage', 'CMake' + '.sublime-syntax'))


class CmakeFormatCommand(sublime_plugin.TextCommand):
    """Triggered when the user runs cmake format."""

    def run(self, edit, whole_buffer=False):
        """Entry point for sublime to call this."""

        load_settings()

        if not check_binary():
            return

        # The below code has been taken and tweaked from llvm.
        encoding = st_encodings_trans[self.view.encoding()]
        if encoding is None:
            encoding = 'utf-8'

        if style == "default":
            command = [binary, str(self.view.file_name())]
        elif style == "file":
            if not config_file:
                command = [binary, str(self.view.file_name())]
            else:
                command = [binary, str(self.view.file_name()),
                           '-c', config_file]
        elif style == "custom":
            command = [binary, str(self.view.file_name()),
                       '--line-width', str(line_width),
                       '--tab-size', str(tab_size),
                       '--max-subgroups-hwrap', str(max_subgroups_hwrap),
                       '--max-pargs-hwrap', str(max_pargs_hwrap),
                       '--separate-ctrl-name-with-space', str(separate_ctrl_name_with_space),
                       '--separate-fn-name-with-space', str(separate_fn_name_with_space),
                       '--dangle-parens', str(dangle_parens),
                       '--dangle-align', dangle_align,
                       '--min-prefix-chars', str(min_prefix_chars),
                       '--max-prefix-chars', str(max_prefix_chars),
                       '--max-lines-hwrap', str(max_lines_hwrap),
                       '--line-ending', line_ending,
                       '--command-case', command_case,
                       '--keyword-case', keyword_case,
                       '--always-wrap', always_wrap,
                       '--enable-sort', str(enable_sort),
                       '--autosort', str(autosort),
                       '--hashruler-min-length', str(hashruler_min_length),
                       '--bullet-char', bullet_char,
                       '--enum-char', enum_char,
                       '--enable-markup', str(enable_markup),
                       '--first-comment-is-literal', str(first_comment_is_literal),
                       '--literal-comment-pattern', literal_comment_pattern,
                       '--fence-pattern', fence_pattern,
                       '--ruler-pattern', ruler_pattern,
                       '--canonicalize-hashrulers', str(canonicalize_hashrulers),
                       '--emit-byteorder-mark', str(emit_byteorder_mark),
                       '--input-encoding', input_encoding,
                       '--output-encoding', output_encoding]
        else:
            print("CMake format: invalid style, choose either default, file, or custom")
            return

        print(command)
        # Run CF, and set buf to its output.
        buf = self.view.substr(sublime.Region(0, self.view.size()))
        startupinfo = None
        if os_is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                             startupinfo=startupinfo)
        output, error = p.communicate(buf.encode(encoding))

        # Display any errors returned by cmake-format using a message box,
        # instead of just printing them to the console.
        if error:
            # We don't want to do anything by default.
            # If the error message tells us it is doing that, truncate it.
            default_message = "cmake format is wrong"
            msg = error.decode("utf-8")
            if msg.strip().endswith(default_message):
                msg = msg[:-len(default_message)-1]
            # sublime.error_message("CMake format: " + msg)
            print("CMake format: " + msg)
            # Don't do anything.
            return

        # If there were no errors, we replace the view with the outputted buf.
        # Temporarily disable tabs to space so that tabs elsewhere in the file
        # do not get modified if they were not part of the formatted selection
        prev_tabs_to_spaces = self.view.settings().get('translate_tabs_to_spaces')
        self.view.settings().set('translate_tabs_to_spaces', False)

        self.view.replace(
            edit, sublime.Region(0, self.view.size()),
            output.decode(encoding).replace("\r", ""))

        # Re-enable previous tabs to space setting
        self.view.settings().set('translate_tabs_to_spaces', prev_tabs_to_spaces)


class CmakeFormatEventListener(sublime_plugin.EventListener):
    """Hook for on-save event, to allow application of cmake-format on save."""

    def on_pre_save(self, view):
        """Check syntax and format on save prior step."""

        # Only do this for supported languages
        syntax = view.settings().get('syntax')
        if is_supported(syntax):
            # Ensure that settings are up to date.
            load_settings()
            if format_on_save:
                # Saving file manually so cmake-format runs on new contents
                body = view.substr(sublime.Region(0, view.size()))
                with open(view.file_name(), "w", encoding=input_encoding) as f:
                    f.write(body)
                    f.close()

                print("Auto-applying CMake Format on save.")
                view.run_command("cmake_format", {"whole_buffer": True})


# Called from the UI to update the path in the settings.
class CmakeFormatSetPathCommand(sublime_plugin.WindowCommand):
    """We can also update the path on the UI."""

    def run(self):
        """Update the path."""

        update_path()
