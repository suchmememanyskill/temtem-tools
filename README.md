# temtem-tools
Some tools i wrote for temtem

This uses parts of the windows api. This will probably not work on linux, but i have not tried it

## How to use

### First time setup
1. Install python (and check the "Add to path" option in the installer)
2. Download the code as zip, unzip it, then open a command prompt in this unzipped folder
3. Type in `pip install -r requirements.txt`

### How to launch
1. Open a command prompt in the source folder
2. Type in `py CounterTAPI.py`. You will be asked what temtem you are hunting. The encounter count will be stored in the json with the provided name, so you can retrieve it later
3. Play temtem and go hunting. The counter will automatically count up how many temtem you encounter. (Note it will not distinguish temtem, so any encounter is counted)
4. Press '0' to save and quit