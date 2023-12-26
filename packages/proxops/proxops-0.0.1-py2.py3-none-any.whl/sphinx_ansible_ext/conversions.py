"""
TODO
"""
import os

import yaml2rst
from boltons import fileutils


def yaml2rst_role_defaults(search_path, dst_path, filename="main.yml", *, force=False):
    """
    TODO
    """
    for file in fileutils.iter_find_files(search_path, "main.yml"):
        dirname = os.path.dirname(file).split("/")[-1:][0]
        if dirname != "defaults":
            continue
        dirname = os.path.join(dst_path, os.path.dirname(file).split("/")[-2:-1][0])
        fileutils.mkdir_p(dirname)

        # Only rebuild files that have changed, thus
        # taking advantage of the Sphinx cache to avoid unnecessary rebuilds
        dstfile = os.path.join(dirname, os.path.basename(file))
        dstfile = dstfile[: -len(filename)] + "index.rst"
        if os.path.exists(dstfile):
            src_stat = os.stat(file)
            dst_stat = os.stat(dstfile)
            if force:
                pass
            elif dst_stat.st_mtime_ns >= src_stat.st_mtime_ns:
                continue

        yaml2rst.convert_file(
            file,
            dstfile,
            # strip [[[, ]]], and dnl
            strip_regex=r"(\s?dnl.*|\s:?\[{3}|\s\]{3})\d?\s*$",
            # strip remaining dnl
            yaml_strip_regex=r"^.*(#|\s)dnl.*$",
        )

        # Strip empty literal blocks
        with open(dstfile) as file:
            lines = file.readlines()
            lines += ["", ""]

        output = []
        line0 = ""
        line1 = ""
        for line in lines:
            line2 = line
            if line2 == line1 and line1 == "\n":
                continue

            # Kill the line that doesn't contain a literal block
            if line0 == "::\n" and line1 == "\n" and not line2.startswith("  "):
                line0 = ""

            # Pop line and continue
            output += [line0]
            line0 = line1
            line1 = line2

        # Keep no trailing newline
        while output[len(output) - 1] == "\n":
            output.pop()

        with open(dstfile, "w") as file:
            file.writelines(output)
