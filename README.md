# BananaSplit
BananaSplit.py is a Python 3 script for rendering After Effects compositions in automagically compressed chunks.

## Requirements
Both [After Effects](http://www.adobe.com/products/aftereffects.html) (obviously) and [ffmpeg](https://www.ffmpeg.org/) must be installed.

Additionally, ffmpeg.exe (found in FFmpeg's /bin folder) and aerender.exe (found in After Effect's install location with AfterFX.exe) must also be added to the system's shell path for the script to work properly.

[Tutorial on Modifying Windows' Shell Path](http://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/)

[Tutorial on Modifying OS X's Shell Path](http://coolestguidesontheplanet.com/add-shell-path-osx/)

## Cross-platform Compatibility?
BananaSplit should work on all Windows systems (tested) and OS X systems (untested) that After Effects can be installed on.

## I accidentally deleted my fragmentList.txt! What do?
First off, check to see if you have a fragmentList.bak from a previous render. If the project's basic properties have remained unchanged, using that may work.

Otherwise, reconstructing a fragmentList.txt is easy, and follows FFmpeg's concatenation file syntax. See [here](https://trac.ffmpeg.org/wiki/Concatenate#Instructions) for more information.
