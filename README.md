# Unit Parse (unit_parse)

---
---
![PyPI](https://img.shields.io/pypi/v/well_plate)
![downloads](https://img.shields.io/pypi/dm/well_plate)
![license](https://img.shields.io/github/license/dylanwal/well_plate)

Do you have strings/text that you want to turn into quantities?

Are you trying to clean scientific data you extracted from [Wikipida](https://en.wikipedia.org/wiki/Main_Page) or some 
other sketchy website?

Try 'Unit_Parse' to clean everything up for you!

#### Description: 

'Unit_Parse' is built on top of [Pint](https://github.com/hgrecco/pint). It was specifically designed to handle data 
that was extracted from scientific work. It has been rigorously tested against chemistry data 
extracted from Wikipida (example: [styrene](https://en.wikipedia.org/wiki/Styrene); density, melting point, boiling 
point, etc.) and data from [PubChem](https://pubchem.ncbi.nlm.nih.gov/) 
(example: [styrene](https://pubchem.ncbi.nlm.nih.gov/compound/Styrene) ; density, melting point, flash point, etc.).


---

## Installation

```
pip install unit_parse
```

## Dependencies

[Pint](https://github.com/hgrecco/pint) - Provides unit conversions of cleaned and parsed quantities.

---
---

## Usage