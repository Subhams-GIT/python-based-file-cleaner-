#!/usr/bin/env python3
import argparse
import pathlib
import os
from . import customtype
from .colors import Colors
from time import time

parser=argparse.ArgumentParser(prog="file cleaner")
parser.add_argument('--foldername',type=pathlib.Path,default=os.curdir)
parser.add_argument('--mimetype',type=customtype.mimeType,default=None)
parser.add_argument('--depth',type=int,default=None)
parser.add_argument('--lgt',type=int,default=None)
parser.add_argument('--smt',type=int,default=None)
parser.add_argument('--ot',type=int,default=None)
parser.add_argument('--drymode',type=bool,default=False)

mime_types = {
        "image":[".jpg",".jpeg",".png"],
        "doc":[".txt",".docx"],
        "python":[".py",".ipynb"],
        None:[None]
}

def findFiles(mimetype,path,depth)->list[pathlib.Path]:
    ignored=set()

    try:
        with open(".gitignore") as f:
            ignored=f.read().split("\n")
            # print(ignored)
    except:
        pass
        
    allowedexts=mime_types.get(mimetype)
    

    if not allowedexts:
        print("wrong mimetype")
        return 
    
    global matched
    match depth:
        case 1:
            matched=scan1(path,ignored,allowedexts)
            
        case 2:
            matched=scan2(path,ignored,allowedexts)
        
        case _:
            print("not found")
    
    # print(matched)
    return matched
    
def scan1(path,ignored,exts)->list[pathlib.Path]:
    matched_files=[]
    for root,dir,files in os.walk(path):
        for d in dir:
            t=pathlib.Path(d)
            if t.is_dir() and next(os.scandir(t), None) is None:
                matched_files.append(t)

        for f in files:
            _,ext=os.path.splitext(f)
            
            if not None in exts:
                if ext in ignored or not ext in exts:
                    continue
            matched_files.append(pathlib.Path(os.path.join(root,f)))
        break
    return matched_files

def scan2(
    path: pathlib.Path | str,
    ignored: set[str],
    exts: list[str | None]
) -> list[pathlib.Path]:

    base = pathlib.Path(path)
    matched: list[pathlib.Path] = []

    for level1 in base.iterdir():
        if level1.name in ignored:
            continue

        
        if level1.is_file():
            if None in exts or level1.suffix in exts:
                matched.append(level1)
        
        elif level1.is_dir():
            for level2 in level1.iterdir():
                if level2.name in ignored:
                    continue

                if level2.is_file():
                    if None in exts or level2.suffix in exts:
                        matched.append(level2)

    return matched

def filter(files:list[pathlib.Path],args):
    final=[]
    totalspace=0
    if args.drymode==True:
        for file in files:
            print(f"{Colors.RED}[DRY-RUN]{Colors.ENDC} Would delete:{file}")
            totalspace+=os.path.getsize(file)
        print(f"{Colors.GREEN} TOTAL_SPACE TO BE CLEARED: {Colors.ENDC}",totalspace/1024)
        return totalspace;
    
    else:
        for file in files:
            size = os.path.getsize(file)
            age = time() - os.path.getatime(file)
            if args.lgt is not None and size < args.lgt:
                continue
            if args.smt is not None and size > args.smt:
                continue
            if args.ot is not None and age < args.ot:
                continue

            final.append(file)
    
    return (final,totalspace)
        
def deleteFiles(files:list[pathlib.Path]):
    for f in files:
        f.unlink()


def main():
    args=parser.parse_args()
    path=args.foldername
    if not os.path.exists(path) or not args.mimetype in ["image","docs","videos","python",None] or args.lgt>args.smt:
        print("provide valid details")
        return
    absolutepath=os.path.abspath(path)
    files=findFiles(args.mimetype,absolutepath,args.depth)
    final_set_files,totalspace=filter(files,args)
    if args.drymode==False:
        choice=input(f"would you like to delete {totalspace}Mb \n [Y/N]?")
        if choice.lower()=="y":
            deleteFiles(final_set_files)
        else:
            exit(1)

if (__name__=="__main__"):    
    main()
