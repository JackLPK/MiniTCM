# MiniTCM
A very mini/simple script (PDF) writer for Traditional Cchinese Medidine (TCM). 

## To build executable:
Make spec. For Windows, use `;` inside `--add-data` argument. For Linux and MacOS, use `:` inside `--add-data` argument
```
pyi-makespec run.py \
	--windowed \
	--name "MiniTCM" \
	--add-data "./minitcm/resources;minitcm/resources" 
```
Build.
```
pyinstaller MiniTCM.spec
```
Run.
```
./dist/MiniTCM/MiniTCM.exe    # Windows
# or 
./dist/MiniTCM/MiniTCM        # Linux
# or 
./dist/MiniTCM/MiniTCM.app    # MacOS
```
**Tip**: You can create shortcut to executable on ~/Desktop.
