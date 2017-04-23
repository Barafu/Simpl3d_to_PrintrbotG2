#!/usr/bin/python3
import sys
from os import listdir
from os.path import isfile, join

def main():
    with open(sys.argv[1], 'r') as input_file:
        lines = input_file.readlines()

    result=[]

    for line in lines:
        #Chilipeppr has problems with too many comments, and Simplify3D
        #generates many. Remove them.
        if line.startswith(';'):
            if line.startswith(";SIMPL_START"):
                result.extend(collect_snippets("start"))
            if line.startswith(";SIMPL_END"):
                result.extend(collect_snippets("fin"))
            continue
        #S3D generates a strange and useless command to move nozzle to
        #0 corner after the homing. Remove it.
        if line.startswith('G1 X0.000 Y0.000 Z'):
            continue
        if line.startswith('T0'):
            continue

        bits=line.rstrip('\n').split()

        if bits[0]==("M104"): #Nozzle temp
            temp = int(bits[1].lstrip('S'))
            result.append("M100 ({{\"he1st\":{}}})\n".format(temp))
            continue
        if bits[0]==("M109"): #Nozzle temp with wait
            temp = int(bits[1].lstrip('S'))
            result.append("M100 ({{\"he1st\":{}}})\n".format(temp))
            result.append("M101 ({\"he1at\":true})\n")
            continue
        if bits[0]==("M140"): #Bed temp
            temp = int(bits[1].lstrip('S'))
            result.append("M100 ({{\"he3st\":{}}})\n".format(temp))
            continue
        if bits[0]==("M190"): #Bed temp with wait
            temp = int(bits[1].lstrip('S'))
            result.append("M100 ({{\"he3st\":{}}})\n".format(temp))
            result.append("M101 ({\"he3at\":true})\n")
            continue

        #Few MXXX commands are supported, and those have different
        #dialects. Clean them.
        if line.startswith('M'):
            continue

        #Detect a free movement by lack of extruder action AND a magic
        #speed. Replace G1 with G0 without speed
        if bits[0]=="G1" and bits[4]=="F46620":
            bits[0]="G0"
            del(bits[4])

        #Rename E axis to A axis everywhere.
        for i,b in enumerate(bits):
            if b.startswith('E'):
                bits[i]="A{}".format(b.lstrip('E'))

        line=" ".join(bits)
        result.append("{}\n".format(line))

    with open(sys.argv[2], 'w') as out_file:
        for line in result:
            out_file.write(line)

def collect_snippets(foldername):
    """
    Read snippets of code from folders, collect them into a list
    """
    snippets=[]
    files = [f for f in listdir(foldername)
            if isfile(join(foldername, f))]
    print(files)
    for filename in sorted(files):
        if filename.startswith('-'):
            continue
        with open(join(foldername, filename), 'r') as f:
            code = [t for t in f.readlines()
                    if not t.startswith(';') and not t=="\n"]
            print (code)
            snippets.extend(code)
    return snippets

main()
