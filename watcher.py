import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TARGET_DIR = "txtfolder"
TARGET_FILE = "all_code.txt"

ALLOWED_EXT = (
    ".js",
    ".html",
    ".css",
    ".php",
    ".md",
    ".json",
    ".py"
)

IGNORE_FOLDERS = {
    "venv",
    ".venv",
    "__pycache__",
    ".git",
    "node_modules",
    "vendor",
    "watcher.py",
    TARGET_DIR
}

IGNORE_FILES = {
    "all_code.txt"
    "watcher.py"
}

os.makedirs(TARGET_DIR, exist_ok=True)

target_path = os.path.join(TARGET_DIR, TARGET_FILE)

# memory index
file_blocks = {}


def normalize_name(path):
    return path.replace("\\", "/")


def should_ignore(path):

    norm = normalize_name(path)

    parts = norm.split("/")

    for part in parts:
        if part in IGNORE_FOLDERS:
            return True

    filename = os.path.basename(path)

    if filename in IGNORE_FILES:
        return True

    if not path.endswith(ALLOWED_EXT):
        return True

    return False


def read_file(path):

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    except Exception as e:
        print(f"[ERROR READ] {path} => {e}")
        return ""


def format_block(path, content):

    name = normalize_name(path)

    return f'''file {name}
\"\"\"
{content}
\"\"\"


'''


def write_full():

    with open(target_path, "w", encoding="utf-8") as f:

        for path in sorted(file_blocks.keys()):
            f.write(file_blocks[path])


def update_file(path):

    if should_ignore(path):
        return

    content = read_file(path)

    block = format_block(path, content)

    file_blocks[path] = block

    write_full()

    print(f"[UPDATE] {path}")


def delete_file(path):

    if path in file_blocks:

        del file_blocks[path]

        write_full()

        print(f"[DELETE] {path}")


def initial_scan():

    print("🔍 Initial Scan...")

    for root, dirs, files in os.walk("."):

        # skip ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        for file in files:

            path = os.path.join(root, file)

            if not should_ignore(path):

                update_file(path)

    print("✅ Initial Scan Complete")


class Handler(FileSystemEventHandler):

    def on_modified(self, event):

        if not event.is_directory:
            update_file(event.src_path)

    def on_created(self, event):

        if not event.is_directory:
            update_file(event.src_path)

    def on_deleted(self, event):

        if not event.is_directory:
            delete_file(event.src_path)


observer = Observer()
handler = Handler()

observer.schedule(handler, ".", recursive=True)

observer.start()

print("🚀 Watching Start")

initial_scan()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()