from os.path import exists, abspath
from os import mkdir
import datetime
import json
from time import sleep


class asset_as_object:
    def __init__(self, assetname, gdt, path):
        self.assetname = assetname
        self.gdt = gdt
        self.path = path
        
    
def split_error_line_to_object(error_log):
    
    object_list = []
    gdt_assets_to_fix = {}
    json_list = []
    
    with open(error_log, 'r') as raw_lines:
        
        lines = raw_lines.readlines()
        
        for line in lines:
            
            if ('ERROR: Duplicate' or 'found in ' or 'gdt:') not in line:
                continue
            
            asset = ( ( line.split("asset")[1] ).split(" found in" )[0] ).replace("'", "").replace(" ", "")
            
            location = (line.split('found in ')[1]).split('.gdt:')[0] + '.gdt'
            
            splitup = (line.split('\\')[(len(line.split('\\'))-1)]).split(':')[0]
            
            asset_object = asset_as_object(asset, splitup, location)
            
            object_list.append(asset_object)
    
    for object in object_list:
        json_list.append(json.dumps(object.__dict__))
    
       # load json objects to dictionaries
    jsons = map(json.loads, json_list)
    uniques = {x['assetname']: x for x in jsons}
    objects_to_delete = list(uniques.values())
    for obj in objects_to_delete:
        remove_dupe_from_gdt(obj['assetname'], obj['gdt'], obj['path'])
        sleep(1)
    print("Done.")



def backup_old_gdt(name, gdt):
    now = datetime.datetime.utcnow()
    backup_string = (now.strftime(f"%Y-%m-%d_%H_%M_%S__{name}"))
    with open(gdt, 'r') as old_gdt_lines:
        bak_lines = old_gdt_lines.readlines()
        
    if not exists('./backup'):
        mkdir('./backup')
        
    with open(f'./backup/{backup_string}', 'x') as bak_gdt:
        for line in bak_lines:
            bak_gdt.writelines(line)



def purge_asset_from_gdt_lines(asset, lines, out_path):
    
    return_lines = []
    purging_lines = False
    
    for i, line in enumerate(lines):
        if line == "\t{\n" and asset in lines[i-1] and not purging_lines:
            purging_lines = True
            if(len(return_lines) > 1):
                return_lines.pop(len(return_lines)-1)
            
        elif line == "\t}\n" and purging_lines:
            purging_lines = False
        
        elif purging_lines:
            continue
        
        else:
            return_lines.append(line)
    
    print(f"Purging {asset} from {out_path}...")
    with open(out_path, 'w+') as new_gdt:
        new_gdt.writelines(return_lines)
        
    # cleanup error lines file:
    
    with open('./dupe_error.txt', 'w') as error_txt:
        error_txt.writelines("")
        
    
        


    
def remove_dupe_from_gdt(asset, gdt_name, gdt_path):
    backup_old_gdt(gdt_name, gdt_path)
    
    with open(gdt_path, 'r') as old_gdt:
        old_lines = old_gdt.readlines()
    
    out_file_lines = purge_asset_from_gdt_lines(asset, old_lines, gdt_path)
    
    


def __main__():
    abs_path = abspath("./dupe_error.txt")
    
    try:
        with open('./dupe_error.txt', 'r') as dupe_error_file:
            
            lines = dupe_error_file.readlines()
            
            if len(lines) != 0: split_error_line_to_object('./dupe_error.txt')
            
            else: print(f"No lines found in {abs_path}!  [Did you forget to save?] ")
            
            
            
    except:
        
        with open('./dupe_error.txt', 'x') as dupe_error_file:
            print(f"{abs_path} wasn't found.\nIt has now been created for you.")
            print(f"Place your linker error lines in {abs_path}, save, and run this tool again.")



    print("Press [RETURN] to exit ;)")
    input()
    


__main__()



        
        
        