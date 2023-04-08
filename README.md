# GDTDupePurger
A one-file script that takes duplicate asset errors from Black Ops 3 Mod Tools' linker output and attempt to resolve them.

This is a 'dumb' script that doesn't check the most recent file, specific dupe you want to keep etc.
It just removes the first dupe it finds, no questions asked.


How to use:

Do "Compile" in BO3 MT. If you have duplicates, they will show in the linker output, such as:

    J:\Steam\steamapps\common\Call of Duty Black Ops III\/gdtdb/gdtdb.exe /update

    gdtDB: updating

    errors found while updating database!

    ERROR: Duplicate 'beam' asset 'flamethrower_beam_dragon_gauntlet' found in j:\steam\steamapps\common\call of duty black ops iii\source_data       \wpn_t7_zmb_dlc3_gauntlet_dragon.gdt:2296
    ERROR: Duplicate 'beam' asset 'flamethrower_beam_dragon_gauntlet' found in j:\steam\steamapps\common\call of duty black ops iii\source_data\wpn_t7_zmb_dlc3_gauntlet_dragon_1.gdt:2296
    gdtDB: processed (2 GDTs) (584 assets) in 0.222 sec


Copy that entire output (all of the text). Open **dupe_error.txt** in a text editor such as notepad, paste the text, then save it and close.

Run ***dupe_fixer.exe***. The console window will show you any issues, or its progress through the GDT purging.

Try compiling in Mod Tools again. Your duplicates should be fixed!

**NOTE**

v.1.0a only deletes a single duplicate for each asset.
If you have multiple duplicates of one asset, you will need to try compiling in MT after running **dupe_fixer.exe** to get the updated error list, and repeat as many times as necessary.
This will be fixed on full release.


**NOTE**

Backups of GDTs will be placed in ***<dupe_fixer_folder>/backup***.
Backups are in the following format: ***YYYY-MM-DD_HH_MM_SS__{gdtname}.gdt*** (UTC Time)
As this is an alpha, **ANY** time a GDT is overwritten to a backup is made - which can lead to a lot of backups. Feel free to delete old backups when necessary, such as when confirmed you do not want to revert.

This will be fixed on full release.


