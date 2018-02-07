import sublime, sublime_plugin
import subprocess, os

# Settings file locations.
settings_file = 'cmake_format.sublime-settings'
custom_style_settings = 'cmake_format_custom.sublime-settings'

st_encodings_trans = {
   "UTF-8" : "utf-8",
   "UTF-8 with BOM" : "utf-8-sig",
   "UTF-16 LE" : "utf-16-le",
   "UTF-16 LE with BOM" : "utf-16",
   "UTF-16 BE" : "utf-16-be",
   "UTF-16 BE with BOM" : "utf-16",
   "Western (Windows 1252)" : "cp1252",
   "Western (ISO 8859-1)" : "iso8859-1",
   "Western (ISO 8859-3)" : "iso8859-3",
   "Western (ISO 8859-15)" : "iso8859-15",
   "Western (Mac Roman)" : "mac-roman",
   "DOS (CP 437)" : "cp437",
   "Arabic (Windows 1256)" : "cp1256",
   "Arabic (ISO 8859-6)" : "iso8859-6",
   "Baltic (Windows 1257)" : "cp1257",
   "Baltic (ISO 8859-4)" : "iso8859-4",
   "Celtic (ISO 8859-14)" : "iso8859-14",
   "Central European (Windows 1250)" : "cp1250",
   "Central European (ISO 8859-2)" : "iso8859-2",
   "Cyrillic (Windows 1251)" : "cp1251",
   "Cyrillic (Windows 866)" : "cp866",
   "Cyrillic (ISO 8859-5)" : "iso8859-5",
   "Cyrillic (KOI8-R)" : "koi8-r",
   "Cyrillic (KOI8-U)" : "koi8-u",
   "Estonian (ISO 8859-13)" : "iso8859-13",
   "Greek (Windows 1253)" : "cp1253",
   "Greek (ISO 8859-7)" : "iso8859-7",
   "Hebrew (Windows 1255)" : "cp1255",
   "Hebrew (ISO 8859-8)" : "iso8859-8",
   "Nordic (ISO 8859-10)" : "iso8859-10",
   "Romanian (ISO 8859-16)" : "iso8859-16",
   "Turkish (Windows 1254)" : "cp1254",
   "Turkish (ISO 8859-9)" : "iso8859-9",
   "Vietnamese (Windows 1258)" :  "cp1258",
   "Hexadecimal" : None,
   "Undefined" : None
}


# Check if we are running on a Windows operating system
os_is_windows = os.name == 'nt'


# The default name of the cmake-format executable
default_binary = 'cmake-format'


# This function taken from Stack Overflow response:
# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
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


# Set the path to the binary in the settings file.
def set_path(path):
    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    sublime.save_settings(settings_file)
    # Make sure the globals are updated.
    load_settings()


# Display input panel to update the path.
def update_path():
    load_settings()
    w = sublime.active_window()
    w.show_input_panel("Path to cmake-format: ", binary, set_path, None, None)


# Check that the binary can be found and is executable.
def check_binary():
    # If we couldn't find the binary.
    if (which(binary) == None):
        # Try to guess the correct setting.
        if (which(default_binary) != None):
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


# Load settings and put their values into global scope.
# Probably a nicer way of doing this, but it's simple enough and it works fine.
def load_settings():
    # We set these globals.
    global binary
    global format_on_save
    settings_global = sublime.load_settings(settings_file)
    settings_local = sublime.active_window().active_view().settings().get('CmakeFormat', {})
    load = lambda name, default: settings_local.get(name, settings_global.get(name, default))
    # Load settings, with defaults.
    binary         = load('binary', default_binary)
    format_on_save = load('format_on_save', False)

def is_supported(lang):
    load_settings()
    return lang.endswith(('CMake' + '.tmLanguage', 'CMake' + '.sublime-syntax'))

# Triggered when the user runs cmake format.
class CmakeFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit, whole_buffer=False):
        load_settings()

        if not check_binary():
            return

        # The below code has been taken and tweaked from llvm.
        encoding = st_encodings_trans[self.view.encoding()]
        if encoding is None:
            encoding = 'utf-8'

        command = [binary, str(self.view.file_name())]

        print(command)
        # Run CF, and set buf to its output.
        buf = self.view.substr(sublime.Region(0, self.view.size()))
        startupinfo = None
        if os_is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p   = subprocess.Popen(command, stdout=subprocess.PIPE,
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
            sublime.error_message("CMake format: " + msg)
            # Don't do anything.
            return

        # If there were no errors, we replace the view with the outputted buf.
        # Temporarily disable tabs to space so that tabs elsewhere in the file
        # do not get modified if they were not part of the formatted selection
        prev_tabs_to_spaces = self.view.settings().get('translate_tabs_to_spaces')
        self.view.settings().set('translate_tabs_to_spaces', False)

        self.view.replace(
            edit, sublime.Region(0, self.view.size()),
            output.decode(encoding))

        # Re-enable previous tabs to space setting
        self.view.settings().set('translate_tabs_to_spaces', prev_tabs_to_spaces)

# Hook for on-save event, to allow application of cmake-format on save.
class CmakeFormatEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        # Only do this for supported languages
        syntax = view.settings().get('syntax')
        if is_supported(syntax):
            # Ensure that settings are up to date.
            load_settings()
            if format_on_save:
                print("Auto-applying CMake Format on save.")
                view.run_command("cmake_format", {"whole_buffer": True})


# Called from the UI to update the path in the settings.
class CmakeFormatSetPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_path()
