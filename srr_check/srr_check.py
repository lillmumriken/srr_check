#!/usr/bin/env python3
import os
import sys
import argparse
from .colorprint import ColorPrint as cprint
from .srrdb import search, download
from .fs import list_rel, crc_check, size_check

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def main():
    parser = argparse.ArgumentParser(description="Compare a release against srrDB")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--crc-check", action="store_true", help="Compare crc checksums")
    parser.add_argument("-f", "--fix", action="store_true", help="Try to download mismatched nfo,sfv,jpg from srrDB")
    parser.add_argument("path", type=dir_path, help="path to release", nargs=1)
    args = parser.parse_args()

    os.chdir(args.path[0])
    relname = os.getcwd().split("/")[-1]

    cprint.print_info(f"Searching srrDB for \"{relname}\"...")
    srr_res = search(relname)
    if srr_res:
        cprint.print_pass("Found release in srrDB")
    else:
        cprint.print_fail("Could not find release in srrDB")
        exit(1)

    # List local files
    fs_res = list_rel(".")

    # Compare and check for missing files
    cprint.print_info("Comparing list of files")
    match_errors = []
    idx = 0
    while idx < len(srr_res["files"]):
        i = srr_res["files"][idx]
        if not any(j["name"] == i["name"] for j in fs_res["files"]):
            cprint.print_fail(f'You are missing {i["name"]}')
            # Download
            if args.fix is True and download(relname, i["name"]) is True:
                cprint.print_pass("Successfully downloaded file, testing again")
                # Refresh file listing
                fs_res = list_rel(".")
                continue
            else:
                match_errors.append(i["name"])
        idx += 1

    if len(match_errors) == 0:
        cprint.print_pass("All files exists")

    # Compare and check for extra local files
    for i in fs_res["files"]:
        if not any(j["name"] == i["name"] for j in srr_res["files"]):
            cprint.print_warn(f'{i["name"]} does not exist in srrDB')


    # Compare size
    size_errors = []
    idx = 0
    while idx < len(srr_res["files"]):
        i = srr_res["files"][idx]
        if any(j["name"] == i["name"] for j in fs_res["files"]):
            s = size_check(i["name"])
            if s != i["size"]:
                msg = f'{i["name"]} with size {i["size"]} does not match your size of {s}'
                # Download
                cprint.print_fail(msg)
                if args.fix is True and download(relname, i["name"]) is True:
                    cprint.print_pass("Successfully downloaded file, testing again")
                    continue
                else:
                    size_errors.append(i["name"])
        idx += 1

    if len(size_errors) == 0:
        cprint.print_pass("All size checks passed")


    # Compare CRC 
    if args.crc_check:
        cprint.print_info("Comparing CRC checksums")
        crc_errors = []
        idx = 0
        while idx < len(srr_res["files"]):
            i = srr_res["files"][idx]
            if any(j["name"] == i["name"] for j in fs_res["files"]):
                c = crc_check(i["name"])
                msg = f'{i["name"]} {i["crc"]} {c}'
                if c == i["crc"]:
                    cprint.print_pass(".", end="")
                    sys.stdout.flush()
                else:
                    sys.stdout.flush()
                    msg = f'{i["name"]} with crc {i["crc"]} does not match your crc of {s}'
                    print("\n")
                    cprint.print_fail(msg)
                    # Download
                    if args.fix is True and download(relname, i["name"]) is True:
                        cprint.print_pass("Successfully downloaded file, testing again")
                        continue
                    else:
                        crc_errors.append(i["name"])
            idx += 1

        if len(crc_errors) == 0:
            print("\n")
            cprint.print_pass("All CRC checks passed")

if __name__ == "__main__":
    main()
