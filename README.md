# GDTDupePurger
A one-file script that takes duplicate asset errors from Black Ops 3 Mod Tools' linker output and attempt to resolve them.

This is a 'dumb' script that doesn't check the most recent file, specific dupe you want to keep etc.
It just removes the dupe no questions asked.

v.1.0a only deletes a single duplicate for each asset. If you have multiple - you will need to repeat the steps.
How to use:

Do "Compile" in BO3 MT. If you have duplicates, they will show in the linker output, such as:

J:\Steam\steamapps\common\Call of Duty Black Ops III\/gdtdb/gdtdb.exe /update

gdtDB: updating

errors found while updating database!

ERROR: Duplicate 'beam' asset 'flamethrower_beam_dragon_gauntlet' found in j:\steam\steamapps\common\call of duty black ops iii\source_data\wpn_t7_zmb_dlc3_gauntlet_dragon.gdt:2296
ERROR: Duplicate 'beam' asset 'flamethrower_beam_dragon_gauntlet' found in j:\steam\steamapps\common\call of duty black ops iii\source_data\wpn_t7_zmb_dlc3_gauntlet_dragon_1.gdt:2296
gdtDB: processed (2 GDTs) (584 assets) in 0.222 sec



