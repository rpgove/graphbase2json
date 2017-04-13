# Graphbase2json

A Python 2.7 script that converts [Stanford GraphBase](http://www-cs-faculty.stanford.edu/~uno/sgb.html) .dat files to JSON suitable for loading in [D3.js](https://d3js.org). This has only been tested with the jean.dat file.

Other parsed versions of the jean.dat dataset are common in the D3.js community, but they are missing isolate characters. This parser also creates a list of chapters where the character occured, and a list of chapters for each link between characters.

Example usage:

    $ python graphbase2json.py --input jean.dat --output jean.json