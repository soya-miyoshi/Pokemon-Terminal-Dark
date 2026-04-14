# Pokemon-Terminal (Dark Edition)

> This is a fork of [LazoCoder/Pokemon-Terminal](https://github.com/LazoCoder/Pokemon-Terminal) with all Pokemon images darkened. The base color of each Pokemon is detected and shifted to a dark variant while preserving the original hue, making it suitable for dark terminal themes. See `darken_pokemon.py` for the conversion script.
>
> This fork also adds 24 extra images (trainers, alt forms, anniversary art, etc.) sourced from [pldh.net's Rarities & B-Sides gallery](https://pldh.net/gallery/rarities) — these are **not** included in the upstream repo. They're run through the same darkening pass as the rest, so `pokemon -e` stays consistent with the main set.
>
> I install this fork from my own [dotfiles](https://github.com/soya-miyoshi/dotfiles) — see the [venv + `~/.local/bin` symlink](#venv--locallocalbin-symlink) section below for the pattern.

[![Build Status](https://travis-ci.org/LazoCoder/Pokemon-Terminal.svg?branch=master)](https://travis-ci.org/LazoCoder/Pokemon-Terminal)

![025 - Pikachu](https://github.com/user-attachments/assets/69829029-5d73-4596-bd3c-09994e4bbec2)
![107](https://github.com/user-attachments/assets/7b3b385e-ab08-47e7-bed5-e0dd5340e4ee)
![088](https://github.com/user-attachments/assets/877417d1-d9eb-461f-85f2-ec7b1d0c11b1)
![072](https://github.com/user-attachments/assets/11c123d2-57a7-472d-8392-3d2230af76d5)
![rotom-heat](https://github.com/user-attachments/assets/630e5275-ea00-49be-b092-f9a1f99577d9)
![sawsbuck-summer](https://github.com/user-attachments/assets/74ef3375-e132-4447-8e83-70b5fb0de325)

# Features
- 719 unique Pokemon
- Select Pokemon by name or by index number
- Ability to change the Desktop Wallpaper & the Terminal background
- Internal search system for finding Pokemon
- Supports iTerm2, ConEmu, Terminology, Windows Terminal, Tilix and Kitty terminal emulators
- Supports Windows, MacOS, GNOME, Openbox (with feh), i3wm (with feh) and sway for desktops

# Installation

Install Python 3.7 or higher:
- [For Mac](https://www.python.org/downloads/mac-osx/)
- For Windows: [desktop](https://www.python.org/downloads/windows/) or [Microsoft Store](https://www.microsoft.com/p/python-38/9mssztt1n39l)
- [For Ubuntu](https://askubuntu.com/a/865569)
- [For Arch Linux](https://www.archlinux.org/packages/extra/x86_64/python/)
- Not all compatible distros are named here, but a quick Google search should give you instructions for your distribution of choice.

Get a compatible terminal emulator:
- [iTerm2](https://iterm2.com/)
- [ConEmu](https://conemu.github.io/) or derivative (such as [Cmder](http://cmder.net/))
- [Terminology](https://www.enlightenment.org/about-terminology)
- [Tilix](https://gnunn1.github.io/tilix-web/)
- [Windows Terminal](https://www.microsoft.com/p/windows-terminal-preview/9n0dx20hk701)
- [Kitty](https://sw.kovidgoyal.net/kitty/) from version `0.27.0` onwards

The only reliable way to install this fork is directly from the repo — the upstream `pip` and `npm` packages don't ship the darkened sprites or the extras. Pick one of:
- [venv + `~/.local/bin` symlink (recommended)](#venv--locallocalbin-symlink)
- [Distutils (System-wide or Per-User)](#distutils)

## venv + `~/.local/bin` symlink

This is how I install the fork from my own [dotfiles](https://github.com/soya-miyoshi/dotfiles) (see `run_once_after_03_install_pokemon_terminal.sh.tmpl`): clone the repo, install it into a local `python3 -m venv`, and symlink the generated `pokemon` entry point into `~/.local/bin` so it's on your `PATH` without polluting the system Python.

```bash
git clone https://github.com/soya-miyoshi/Pokemon-Terminal-Dark.git
cd Pokemon-Terminal-Dark

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
deactivate

mkdir -p "$HOME/.local/bin"
ln -sf "$PWD/.venv/bin/pokemon" "$HOME/.local/bin/pokemon"
```

Make sure `~/.local/bin` is on your `PATH`, then `pokemon` is ready to go.

## Distutils

This doesn't works on Microsoft Store installations of Python.

You can clone or [download](https://github.com/LazoCoder/Pokemon-Terminal/archive/master.zip) this repo, and run `python3 setup.py install` at the root of the repo.

If you want a system-wide install, run the command as superuser or administrator.

If you want a per-user install, append the `--user` flag. Look at the pip directives to add a per-user install to your `PATH`.

# Usage

```
usage: pokemon [-h] [-n NAME]
               [-r [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]]]
               [-l [0.xx]] [-d [0.xx]]
               [-t [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]]]
               [-ne] [-e] [-ss [X]] [-w] [-v] [-dr] [-c]
               [id]

Set a pokemon to the current terminal background or wallpaper

positional arguments:
  id                    Specify the wanted pokemon ID or the exact (case
                        insensitive) name

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear           Clears the current pokemon from terminal background
                        and quits.

Filters:
  Arguments used to filter the list of pokemons with various conditions that
  then will be picked

  -n NAME, --name NAME  Filter by pokemon which name contains NAME
  -r [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]], --region [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]]
                        Filter the pokemons by region
  -l [0.xx], --light [0.xx]
                        Filter out the pokemons darker (lightness threshold
                        lower) then 0.xx (default is 0.7)
  -d [0.xx], --dark [0.xx]
                        Filter out the pokemons lighter (lightness threshold
                        higher) then 0.xx (default is 0.42)
  -t [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]], --type [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]]
                        Filter the pokemons by type.
  -ne, --no-extras      Excludes extra pokemons (from the extras folder)
  -e, --extras          Excludes all non-extra pokemons

Misc:
  -ss [X], --slideshow [X]
                        Instead of simply choosing a random pokemon from the
                        filtered list, starts a slideshow (with X minutes of
                        delay between pokemon) in the background with the
                        pokemon that matched the filters
  -w, --wallpaper       Changes the desktop wallpaper instead of the terminal
                        background
  -v, --verbose         Enables verbose output
  -dr, --dry-run        Implies -v and doesn't actually changes either
                        wallpaper or background after the pokemon has been
                        chosen

Not setting any filters will get a completely random pokemon
```

Example:

![](https://i.imgur.com/DfA2lcd.gif)

# Tips, tricks and common issues

## iTerm2 settings

I highly suggest making the font colors black and the terminal window transparent. Some of the images have both light and dark colours and so it can be difficult to see the text sometimes. Transparency resolves this issue. Since *Pokemon-Terminal* only changes the background, the transparency must be done manually:

1. Navigate to iTerm2 > Preferences > Profiles > Window
2. Set the transparency to about half way.
3. Hit the "blur" checkbox.
4. Set the blur to maximum.
5. Optionally you can set the blending to maximum to adjust the colors to look like the samples provided.

![](https://i.imgur.com/xSZAGhL.png)

The result should look like this:

![](https://i.imgur.com/82DAT97.jpg)

## ConEmu settings

1. From the menu under the symbol at left of title bar, navigate to Settings > Main > Background
2. Set Darkening to maximum (255).
3. Set Placement to Stretch.
4. Click Save Settings.
5. Optionally you apply transparency under Features > Transparency.

## Windows Terminal settings

You can, like in iTerm2, enable transparency. Simply press the down arrow in the tab bar and click settings. Once the JSON file opens, add the following settings under the `defaults` section:

```json
"backgroundImageOpacity": 0.5,
"useAcrylic": true,
"acrylicOpacity": 0.0
```

The result should look like this:

![](https://i.imgur.com/DZbiQHf.png)

## Kitty settings

To dynamically set background images in kitty, we use its [remote control feature](https://sw.kovidgoyal.net/kitty/overview/#remote-control). It is not enabled by default, and can be configured to be password protected.

The way passwords work for kitty remote control is that you set one or more passwords, each granting some amount of permissions (see [the docs](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) for details).

Here's an example of how to set it up in `./config/kitty/kitty.conf`:

```
# Enable remote control (password protected)
allow_remote_control password

# Option 1: Allow setting the background image with a password
remote_control_password "missingno" set-background-image

# Option 2: Allow setting the background image without a password
# (slightly less secure, a malicious actor could mess up your backgrounds)
remote_control_password "" set-background-image
```

If you choose option 1 (recommended), you still need to pass your chosen password when running `pokemon`, this works using the environment variable `KITTY_RC_PASSWORD` - i.e. you can run `KITTY_RC_PASSWORD=missingno pokemon`, or set the variable in any other way using your method of choice.

## Adding Custom Images

The folder `pokemonterminal/Images/Extra` is for adding custom images. You can manually add backgrounds to this folder and they will be visible to the program. Only JPG format is supported. To see a list of all the custom backgrounds type:
```bash
$ pokemon -e -dr
```
Alternatively, you can delete images from this folder and it will not break the program. These are some custom backgrounds:

![](https://i.imgur.com/gdGUucu.gif)

## Solutions for Common Issues

* If you experience a line at the top of the terminal after changing the Pokemon, you can remove it by typing in the `clear` command or opening a new terminal.
![](https://i.imgur.com/5HMu1jD.png)

* If you are using Tilix and the terminal background is not changing, try adjusting the transparency in your profile settings.
* If you are experiencing issues with Terminology and are running on Ubuntu, make sure that you have installed the latest version:
   ```bash
   $ sudo add-apt-repository ppa:niko2040/e19
   $ sudo apt-get update
   $ sudo apt install terminology
   ```

## Saving

### iTerm2
To save a background you will need to setup a startup command in the profile:
1. Navigate to iTerm2 > Preferences > General
2. Locate the field where it says *Send text at start* under *Command*.
3. In that field type `pokemon -n [pokemon name]`. You can see an example in the image down below.
   - Alternatively you can also type `pokemon` for a random theme each time you open up a new terminal.
4. You can leave out `; clear` if you don't care about the line showing up at the top of the terminal.

![](https://i.imgur.com/2d4qa9j.png)

### ConEmu
After setting your desired pokemon, from the menu under the symbol at left of title bar, navigate to Settings > Main > Background and click Save Settings.

### Terminology
Terminology already saves it automatically, just untick "temporary" in the settings after setting your desired Pokemon:
![](http://i.imgur.com/BTqYXKa.png)

To show a random Pokemon each session:
1. Open `~/.bashrc` in your favorite text editor.
2. Add the following lines to it:
   ```bash
   if [[ "$TERMINOLOGY" -eq "1" ]]; then
       pokemon
   fi
   ```
That will simply pick a completely random Pokemon each session, but the `pokemon` line is simply calling the app, so you can still filter with regions, darkness, and etc. like you normally would, or you can also reset to a preset Pokemon every time you start.

# Notes & Credits

- Nearly all of the Pokemon backgrounds were created by [Teej](https://pldh.net/gallery/the493).
- Originally the images were about 100mb in total but [ImageOptim](https://imageoptim.com/) was used to compress them down to about 17mb.
- Since the images are compressed, some of them may have some mild (but negligible) compression artifacts.
- Platforms:
  - Thanks to [@samosaara](https://github.com/samosaara) for the Linux (GNOME and Terminology) port.
  - Thanks to [@jimmyorourke](https://github.com/jimmyorourke) for the Windows (ConEMU and wallpaper) port.
  - Thanks to [@sylveon](https://github.com/sylveon) for the Windows slideshow functionality and maintaining the AUR package.
- Terminal & wallpaper support:
  - Thanks to [@MattMattV](https://github.com/MattMattV) for adding Tilix support.
  - Thanks to [@regenbogencode](https://github.com/regenbogencode) for sway support.
  - Thanks to [@kyle-seongwoo-jun](https://github.com/kyle-seongwoo-jun) for Windows Terminal support.
- Thanks to [@DrMartinLutherXing](https://github.com/DrMartinLutherXing) for some bug fixes.
- Thanks to [@joanbono](https://github.com/joanbono) for the easy installation script in the readme.
- Thanks to [@BnMcG](https://github.com/BnMcG) for the region specific randomize function.
- Thanks to [@therealklanni](https://github.com/therealklanni) for adding the project to npm.
- Thanks to [@connordinho](https://github.com/connordinho) for enhancing the slideshow functionality.
- Thanks to [@cclauss](https://github.com/cclauss) for simplifying the code in the database class and the main class, as well as general code quality fixes.
- Thanks to [@Fiskie](https://github.com/Fiskie) for implementing the adapter design pattern, piping commands and more.
- Thanks to [@marcobiedermann](https://github.com/marcobiedermann) for better image compression.
- Thanks to [@kamil157](https://github.com/kamil157) and [@dosman711](https://github.com/dosman711) for the randomized slideshow function.
- Thanks to [@Squirrels](https://github.com/Squirrels) for adding Pokemon from the Unova and Kalos regions.
- Thanks to [@caedus75](https://github.com/caedus75) for pip and reorganizing the files & folders.
