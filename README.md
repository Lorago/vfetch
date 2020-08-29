<h1 align="center">vfetch</h1>
<p align="center">
  A simple fetch tool for Linux written in Python.
  <br><br>
  <img src="https://imgur.com/fBCvikM.png">
</p>

## Dependencies
* [python](https://www.python.org/) - For obvious reasons.
* [distro](https://github.com/nir0s/distro) - Python library for getting the machine's Linux distribution.
* [pyxdg](https://freedesktop.org/wiki/Software/pyxdg/) - Python library used to get the $XDG_CONFIG_HOME file path.

## Installation
Download the repository and add a symbolic link to the `vfetch.py` script in your `/usr/bin/` directory:

    $ git clone https://github.com/Lorago/vfetch.git
    $ sudo ln -s vfetch/vfetch.py /usr/bin/vfetch

You can then run the script with a simple

    $ vfetch

## Configuration
The default configuration is located in the same folder as the `vfetch.py` file, and is called `vfetch.conf`. This file should not be removed, moved, or edited.
To configure the script, make a copy of the configuration to `$XDG_CONFIG_HOME/vfetch/vfetch.conf`, which will usually be `~/.config/vfetch/vfetch.conf`.
If the script does not find a file in this directry it will use the default configuration file. By default the vfetch output will look similar to this:

<p align="center"><img src="https://imgur.com/MphO1Cq.png"></p>

### Options

Note that all option values that are not integers or booleans (`true` or `false`) need to be surrounded by
quotation marks as the configuration file is a `JSON` file.

#### alignMode
The `alignMode` option sets the data align mode for the output. Acceptable values are `spaces` and `center`.

#### alignSpace
The `alignSpace` option sets the shortest space between the data names and values when the `alignMode` is set to
`spaces`. Acceptable values are positive integers.

#### colorIndex
The `colorIndex` option sets the index of the terminal color (from 0 to 15) to use for the data names. Acceptable
values are 0-15.

#### displayAscii
The `displayAscii` option sets whether to display an ascii image at the top left corner of the output. Acceptable
values are `true` and `false`.

#### asciiImage
The `asciiImage` option sets the file path for the ascii image used if the `displayAscii` option is set to `true`.
Acceptable values are file paths to text files.

#### iconMode
The `iconMode` option sets whether to replace the data names with NERD Font icons. Acceptable values are `true` and
`false`.

#### lowercase
The `lowercase` option sets whether to lowercase all text. Acceptable values are `true` and `false`.

#### removeLinux
The `removeLinux` option sets whether to remove the text `Linux` (case-independent) from the `OS` data. Acceptable
values are `true` and `false`.

#### kernelFullName
The `kernelFullName` options sets whether to display the full kernel name or to cut off at the first `-` (e.g.
`5.8.4-arch1-1` becomes `5.8.4`). Acceptable values are `true` and `false`.

#### displayArchitecture
The `displayArchitecture` option sets whether to display the current system architecture after the `OS` name (e.g.
`arch linux x86_64` becomes `arch linux`). Acceptable values are `true` and `false`.

#### displayPackageManager
The `displayPackageManager` option sets whether to display the package manager in parentheses after the number of
packages. Acceptable values are `true` and `false`.

#### data
The `data` option sets what data to display and in what order. Values are separated by commas. Acceptable values
are `os`, `kernel`, `uptime`, `packages`, and `wm`.

#### offset
The `offset` option sets the offset of the data from the edge or the ascii image (in both the x- and y-directions).
Acceptable values are two different positive integer values (one for the offset in the x-direction, and one for the
offset in the y-direction).
