import numpy as np


class CIg:
    def __init__(self):
        self.name = 'Green Chlorophyll Index'
        self.formula = '(NIR / GREEN) - 1'
        self.reference = 'Gitelson et al., 2005'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir / green) - 1


class CIre:
    def __init__(self):
        self.name = 'Red Edge Chlorophyll Index'
        self.formula = '(NIR / RED_EDGE) - 1'
        self.reference = 'Gitelson et al., 2003'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (nir / red_edge) - 1


class CIVE:
    def __init__(self):
        self.name = 'Color Index for Vegetation Extraction'
        self.formula = '0.441*[RED] - 0.811*[GREEN] + 0.385*[BLUE] + 18.787'
        self.reference = 'Beniaich et al., 2019'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> np.ndarray:
        return 0.441 * red - 0.811 * green + 0.385 * blue + 18.787


class DATT:
    def __init__(self):
        self.name = 'DATT Index'
        self.formula = '([NIR] - [RED EDGE]) / ([NIR] - [RED])'
        self.reference = 'Datt, 1999'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / (nir - red)


class DVI:
    def __init__(self):
        self.name = 'Difference Vegetation Index'
        self.formula = '[NIR] - [RED]'
        self.reference = 'Roncagliolo et al., 2012'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return nir - red


class ExB:
    def __init__(self):
        self.name = 'Excess Blue Index'
        self.formula = '1.4*[BLUE] - [GREEN]'
        self.reference = 'Guo et al., 2020'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, blue: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 1.4 * blue - green


class ExR:
    def __init__(self):
        self.name = 'Excess Red Index'
        self.formula = '1.4*[RED] - [GREEN]'
        self.reference = 'Guo et al., 2020'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 1.4 * red - green


class GDVI:
    def __init__(self):
        self.name = 'Green Difference Vegetation Index'
        self.formula = '[NIR] - [GREEN]'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return nir - green


class GI:
    def __init__(self):
        self.name = 'Greenness Index'
        self.formula = '[GREEN] / [RED]'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, red: np.ndarray) -> np.ndarray:
        return green / red


class GNDVI:
    def __init__(self):
        self.name = 'Green Normalized Difference Vegetation Index'
        self.formula = '([NIR] - [GREEN]) / ([NIR] + [GREEN])'
        self.reference = 'Gitelson et al., 1996a'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - green) / (nir + green)


class GOSAVI:
    def __init__(self):
        self.name = 'Green Optimized SAVI'
        self.formula = '(1 + 0.16) * ([NIR] - [GREEN]) / ([NIR] + [GREEN] + 0.16)'
        self.reference = 'Rondeaux et al., 1996'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (1 + 0.16) * (nir - green) / (nir + green + 0.16)


class GRD:
    def __init__(self):
        self.name = 'Green and Red Difference'
        self.formula = '[GREEN] - [RED]'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, red: np.ndarray) -> np.ndarray:
        return green - red


class GRDVI:
    def __init__(self):
        self.name = 'Green Re-normalized Difference Vegetation Index'
        self.formula = '([NIR] - [GREEN]) / Sqr([NIR] + [GREEN])'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - green) / np.sqrt(nir + green)


class GRVI:
    def __init__(self):
        self.name = 'Green Ratio Vegetation Index'
        self.formula = '[NIR] / [GREEN]'
        self.reference = 'Buschmann and Nagel, 1993'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return nir / green


class GSAVI:
    def __init__(self):
        self.name = 'Green Soil Adjusted Vegetation Index'
        self.formula = '1.5 * ([NIR] - [GREEN]) / ([NIR] + [GREEN] + 0.5)'
        self.reference = 'Sripada et al., 2006'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 1.5 * (nir - green) / (nir + green + 0.5)


class GWDRVI:
    def __init__(self):
        self.name = 'Green Wide Dynamic Range Vegetation Index'
        self.formula = '(0.12*[NIR]-[GREEN]) / (0.12*[NIR]+[GREEN])'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (0.12 * nir - green) / (0.12 * nir + green)


class IKAW:
    def __init__(self):
        self.name = 'Kawashima Index'
        self.formula = '([RED] - [BLUE]) / ([RED] + [BLUE])'
        self.reference = 'Gitelson et al., 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, blue: np.ndarray) -> np.ndarray:
        return (red - blue) / (red + blue)


class MCARI:
    def __init__(self):
        self.name = 'Modified Chlorophyll Absorption in Reflectance Index'
        self.formula = '(([RED EDGE]-[RED])-0.2*([RED EDGE]-[RED])) * ([RED EDGE]/[RED])'
        self.reference = 'Modified by Li and Chen, 2011'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return ((red_edge - red) - 0.2 * (red_edge - red)) * (red_edge / red)


class MCARI1:
    def __init__(self):
        self.name = 'Modified Chlorophyll Absorption in Reflectance Index 1'
        self.formula = '1.2 * (2.5*([NIR]-[RED])-1.3*([NIR]-[GREEN]))'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 1.2 * (2.5 * (nir - red) - 1.3 * (nir - green))


class MCARI1_MRETVI:
    def __init__(self):
        self.name = 'MCARI1/MRETVI'
        self.formula = '[MCARI1] / [MRETVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, mcari1: np.ndarray, mretvi: np.ndarray) -> np.ndarray:
        return mcari1 / mretvi


class MCARI1_OSAVI:
    def __init__(self):
        self.name = 'MCARI1/OSAVI'
        self.formula = '[MCARI1] / [OSAVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, mcari1: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return mcari1 / osavi


class MCARI2:
    def __init__(self):
        self.name = 'Modified Chlorophyll Absorption in Reflectance Index 2'
        self.formula = '1.5 * (2.5*([NIR]-[RED])-1.3*([NIR]-[GREEN])) / Sqr(((2*[NIR]+1)*(2*[NIR]+1))-((6*[NIR])-(5*Sqr([RED])))-0.5)'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        denominator = np.sqrt(((2*nir + 1)**2) - ((6*nir) - (5*(red**2))) - 0.5)
        return 1.5 * (2.5 * (nir - red) - 1.3 * (nir - green)) / denominator


class MCARI2_OSAVI:
    def __init__(self):
        self.name = 'MCARI2/OSAVI'
        self.formula = '[MCARI2] / [OSAVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, mcari2: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return mcari2 / osavi


class MCARI3:
    def __init__(self):
        self.name = 'Modified Chlorophyll Absorption in Reflectance Index 3'
        self.formula = '(([NIR]-[RED EDGE])-0.2*([NIR]-[RED])) / ([NIR]/[RED EDGE])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return ((nir - red_edge) - 0.2 * (nir - red)) / (nir / red_edge)


class MCARI4:
    def __init__(self):
        self.name = 'Modified Chlorophyll Absorption in Reflectance Index 4'
        self.formula = '1.5 * (2.5*([NIR]-[GREEN])-1.3*([NIR]-[RED EDGE])) / Sqr(((2*[NIR]+1)*(2*[NIR]+1))-((6*[NIR])-(5*Sqr([GREEN])))-0.5)'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        denominator = np.sqrt(((2*nir + 1)**2) - ((6*nir) - (5*(green**2))) - 0.5)
        return 1.5 * (2.5 * (nir - green) - 1.3 * (nir - red_edge)) / denominator


class MCCCI:
    def __init__(self):
        self.name = 'Modified Canopy Chlorophyll Content Index'
        self.formula = '[NDRE] / [NDVI]'
        self.reference = 'Long et al., 2009'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, ndre: np.ndarray, ndvi: np.ndarray) -> np.ndarray:
        return ndre / ndvi


class MDD:
    def __init__(self):
        self.name = 'Modified Double Difference Index'
        self.formula = '([NIR]-[RED EDGE]) - ([RED EDGE]-[GREEN])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - red_edge) - (red_edge - green)


class MDD_R:
    def __init__(self):
        self.name = 'Modified Double Difference Index (Red Edge)'
        self.formula = '([NIR]-[RED EDGE]) - ([RED EDGE]-[RED])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red_edge) - (red_edge - red)


class MRESAVI:
    def __init__(self):
        self.name = 'Modified Red Edge Soil Adjusted Vegetation Index'
        self.formula = '0.5 * (2*[NIR] + 1 - Sqr(((2*[NIR] + 1)*(2*[NIR] + 1)) - 8*([NIR] - [RED EDGE])))'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 0.5 * (2*nir + 1 - np.sqrt(((2*nir + 1)*(2*nir + 1)) - 8*(nir - red_edge)))


class MEVI_Cao:
    def __init__(self):
        self.name = 'Modified Enhanced Vegetation Index (Cao et al.)'
        self.formula = '2.5 * ([NIR] - [RED EDGE]) / ([NIR] + 6*[RED EDGE] - 7.5*[GREEN] + 1)'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 2.5 * (nir - red_edge) / (nir + 6*red_edge - 7.5*green + 1)


class MEVI_Lu:
    def __init__(self):
        self.name = 'Modified Enhanced Vegetation Index (Lu et al.)'
        self.formula = '2.5 * ([NIR] - [RED]) / ([NIR] + 6*[RED] - 7.5*[RED EDGE] + 1)'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 2.5 * (nir - red) / (nir + 6*red - 7.5*red_edge + 1)


class MGSAVI:
    def __init__(self):
        self.name = 'Modified Green SAVI'
        self.formula = '0.5 * (2*[NIR] + 1 - Sqr(((2*[NIR] + 1)*(2*[NIR] + 1)) - 8*([NIR] - [GREEN])))'
        self.reference = 'Huang et al., 2015'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 0.5 * (2*nir + 1 - np.sqrt(((2*nir + 1)*(2*nir + 1)) - 8*(nir - green)))


class MNDI:
    def __init__(self):
        self.name = 'Modified Normalized Difference Index'
        self.formula = '([NIR] - [RED EDGE]) / ([NIR] - [GREEN])'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / (nir - green)


class MNDI_R:
    def __init__(self):
        self.name = 'Modified Normalized Difference Index (Red)'
        self.formula = '([NIR] - [RED EDGE]) / ([NIR] + [RED EDGE] - 2*[RED])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / (nir + red_edge - 2*red)


class MNDRE:
    def __init__(self):
        self.name = 'Modified Normalized Difference Red Edge'
        self.formula = '([NIR] - ([RED EDGE] - 2*[GREEN])) / ([NIR] + ([RED EDGE] - 2*[GREEN]))'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - (red_edge - 2*green)) / (nir + (red_edge - 2*green))


class MNDRE2:
    def __init__(self):
        self.name = 'Modified Normalized Difference Red Edge 2'
        self.formula = '([NIR] - [RED EDGE] + 2*[RED]) / ([NIR] + [RED EDGE] - 2*[RED])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red_edge + 2*red) / (nir + red_edge - 2*red)


class mNDVI1:
    def __init__(self):
        self.name = 'Modified Normalized Difference Vegetation Index 1'
        self.formula = '([NIR] - [RED] + 2*[GREEN]) / ([NIR] + [RED] - 2*[GREEN])'
        self.reference = 'Wang et al., 2012'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir - red + 2*green) / (nir + red - 2*green)


class MNLI:
    def __init__(self):
        self.name = 'Modified Nonlinear Index'
        self.formula = '1.5 * (([NIR]*[NIR]) - [RED]) / (([NIR]*[NIR]) + [RED] + 0.5)'
        self.reference = 'Roujean and Breon, 1995'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return 1.5 * ((nir**2) - red) / ((nir**2) + red + 0.5)


class MRBVI:
    def __init__(self):
        self.name = 'Modified Red Blue Vegetation Index'
        self.formula = '((([RED]*[RED]) - ([BLUE]*[BLUE])) / (([RED]*[RED]) + ([BLUE]*[BLUE])))'
        self.reference = 'Guo et al., 2020'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, blue: np.ndarray) -> np.ndarray:
        return ((red**2) - (blue**2)) / ((red**2) + (blue**2))


class MREDVI:
    def __init__(self):
        self.name = 'Modified Red Edge Difference Vegetation Index'
        self.formula = '[RED EDGE] - [RED]'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return red_edge - red


class MRESR:
    def __init__(self):
        self.name = 'Modified Red Edge Simple Ratio'
        self.formula = '([NIR] - [RED]) / ([RED EDGE] - [RED])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (nir - red) / (red_edge - red)


class MRETVI:
    def __init__(self):
        self.name = 'Modified Red Edge Transformed Vegetation Index'
        self.formula = '1.2 * (1.2 * ([NIR] - [RED]) - 2.5 * ([RED EDGE] - [RED]))'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 1.2 * (1.2 * (nir - red) - 2.5 * (red_edge - red))


class MSAVI:
    def __init__(self):
        self.name = 'Modified Soil-adjusted Vegetation Index'
        self.formula = '0.5 * (2*[NIR] + 1 - Sqr(((2*[NIR] + 1)*(2*[NIR] + 1)) - 8*([NIR] - [RED])))'
        self.reference = 'Sripada et al., 2006'
        self.doi = 'http.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return 0.5 * (2*nir + 1 - np.sqrt(((2*nir + 1)*(2*nir + 1)) - 8*(nir - red)))


class MSR:
    def __init__(self):
        self.name = 'Modified Simple Ratio'
        self.formula = '([NIR]/[RED]-1)/Sqr([NIR]/[RED]+1)'
        self.reference = 'Sandham, 1997'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir / red - 1) / np.sqrt(nir / red + 1)


class MSR_G:
    def __init__(self):
        self.name = 'Modified Green Simple Ratio'
        self.formula = '([NIR]/[GREEN]-1)/Sqr([NIR]/[GREEN]+1)'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, green: np.ndarray) -> np.ndarray:
        return (nir / green - 1) / np.sqrt(nir / green + 1)


class MSR_RE:
    def __init__(self):
        self.name = 'Modified Red Edge Simple Ratio'
        self.formula = '([NIR]/[RED EDGE]-1)/Sqr([NIR]/[RED EDGE]+1)'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (nir / red_edge - 1) / np.sqrt(nir / red_edge + 1)


class MSRGR:
    def __init__(self):
        self.name = 'Modified Simple Ratio Green and Red'
        self.formula = 'Sqr([GREEN]/[RED])'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, red: np.ndarray) -> np.ndarray:
        return np.sqrt(green / red)


class MTCARI:
    def __init__(self):
        self.name = 'Modified Transformed Chlorophyll Absorption In Reflectance Index'
        self.formula = '3*(([NIR]-[RED EDGE])-0.2*([NIR]-[RED])*([NIR]/[RED EDGE]))'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return 3 * ((nir - red_edge) - 0.2 * (nir - red) * (nir / red_edge))


class MTCARI_MRETVI:
    def __init__(self):
        self.name = 'MTCARI/MRETVI'
        self.formula = '[MTCARI]/[MRETVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, mtcari: np.ndarray, mretvi: np.ndarray) -> np.ndarray:
        return mtcari / mretvi


class MTCARI_OSAVI:
    def __init__(self):
        self.name = 'MTCARI/OSAVI'
        self.formula = '[MTCARI]/[OSAVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, mtcari: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return mtcari / osavi


class MTCI:
    def __init__(self):
        self.name = 'MERIS Terrestrial Chlorophyll Index'
        self.formula = '([NIR]-[RED EDGE])/([RED EDGE]-[RED])'
        self.reference = 'Dash and Curran, 2004'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / (red_edge - red)


class NDGR:
    def __init__(self):
        self.name = 'Normalized Difference Green and Red'
        self.formula = '([GREEN]-[RED])/([GREEN]+[RED])'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (green - red) / (green + red)


class NDRE:
    def __init__(self):
        self.name = 'Normalized Difference Red Edge'
        self.formula = '([NIR]- [RED EDGE])/([NIR] + [RED EDGE])'
        self.reference = 'Manuscript and Manuscript, n.d.'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / (nir + red_edge)


class NDVI:
    def __init__(self):
        self.name = 'Normalized Difference Vegetation Index'
        self.formula = '([NIR]-[RED])/([NIR] + [RED])'
        self.reference = 'Roujean and Breon, 1995'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red) / (nir + red)


class NDVI_RVI:
    def __init__(self):
        self.name = 'NDVI*RVI'
        self.formula = '(Sqr([NIR])-[RED])/([NIR]+Sqr([RED]))'
        self.reference = 'Roujean and Breon, 1995'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir**2 - red) / (nir + red**2)


class NGBDI:
    def __init__(self):
        self.name = 'Normalized Green-Blue Difference Index'
        self.formula = '([GREEN]-[BLUE])/([GREEN]+[BLUE])'
        self.reference = 'Gitelson et al., 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, blue: np.ndarray) -> np.ndarray:
        return (green - blue) / (green + blue)


class NGI:
    def __init__(self):
        self.name = 'Normalized Green Index'
        self.formula = '[GREEN]/([NIR]+[RED EDGE]+[GREEN])'
        self.reference = 'Sripada et al., 2006'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return green / (nir + red_edge + green)


class NLI:
    def __init__(self):
        self.name = 'Nonlinear Index'
        self.formula = '(([NIR]*[NIR])-[RED])/(([NIR]*[NIR])+[RED])'
        self.reference = 'Goel and Qin, 1994'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return ((nir**2) - red) / ((nir**2) + red)


class NNIR:
    def __init__(self):
        self.name = 'Normalized NIR Index'
        self.formula = '[RED]/([NIR]+[RED EDGE]+[RED])'
        self.reference = 'Sripada et al., 2006'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return red / (nir + red_edge + red)


class NNIRI:
    def __init__(self):
        self.name = 'Normalized Near Infrared Index'
        self.formula = '[TCARI]/[OSAVI]'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, tcari: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return tcari / osavi


class NREI:
    def __init__(self):
        self.name = 'Normalized Red Edge Index'
        self.formula = '[RED EDGE]/([NIR]+[RED EDGE]+[GREEN])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, nir: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return red_edge / (nir + red_edge + green)


class NRI:
    def __init__(self):
        self.name = 'Normalized Red Index'
        self.formula = '[RED]/([NIR]+[RED EDGE]+[RED])'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return red / (nir + red_edge + red)


class OSAVI:
    def __init__(self):
        self.name = 'Optimized Soil-Adjusted Vegetation Index'
        self.formula = '(1+0.16)*([NIR]-[RED])/([NIR]+[RED]+0.16)'
        self.reference = 'Rondeaux et al., 1996'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (1 + 0.16) * (nir - red) / (nir + red + 0.16)


class PSRI:
    def __init__(self):
        self.name = 'Plant Senescence Reflectance Index'
        self.formula = '([RED]-[GREEN])/[NIR]'
        self.reference = 'Sims and Gamon, 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, green: np.ndarray, nir: np.ndarray) -> np.ndarray:
        return (red - green) / nir


class RDVI:
    def __init__(self):
        self.name = 'Renormalized Difference Vegetation Index'
        self.formula = '([NIR]-[RED])/SQRT([NIR] + [RED])'
        self.reference = 'Roujean and Breon, 1995'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (nir - red) / np.sqrt(nir + red)


class REDVI:
    def __init__(self):
        self.name = 'Red Edge Difference Vegetation Index'
        self.formula = '[NIR]-[RED EDGE]'
        self.reference = 'Gitelson et al., 1996b'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return nir - red_edge


class RENDVI:
    def __init__(self):
        self.name = 'Red Edge Normalized Difference Vegetation Index'
        self.formula = '([RED EDGE]-[RED])/([RED EDGE]+[RED])'
        self.reference = 'Elsayed et al., 2015'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (red_edge - red) / (red_edge + red)


class REOSAVI:
    def __init__(self):
        self.name = 'Red Edge Optimal Soil Adjusted Vegetation Index'
        self.formula = '(1 + 0.16)*([NIR]-[RED EDGE])/([NIR] + [RED EDGE] + 0.16)'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (1 + 0.16) * (nir - red_edge) / (nir + red_edge + 0.16)


class REPR:
    def __init__(self):
        self.name = 'Red Edge Point Reflectance'
        self.formula = '([RED]+[NIR])/2'
        self.reference = 'Dash and Curran, 2004'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red: np.ndarray, nir: np.ndarray) -> np.ndarray:
        return (red + nir) / 2


class RERDVI:
    def __init__(self):
        self.name = 'Red Edge Renormalized Difference Vegetation Index'
        self.formula = '([NIR] -[RED EDGE])/SQRT([NIR] + [RED EDGE])'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return (nir - red_edge) / np.sqrt(nir + red_edge)


class RERVI:
    def __init__(self):
        self.name = 'Red Edge Ratio Vegetation Index'
        self.formula = '[NIR]/[RED EDGE]'
        self.reference = 'Gitelson et al., 1996b'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return nir / red_edge


class RESAVI:
    def __init__(self):
        self.name = 'Red Edge Soil Adjusted Vegetation Index'
        self.formula = '1.5*[([NIR] -[RED EDGE])/([NIR] + [RED EDGE] + 0.5)]'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 1.5 * (nir - red_edge) / (nir + red_edge + 0.5)


class RESR:
    def __init__(self):
        self.name = 'Red Edge Simple Ratio'
        self.formula = '[RED EDGE]/[RED]'
        self.reference = 'Erdle et al., 2011'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray) -> np.ndarray:
        return red_edge / red


class RETVI:
    def __init__(self):
        self.name = 'Red Edge Transformed Vegetation Index'
        self.formula = '0.5*(120*([NIR]-[RED])-200*([RED EDGE]-[RED]))'
        self.reference = 'Lu et al., 2017'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 0.5 * (120 * (nir - red) - 200 * (red_edge - red))


class REVIopt:
    def __init__(self):
        self.name = 'Optimized Red Edge Vegetation Index'
        self.formula = '100*(Log([NIR])-Log([RED EDGE]))'
        self.reference = 'Jasper et al., 2009'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
        return 100 * (np.log(nir) - np.log(red_edge))


class REWDRVI:
    def __init__(self, a=0.12):
        self.name = 'Red Edge Wide Dynamic Range Vegetation Index'
        self.formula = f'(a*[NIR]-[RED EDGE])/(a*[NIR] + [RED EDGE]) (a = {a})'
        self.reference = 'Cao et al., 2013'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red_edge: np.ndarray, a=0.12) -> np.ndarray:
        return (a * nir - red_edge) / (a * nir + red_edge)


class RVI:
    def __init__(self):
        self.name = 'Ratio Vegetation Index'
        self.formula = '[NIR]/[RED]'
        self.reference = 'Roncagliolo et al., 2012'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return nir / red


class SAVI:
    def __init__(self):
        self.name = 'Soil Adjusted Vegetation Index'
        self.formula = '1.5*([NIR]-[RED])/([NIR]+[RED]+0.5)'
        self.reference = 'Alam et al., 1996'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return 1.5 * (nir - red) / (nir + red + 0.5)


class SAVI_SR:
    def __init__(self):
        self.name = 'SAVI*SR'
        self.formula = '(Sqr([NIR])-[RED])/(([NIR]+[RED]+0.5)*[RED])'
        self.reference = 'Roujean and Breon, 1995'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (np.square(nir) - red) / ((nir + red + 0.5) * red)


class TCARI:
    def __init__(self):
        self.name = 'Transformed Chlorophyll Absorption in Reflectance Index'
        self.formula = '3*(([RED EDGE]-[RED])-0.2*([RED EDGE]-[GREEN])*([RED EDGE]/[RED]))'
        self.reference = 'Haboudane et al., 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 3 * ((red_edge - red) - 0.2 * (red_edge - green) * (red_edge / red))


class TCARI_MSAVI:
    def __init__(self):
        self.name = 'TCARI/MSAVI'
        self.formula = '[TCARI]/[MSAVI]'
        self.reference = 'Haboudane et al., 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, tcari: np.ndarray, msavi: np.ndarray) -> np.ndarray:
        return tcari / msavi


class TCARI_OSAVI:
    def __init__(self):
        self.name = 'TCARI/OSAVI'
        self.formula = '[TCARI]/[OSAVI]'
        self.reference = 'Haboudane et al., 2002'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, tcari: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return tcari / osavi


class TCI:
    def __init__(self):
        self.name = 'Triangular Chlorophyll Index'
        self.formula = '1.2*([RED EDGE]-[GREEN])-1.5*([RED]-[GREEN])*Sqr([RED EDGE]/[RED])'
        self.reference = 'Haboudane et al., 2008'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, red_edge: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 1.2 * (red_edge - green) - 1.5 * (red - green) * np.square(red_edge / red)


class TCI_OSAVI:
    def __init__(self):
        self.name = 'TCI/OSAVI'
        self.formula = '[TCI]/[OSAVI]'
        self.reference = 'Haboudane et al., 2008'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, tci: np.ndarray, osavi: np.ndarray) -> np.ndarray:
        return tci / osavi


class TNDGR:
    def __init__(self):
        self.name = 'Transformed Normalized Green and Red'
        self.formula = 'Sqr(([GREEN]-[RED])/([GREEN]+[RED])+0.5)'
        self.reference = 'Tucker, 1979'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, red: np.ndarray) -> np.ndarray:
        return np.square((green - red) / (green + red) + 0.5)


class TNDVI:
    def __init__(self):
        self.name = 'Transformed Normalized Vegetation Index'
        self.formula = 'Sqr((([NIR]-[RED])/([NIR]+[RED])+0.5))'
        self.reference = 'Sandham, 1997'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return np.square((nir - red) / (nir + red) + 0.5)


class TVI:
    def __init__(self):
        self.name = 'Triangular Vegetation Index'
        self.formula = '0.5*(120*([NIR]-[GREEN])-200*([RED]-[GREEN]))'
        self.reference = 'Broge and Leblanc, 2001'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, green: np.ndarray) -> np.ndarray:
        return 0.5 * (120 * (nir - green) - 200 * (red - green))


class VIopt:
    def __init__(self):
        self.name = 'Optimal Vegetation Index'
        self.formula = '1.45*((([NIR]*[NIR])+1)/([RED]+0.45))'
        self.reference = 'Reyniers et al., 2006'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        return 1.45 * ((np.square(nir) + 1) / (red + 0.45))


class WDRVI:
    def __init__(self, a=0.12):
        self.name = 'Wide Dynamic Range Vegetation Index'
        self.formula = f'(a*[NIR]-[RED])/(a*[NIR] + [RED]) (a = {a})'
        self.reference = 'Gitelson, 2004'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, nir: np.ndarray, red: np.ndarray, a=0.12) -> np.ndarray:
        return (a * nir - red) / (a * nir + red)


class WI:
    def __init__(self):
        self.name = 'Warmth Index'
        self.formula = '([GREEN]-[BLUE])/([RED]-[GREEN])'
        self.reference = 'Gitelson et al., 2003'
        self.doi = 'http://dx.doi.org/10.1234/example_doi'

    def __call__(self, green: np.ndarray, blue: np.ndarray, red: np.ndarray) -> np.ndarray:
        return (green - blue) / (red - green)


