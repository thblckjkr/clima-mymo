# clima-mymo

A little tool to translate mysql from WeeWx into mongodb using a defined schema

> Author: Teo Gonzalez Calzada [@thblckjkr]

This tool was made for Python3

## Installation

Copy the `database/config.example.json` to `config/database.json` and update your credentials accordingly.

Install dependencies

```
pip3 install -r requirements.txt
```

## Running

You can pass the stations names as a parameter, or run it without arguments to enable the interactive mode.

Example:
```
python3 import.py Estacion25
```