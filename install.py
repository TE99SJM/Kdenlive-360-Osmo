#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install a user-scoped stock Kdenlive Media Job, preserving other jobs."""

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

JOB = "osmo360reframe"
FILES = (
    "editor.py",
    "media.py",
    "camera.py",
    "engine.py",
    "lensmaps.py",
    "spherical.py",
    "LICENSE-PanoForge",
)


def default_dir():
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/kdenlive"
    if os.name == "nt":
        return Path(os.environ["LOCALAPPDATA"]) / "kdenlive"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "kdenlive"


def job_settings(old, records):
    lines = old.splitlines()
    for group, value in records.items():
        heading = "[" + group + "]"
        if heading not in lines:
            lines.extend(["", heading])
        start = lines.index(heading) + 1
        end = next((i for i in range(start, len(lines)) if lines[i].startswith("[")), len(lines))
        matches = [i for i in range(start, end) if re.match(r"^" + JOB + r"\s*=", lines[i])]
        setting = JOB + "=" + value
        if matches:
            lines[matches[0]] = setting
        else:
            lines.insert(start, setting)
    return "\n".join(lines) + "\n"


def install(root):
    from importlib import import_module

    for name in ("tkinter", "numpy", "PIL.Image"):
        import_module(name)

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit(f"{tool} must be available on PATH.")
    root = Path(root).resolve()
    dest = root / "scripts" / "osmo360"
    dest.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    if source != dest:
        for name in FILES:
            shutil.copy2(source / name, dest / name)
    config = root / "clipjobsettings.rc"
    original = config.read_text(encoding="utf8") if config.exists() else ""
    # Qt accepts forward slashes on Windows paths; KConfig reserves backslashes.
    script = (dest / "editor.py").as_posix()
    if '"' in script:
        raise ValueError("The Kdenlive data folder cannot contain a double quote.")
    entries = {
        "Ids": "Osmo 360 Editor",
        "Binary": Path(sys.executable).as_posix(),
        "Parameters": f'"{script}" {{source}} --output {{output}}',
        "Output": "osmo360.mp4",
        "FolderUse": "subfolder",
        "FolderName": "360 edits",
        "EnabledTypes": "v",
    }
    updated = job_settings(original, entries)
    if updated != original:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf8", delete=False, dir=root) as out:
            out.write(updated)
        os.replace(out.name, config)
    return dest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_dir())
    args = parser.parse_args()
    print("Installed in", install(args.data_dir))
    print("Restart Kdenlive. Select the bin clip and choose Clip > Clip Jobs (or Media Jobs) > Osmo 360 Editor.")
