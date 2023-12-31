"""  Utility to fix basic notebook validation errors """

import sys
import json
import click

from pathlib import Path


def collect_files(paths, *, recurse=False):
    """ collect file paths with optional recursion """

    files = []

    for path in paths:
        path = Path(path)
        if path.is_dir():
            if recurse:
                files.extend(path.rglob("*.ipynb"))
            else:
                files.extend(path.glob("*.ipynb"))
        elif path.exists():
            files.append(path)
        else:
            raise FileNotFoundError(path)

    return files


def fix_notebook(file, outdir=None, *, check_only=False):
    """ fix notebook """
    file = Path(file)

    try:
        changes = 0
        data = json.loads(file.read_text())
        cells = data['cells']

        for cell in cells:
            ct = cell.get('cell_type')
            if ct == "code" and 'execution_count' not in cell:
                cell['execution_count'] = None
                changes += 1

    except Exception as ex:
        print(file, "error")
        return

    if not changes:
        print(file, "ok")
        return

    if check_only:
        print(file, "tofix")
        return

    if outdir:
        outfile = Path(outdir).joinpath(file.name)
    else:
        outfile = file

    output = json.dumps(data)
    outfile.write_text(output)
    print(file, "fixed")


@click.command
@click.argument("path", nargs=-1)
@click.option("-o", "--outdir", metavar='OUTDIR', default=None, help="Save output in directory.")
@click.option("-c", "--check-only", is_flag=True, help="Only check for errors.")
@click.option("-r", "--recurse", is_flag=True, help="Recurse to sub directories.")
def main(path=(), outdir=None, check_only=False, recurse=False):
    """
    Utility to fix basic notebook validation errors

    PATH is the path to a notebook file or a directory containing *.ipynb files.

    By default the script will change the files in place when there is a fix,
    but you can specify an OUTDIR parameter if you prefer to save output files
    in a different directory.
    """

    if outdir:
        outdir = Path(outdir)

    try:
        files = collect_files(path, recurse=recurse)

        for file in files:
            fix_notebook(file, outdir=outdir, check_only=check_only)

    except FileNotFoundError as ex:
        print(ex, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
