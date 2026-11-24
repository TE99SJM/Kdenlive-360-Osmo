# Osmo 360 Editor for Kdenlive

Open a dual-lens DJI Osmo 360 recording, drag to frame the shot, set camera keyframes and render it with the original audio. The editor keeps the original recording read-only.

## Windows

Download the **Osmo360-Windows-x64** binary package, extract the ZIP, close Kdenlive and double-click **Install-Kdenlive.cmd**. The installer registers the C++/Qt 6 editor for the current Windows user. It uses FFmpeg and FFprobe from the Kdenlive bin directory or PATH. Windows packages are also produced by the [native build](https://github.com/TE99SJM/Kdenlive-360-Osmo/actions/workflows/native-windows.yml). GitHub's **Download ZIP** button on the repository gives you the source code.

The installer updates the existing **Osmo 360 Editor** Media Job. If it detects the older Python installation, it offers to archive its installed scripts in `%LOCALAPPDATA%\kdenlive\backups\osmo360-python`. Recordings and saved camera tracks can stay where they are.

In stock Kdenlive, close the Open dialog and drag a recording from File Explorer onto the **Project Bin**. Select the imported clip and open **Clip Jobs → Osmo 360 Editor** (called **Media Jobs** in some versions). Kdenlive adds the finished MP4 to **360 edits**. You can also drop a recording or a saved edit into the standalone native editor and choose where to export. A built **KdenCut 360** opens the editor automatically when an OSV or K360 is dropped onto its Project Bin.

## Build from source

With Qt 6 Widgets, CMake and a C++17 compiler installed, run `cmake -S native -B build` and `cmake --build build --config Release`. Register the built executable with `osmo360-editor --install` from its permanent location. FFmpeg needs the v360, remap, maskedmerge and sendcmd filters, libx264 and libx265. The earlier Python editor and installer are retained for existing installations.

## Reframing

Scrub to a frame and drag the picture to aim. Releasing the drag records an aim keyframe. The mouse wheel or **FOV** control changes zoom. **Pan only (lock pitch)** starts enabled on new recordings. Horizontal dragging pans at the current elevation. Disable it to aim up or down. Enter a **Roll** angle and click **Key roll** to hold that tilt until the next roll key. Existing version 1 and 2 camera tracks can be opened in the native editor. Use **Save edit** to keep the editable `.k360` track.

The progress bar animates while the editor reads camera metadata and prepares the first preview. Proxy creation and export show frame-based percentages. Kdenlive remains available while the Media Job runs. In KdenCut 360, queued imports also report progress in the main status bar and add each completed clip to its original project folder.

**Play** creates a temporary silent 1024 × 512, 8 fps playback proxy. **Render and import** reads the original at its full frame rate. For a flat clip, choose landscape, portrait or square. Choose **360 panorama** for an interactive spherical video.

## Output

| Shape | Standard | High | Video |
| --- | --- | --- | --- |
| Landscape | 1920 × 1080 | 3840 × 2160 | H.264, 8-bit |
| Portrait | 1080 × 1920 | 2160 × 3840 | H.264, 8-bit |
| Square | 1080 × 1080 | 2160 × 2160 | H.264, 8-bit |
| 360 panorama | Up to 3840 × 1920 | Up to 7680 × 3840 | HEVC, 10-bit, spherical metadata |

Panorama exports cover the whole sphere and ignore camera keyframes. The editor shows the selected export dimensions alongside the quality setting. The editor uses factory lens geometry when available and shows “Generic lens geometry” if it uses the fallback. Close objects crossing the seam can show parallax. The editor has no motion tracking, gyro horizon lock, optical-flow seam correction or D-Log M grading. Full-resolution CPU rendering can take longer than playback.

Lens projection math is adapted from [PanoForge](https://github.com/Belenos-Toutatis/PanoForge) under the included MIT license. The editor uses GPL-3.0-or-later. See [LICENSE](LICENSE) and [LICENSE-PanoForge](LICENSE-PanoForge).

## Verification

Run `ctest --test-dir build -C Release --output-on-failure` to check the native pipeline. Its integration test covers 4K flat export, spherical metadata, audio, frame counts, held roll, a fractional-rate clip, last-frame playback, and fallback to the original when a proxy is unreadable. Run `python3 -m unittest discover -s tests -v` for the older Python editor.
