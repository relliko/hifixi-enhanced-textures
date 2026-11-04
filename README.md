# HiFi XI texture pack

Sharper textures for FINAL FANTASY XI on Phoenix, for players of the HiFi XI plugin. The scenery, ships, furniture and
characters' gear and hair are drawn at two to four times the game's own resolution.

The pack never changes a game file. HiFi XI reads it from its own folder and keeps it on the graphics card, so the game
itself still loads its small original files and its memory stays small. Anything the pack doesn't have is drawn with the
game's own texture.

## What you need

- **HiFi XI 0.67 or newer.** 0.66 does scenery only; 0.67 adds characters.
- **About 7 GB of disk space** for the pack folder.
- **A graphics card with 4 GB of memory or more.** A typical area takes 100 to 250 MB of it, a crowded city more. When the
  card is nearly full, HiFi XI skips the sharpest level of new textures and then hands the least recently seen characters
  back to the game's textures, so a smaller card still works, just less sharply.

## Make the pack on your own PC

This repository is the tool that makes the pack, `hifixi-texpack.exe`. It reads your own game files, makes each texture
bigger with the Real-ESRGAN upscaler on your graphics card, keeps every hand-painted texel's colour, and writes the pack
folder HiFi XI reads. It never changes a game file and writes only into the pack folder.

1. **Get the tool.** Download `hifixi-texpack-v0.1.zip` from this repository's
   [releases](https://github.com/relliko/hifixi-enhanced-textures/releases) and unzip it anywhere (not inside the game's
   folder). Or build it yourself with `build.cmd` (Visual Studio 2022 or newer with "Desktop development with C++"); it
   ends up in `build\hifixi-texpack.exe`. Run the commands below in a command prompt in the tool's folder.
2. **Get the upscaler** (once). The tool doesn't include it: it downloads the authors' own release from GitHub after you
   say yes, checks its size and SHA-256, and keeps only what it needs, next to the tool in `upscaler\`:

   ```
   hifixi-texpack get-upscaler
   ```

   Real-ESRGAN is xinntao's (BSD-3-Clause; the Windows program MIT, with Tencent's ncnn, BSD-3-Clause). Details:
   [docs/texture-pack/upscaler.md](docs/texture-pack/upscaler.md).
3. **Close the game and make the pack:**

   ```
   hifixi-texpack make --out C:\Games\PhoenixXI\bootloader\hifixi-pack
   ```

   It finds the game folder itself (or give `--ffxi "<...>\SquareEnix\FINAL FANTASY XI"`). Scenery is made at 2x, models
   at 4x. It takes hours: a few for the whole game on a fast graphics card, longer on a slower one. For a quicker pack
   with the scenery only, add `--kind zone`.
   - It runs at low priority. If you start the game while it works, it stops the upscaler and waits; it carries on by
     itself a minute after you close the game.
   - To stop it, press Ctrl+C or create a file named `stop` in the pack folder. Run the same command again and it
     carries on where it stopped.
   - `progress.txt` in the pack folder says how far it is, and HiFi XI's menu shows the same in its "Texture pack"
     section. `texpack.log` there has everything it printed.
4. Turn the pack on in game as in [Install a pack you already have](#install-a-pack-you-already-have) step 3.

When Phoenix updates the game, run `make` again: it redoes only what changed.

## Install a pack you already have

1. Close the game.
2. Unzip the pack so you have a folder named `hifixi-pack` inside the `bootloader` folder, next to HiFi XI's `dxgi.dll` and
   `d3d8.dll`. On Phoenix that is usually:

   ```
   C:\Games\PhoenixXI\bootloader\hifixi-pack\pack.idx
   C:\Games\PhoenixXI\bootloader\hifixi-pack\pack-000.bin
   ...
   C:\Games\PhoenixXI\bootloader\hifixi-pack\pack-006.bin
   ```

   `pack.idx` and every `pack-NNN.bin` file must be there. Make sure you didn't end up with `hifixi-pack\hifixi-pack\`.
3. Start the game. Open the HiFi XI menu (`/hifi`), go to the game's tab, and tick **Use the texture pack** in the "Texture
   pack" section at the bottom. Or type:

   ```
   /hifi textures on
   ```

   The section only appears when HiFi XI finds the folder. The setting is saved, so it stays on next time.

## What you'll see

- **Characters** switch to the pack within a second or two.
- **Scenery** switches at the next area you enter, not the one you're standing in. After you arrive somewhere, the ground and
  walls look soft for 2 to 4 seconds and then sharpen. That is the pack loading in the background, not a bug.
- The menu's "Texture pack" section shows how much of the current area and of the characters around you comes from the pack,
  for example "This area: 27 of 29 scenery textures from the pack". A few textures are never in it; they stay as the game's.
- **Mog Houses** stay as the game draws them (HiFi XI doesn't draw those rooms itself), but characters in them still get
  the pack.
- **Areas served by another XIPivot overlay** (for example the zitah-canopy overlay in The Sanctuary of Zi'Tah) keep that
  overlay's look and get nothing from the pack.
- **Gear that uses colour palettes** stays at the game's own resolution.

## Commands

| Command | What it does |
|---|---|
| `/hifi textures on` | Use the pack (saved). Scenery switches at the next area. |
| `/hifi textures off` | Stop using it (saved). Everything goes back to the game's own textures at once. |
| `/hifi textures compare` | Flip to the game's textures and back, to compare. Frees nothing, switches at once. |
| `/hifi textures reload` | Read the pack folder again, for example after replacing it. |
| `/hifi textures status` | What the pack is doing: how much is loaded, on the graphics card, and why anything was left out. |

## If something is wrong

- **No "Texture pack" section in the menu:** the folder isn't where HiFi XI looks. Check step 2 of Install, then
  `/hifi textures reload`.
- **"Texture pack can't be used: ..."** in the menu: the folder is damaged or incomplete, or a file is missing. Copy the whole
  folder again (with the game closed) and `/hifi textures reload`.
- **Some textures stay soft:** a pack is made from one set of game files. Where Phoenix's files have changed since, those
  textures simply aren't upgraded; nothing breaks.
- **The game hangs or crashes:** after a graphics card crash HiFi XI starts the next session with the pack off. Type
  `/hifi textures on` to use it again, and please send the crash report and `bootloader\hifixi.log`.

## Uninstall

1. Type `/hifi textures off` (or untick "Use the texture pack").
2. Close the game and delete the `bootloader\hifixi-pack` folder.

Nothing else was changed, so nothing else needs undoing.

## Notes

The pack is the game's own textures upscaled. FINAL FANTASY XI and its artwork belong to SQUARE ENIX. This pack is an
unofficial fan modification, not made or supported by Square Enix or by Phoenix.

## For developers

The sources here are copied from [HiFi XI](https://github.com/relliko/hifixi), which keeps the pack format its plugin
reads (`SOURCE.txt` names the commit; `tools/synced.txt` lists the files). Change them there, then
`python -I tools/sync_from_hifixi.py <hifixi checkout>`. `build\texpack_test.exe` runs the tests; the ones that need
the game's files skip themselves when the game isn't installed. The pack format: `docs/texture-pack/format.md`.
