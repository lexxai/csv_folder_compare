import pyinstaller_versionfile
from configparser import ConfigParser
import sys
from pathlib import Path


parser = ConfigParser()
# read config file
description = ""
ver = "0.0.1"
config_setup_toml = None

if len(sys.argv) > 1:
    for ar in sys.argv:
        filename = Path(ar)
        if filename.is_file():
            if filename.suffix == ".toml":
                config_setup_toml = filename
                break


config_setup = Path("..\setup.cfg")
if config_setup.is_file():
    parser.read(config_setup)
    ver = parser["metadata"].get("version", "0.0.1")
    description = parser["metadata"].get("description", "").strip('"')
    name = parser["metadata"].get("name", "").strip('"')
else:
    config_setup = config_setup_toml if config_setup_toml else Path("..\pyproject.toml")
    if config_setup.is_file():
        parser.read(config_setup)
        ver = parser["tool.poetry"].get("version", "0.0.1").strip('"')
        description = parser["tool.poetry"].get("description", "").strip('"')
        name = parser["tool.poetry"].get("name", "").strip('"')

if len(sys.argv) > 1:
    for ar in sys.argv:
        filename = Path(ar)
        if filename.is_file():
            if filename.suffix == ".exe":
                new_fn = filename.with_stem(f"{filename.stem}_{ver}")
                print(f"RENAME TO: {new_fn}")
                filename.rename(new_fn)
                break
else:
    pyinstaller_versionfile.create_versionfile(
        output_file="..\\versionfile.txt",
        version=f"{ver}.0",
        company_name="lexxai",
        file_description=description,
        internal_name=name,
        legal_copyright="https://github.com/lexxai",
        original_filename=f"{name}_{ver}.exe",
        product_name=name,
    )
    print(f"Done: versionfile.txt in parent folder. version='{ver}.0'")
