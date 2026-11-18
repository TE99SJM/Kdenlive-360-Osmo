# Osmo 360 Editor for Kdenlive

Open a dual-lens DJI Osmo 360 recording, drag to frame the shot, set camera keyframes and render it with the original audio. The editor keeps the original recording read-only.

## Install and open

Use a desktop installation of Python 3.10 or later with Tk, NumPy and Pillow, and FFmpeg and FFprobe on PATH. FFmpeg needs the v360, remap, maskedmerge and sendcmd filters, libx264 and libx265. On Debian/Ubuntu the packages are `python3-tk python3-numpy python3-pil ffmpeg`. Download and extract the repository ZIP or clone it. With Kdenlive closed, run `python3 install.py` from the repository folder using that Python interpreter. For a nonstandard installation, use `--data-dir` to select Kdenlive's writable application-data directory. Sandboxed packages need access to the interpreter, FFmpeg and footage.

In Kdenlive, import the original OSV, select its first clip in the bin, then open **Clip → Clip Jobs → Osmo 360 Editor**. In versions that label the submenu **Media Jobs**, use that submenu. If the file picker hides the extension, choose **All Files**. The job reads both lenses from the original file. Kdenlive chooses the MP4 destination alongside the source and adds it to **360 edits** on success. For read-only camera cards or an alternate destination, launch `python3 editor.py` directly and import the exported MP4 into Kdenlive.

## Reframing

Scrub to a frame, then drag the picture to aim. Releasing the drag adds a camera keyframe. The FOV slider changes the zoom and Roll tilts the view. Use the arrow buttons to visit adjacent keys and Undo to reverse the last camera change. **Save edit** writes an editable `.k360` camera track. Reopen a saved track with `python3 editor.py your-edit.k360`.

**Pan only (lock pitch)** is on for new recordings. Drag left or right to pan. Vertical mouse movement is ignored, so the view stays at its current elevation. Uncheck it to aim up or down. To tilt the horizon deliberately, scrub to the frame, type an angle next to **Roll**, and click **Key roll**. Releasing the Roll slider also sets a roll key. New recordings start at 0° roll and hold each chosen angle until the next roll key. Panning and zooming have their own keyframes. Existing saved edits keep their original camera movement.

**Play** creates a temporary silent 8 fps proxy. **Render and import** reads the original at its full frame rate. For a flat clip, choose landscape, portrait or square. Choose **360 panorama** for an interactive spherical video.

## Output

| Shape | Standard | High | Video |
| --- | --- | --- | --- |
| Landscape | 1920 × 1080 | 3840 × 2160 | H.264, 8-bit |
| Portrait | 1080 × 1920 | 2160 × 3840 | H.264, 8-bit |
| Square | 1080 × 1080 | 2160 × 2160 | H.264, 8-bit |
| 360 panorama | Up to 3840 × 1920 | Up to 7680 × 3840 | HEVC, 10-bit, spherical metadata |

Panorama exports cover the whole sphere and ignore camera keyframes. The editor uses factory lens geometry when available and shows “Generic lens geometry” if it uses the fallback. Close objects crossing the seam can show parallax. The editor has no motion tracking, gyro horizon lock, optical-flow seam correction or D-Log M grading. Full-resolution CPU rendering can take longer than playback.

Lens projection math is adapted from [PanoForge](https://github.com/Belenos-Toutatis/PanoForge) under the included MIT license. The editor uses GPL-3.0-or-later. See [LICENSE](LICENSE) and [LICENSE-PanoForge](LICENSE-PanoForge).

## Verification

Run `python3 -m unittest discover -s tests -v` with the dependencies above. Tests cover camera interpolation, installer registration, a flat and spherical render, audio, frame counts, and cancellation. The Linux clip-job workflow was tested in Kdenlive 24.12.3. A full 1,376-frame original Osmo recording and a short 4K spherical export were also checked. Windows and macOS installations still need verification.
