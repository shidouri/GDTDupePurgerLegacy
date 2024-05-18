from pathlib import Path
import requests
import datetime
import json
from time import sleep
import shutil
import sys
import traceback # For catch-all error handling - pv


global dupe_fixer_flags
global already_backed_up

class asset_as_object:
    def __init__(self, assetname, gdt, path):
        self.assetname = assetname
        self.gdt = gdt
        self.path = path

class dupe_flags:
    def __init__(self, should_print, preserve_stock, should_bak, is_debug):
        self.should_print = should_print
        self.preserve_stock = preserve_stock
        self.should_bak = should_bak
        self.is_debug = is_debug


def get_stock_gdts():
    try:
        with open("./stock.gdtdef", 'r') as stock_gdts:
            stock_defs = stock_gdts.readlines()
            return stock_defs
    except FileNotFoundError:
        git_req = "https://raw.githubusercontent.com/shidouri/GDTDupePurger/main/stock.gdtdef"
        response = requests.get(git_req)
  
        if response.status_code == requests.codes.ok:
            with open('./stock.gdtdef', 'w') as stock_gdt:
                stock_gdt.write(response.text.replace('\n', ''))
            return response.text.split('\n')
        else:
            raise Exception(f"Error: Could not retrieve stock.gdtdef (status code {response.status_code})")



def remove_dupe_from_gdt(asset, gdt_name, gdt_path):
    
    if dupe_fixer_flags.should_bak and gdt_name not in already_backed_up: 
        backup_old_gdt(gdt_name, gdt_path)
        already_backed_up.append(gdt_name)
    
    with open(gdt_path, 'r') as old_gdt:
        old_lines = old_gdt.readlines()
    
    purge_asset_from_gdt_lines(asset, old_lines, gdt_path)
    
 
 
def backup_old_gdt(name, gdt):
    timestamp = datetime.datetime.now().isoformat().replace(':', '_')
    backup_path = Path('./backup')
    backup_path.mkdir(exist_ok=True)

    backup_file = backup_path / f"{timestamp}_{name}"
    shutil.copy2(gdt, backup_file)



def purge_asset_from_gdt_lines(asset, lines, out_path):
    return_lines = []
    purging_lines = False

    for i, line in enumerate(lines):
        if line == "\t{\n" and asset in lines[i-1] and not purging_lines:
            purging_lines = True
            if return_lines:
                return_lines.pop()

        elif line == "\t}\n" and purging_lines:
            purging_lines = False

        elif purging_lines:
            continue

        else:
            return_lines.append(line)
    if dupe_fixer_flags.should_print: print(f"Purging {asset} from {out_path}...")
    Path(out_path).write_text(''.join(return_lines))

    # cleanup error lines file
    open('./dupe_error.txt', 'w').close()
    
    


def split_error_line_to_object(error_log):
    
    object_list = []
    stock_gdt_names = stock_gdts
    
    with open(error_log) as f:
        lines = f.readlines()
        
    for line in lines:
        """
        TL;DR:
        If you use 'and' comparisons here, if one of these three ('ERROR: Duplicate', 'found in ', 'gdt:') are present in the line, but the other isn't, like 
        in the example provided below, you'll get an error when parsing the line, and the program will crash.
        
        Changed 'and' to 'or' comparisons because sometimes the launcher starts a new line for some reason, resulting in a line that's split up like so:
        
        > ERROR: Duplicate 'aifxtable' asset 'c_zmb_apothicon_fury_fx_table' foun
        > d in m:\black ops iii\steamapps\common\call of duty black ops iii\source_data\c_zom_dlc4_apothicon_fury.gdt:3864

        This will cause an error because this line will start to get processed because the program saw 'ERROR: Duplicate' but not 'found in ' or 'gdt:' and 
        so this line and the next should be skipped from parsing
        
        \- pv
         """
        #if 'ERROR: Duplicate' not in line or 'found in ' not in line or 'gdt:' not in line:
        if any( kwd not in line for kwd in ( 'ERROR: Duplicate', 'found in ', 'gdt:' ) ) # Iteration ftw g
            continue
            
        asset = line.split("asset")[1].split(" found in")[0].replace("'", "").replace(" ", "")
        location = (line.split('found in ')[1]).split('.gdt:')[0] + '.gdt'
        splitup = line.split('\\')[-1].split(':')[0]
    
        asset_object = asset_as_object(asset, splitup, location)
        
        if is_stock_gdt(splitup, stock_gdt_names) and dupe_fixer_flags.preserve_stock:
            if dupe_fixer_flags.should_print: print(f"Ignoring stock asset {asset} in {location} ({splitup})")
            continue
        else: object_list.append(asset_object)
    
    json_list = [json.dumps(obj.__dict__) for obj in object_list]

    # convert list of objects to list of dicts
    jsons = [json.loads(j) for j in json_list]

    # remove duplicates based on assetname
    uniques = {x['assetname']: x for x in jsons}.values()
    
    for obj in uniques:
        remove_dupe_from_gdt(obj['assetname'], obj['gdt'], obj['path'])
    print("Done.")
    


def is_stock_gdt(name, stock_gdt_names):
    if any(name in s for s in stock_gdt_names): return True
    else: return False



def __main__():
    
    dupe_error_path = Path('./dupe_error.txt').resolve()

    try:
        with open(dupe_error_path, 'r') as f:
            lines = f.readlines()

            if lines:
                split_error_line_to_object(dupe_error_path)
            else:
                print(f"No lines found in {dupe_error_path}!  [Did you forget to save?] ")

    except FileNotFoundError:
        dupe_error_path.touch()
        print(f"{dupe_error_path} wasn't found.\nIt has now been created for you.")
        print(f"Place your linker error lines in {dupe_error_path}, save, and run this tool again.")


    input("Press [RETURN] to exit ;")



def sort_main_args():
    sorted_args = dupe_flags(True, True, True, False)
    if len(sys.argv) < 2: return sorted_args
    
    for arg in sys.argv:
        arg = arg.replace('+', '').replace('-', '').replace('/', '')
        if arg in {'no_preserve_stock', 'no_stock', 'ignorestock', 'nps' }:
            sorted_args.preserve_stock = False
        elif arg in {'no_print', 'no_log', 'noshow', 'quiet', 'shh'}:
            sorted_args.should_print = False
        elif arg in {'developer_no_backup_use_wisely', 'nobak'}:
            sorted_args.should_bak = False
        elif arg in {'debug', 'dev1', 'show_flags'}:
            sorted_args.is_debug = True
   
    return sorted_args


if __name__ == "__main__":
    already_backed_up = []
    dupe_fixer_flags = sort_main_args()
    if dupe_fixer_flags.is_debug:
        print(f"PRESERVE STOCK GDTS: {dupe_fixer_flags.preserve_stock}")
        print(f"PRINT: {dupe_fixer_flags.should_print}")
        print(f"BACKUP GDTS: {dupe_fixer_flags.should_bak}")	
    
    stock_gdts = get_stock_gdts()
    
    # Adding a catch-all error output here so people can send us a log file with the error they get (with a traceback) when the program crashes
    try: __main__()
    except Exception as _e:

        with open( "gdt_dupe_purger_error.log", 'w' ) as log:
            log.write( traceback.format_exc() )
        
        print(
            '\033[91m',
            "UNHANDLED EXCEPTION: An error has occured.",
            '\033[1m' + _e + '\033[0m',
            "There's a traceback in your log file",
			"\nPlease dm your LOG FILE & your DUPE ERROR FILE to either Shidouri or prov3ntus on discord so we can help you fix the error, and ensure others don't run into the same issue",
			f'Your log file can be located here: {os.path.join( os.getcwd(), "gdt_dupe_purger_error.log" )}',
            f'Your dupe_error file can be located here: {os.path.join( os.getcwd(), "dupe_error.txt" )}',
            "\nAlternatively, you can open an issue on GitHub",
            sep = '\n', end = '\033[0m' + '\n
        )

        input( "Press [RETURN] to exit ;" )
    
