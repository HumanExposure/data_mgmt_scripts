lkoval
10/21/19

Uses tabula-py 1.1.1 and pandas 0.24.1 in Python 3.7.3 to extract the refrigerant number, cas number, melting point, boiling point, density, and vapor pressure from library_refrigerant_ref_table.pdf. Note that on the pdf, melting point and boiling point were in the same cell and vapor pressure and denisty were in the same cell. While parsing these fields so they could be split into separate columns, various formats arose that needed to be accounted for. This incuded varying punctuation and different temperatures for the vapor pressure and density. Regular expressions were written to account for the most common cases, but less common cases were dealt with separately. An empty string was left for cells where values were non-existent.
