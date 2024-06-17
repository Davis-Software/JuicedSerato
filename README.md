## JuicedSerato

> Developed by [Davis_Software](https://pages.software-city.org/d) © 2024

This Project aims to enable users of the DJuiced DJ Software to write their configured track cues into the ID3 tags of the track files
with the Serato GEOB format. This will essentially transfer all cues into Serato.

---
### this project is still under development

---
#### used resourced / open-source projects
* https://github.com/Holzhaus/serato-tags
* https://github.com/Holzhaus/serato-tags/blob/main/docs/fileformats.md
* https://github.com/DJUCED/DJUCED_DJ/blob/main/doc/meta-tags.md

---
### Development
* Generate virtual env `python -m venv .venv`
* Activate the venv
* Install packages `pip install -r requirements.txt`
* Install the package in edit mode `pip install -e .`
* Build with `python -m build`