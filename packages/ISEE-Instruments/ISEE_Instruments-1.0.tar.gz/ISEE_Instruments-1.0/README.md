


# ISEE_Instruments

ISEE_Instruments is a Python library written to expedite instrumental analysis for members of the [Takeuchi-Marschilok group](https://www.stonybrook.edu/commcms/iese/) (Stony Brook University, NY, USA).

## About

Instruments is built heirarchically around a core data structures: the Spectrum. This class is designed to streamline the analysis of a wide variety of spectroscopic and spectrum-like datasets
by providing common utility functions of spectral analysis *(ex. spectrum addition/subtraction, normalization, filtering, etc.)*.

The second fundamental structure is the Series, which functions as an ordered collection of Spectrum objects. Many of the same utilty methods which are included
in the Spectrum class are also methods for the Series class, allowing the same procedure to be carried out on all represented spectra simultaneously. Additional
methods which are only applicable to multiple spectra are also available through the Series class *(ex. averaging, multivariate analysis)*.

Subclasses of both the Spectrum and Series classes are available for specialized analysis of several different spectral types, including cell cycling data, UV-Vis/Raman
photospectra, and powder XRD spectra.
## Getting Starated
The library can be installed by downloading all files to a new directory named "Instruments" in your Python home directory.
### Prerequisites
This library depends on the following Python packages. All of these packages are available through PyPI.

* *NumPy*
* *Matplotlib*
* *Scipy*
* *sklearn*
* MACCOR data import module additionally requires: *xlrd*

### Installation
The Instruments library can be installed by copying all files into a directory titled "Instruments" in your system's Python home directory.
Alternatively, simply add the folder containing the Instruments library to your system's PYTHONPATH variable.
## Usage
Although precise usage will depend on the precise instrument used, each subtype of Spectrum and Series rely on the same core set of functions.
A new Spectrum object can be created by:
```
spectrum = Spectrum((x, y)) #Where x and y are iterables representing the x and y axes of the spectrum
```

The x and y axes of the spectrum can be accessed as attributes:
```
spectrum.x
spectrum.y
```
Arbitrary metadata parameters can be assigned through:
```
spectrum.parameters		#A standard Python dictionary
```
The created Spectrum object is compatible with standard mathematical operators:
```
spectrum + 5
spectrum - 5
spectrum * 5
spectrum / 5
```
A few methods for the created spectrum:
```
spectrum.show()				#Displays spectrum in active Matplotlib window
spectrum.normalize('basepeak')	#Returns base-normalized spectrum, other normalization modes available
spectrum.slice(250,500)		#Returns the band from the imported_spectrum between 250 and 500 units along the x axis
spectrum.copy()				#Returns an identical PhotoSpectrum object
```
Multiple data files can be imported as Spectra, then arranged in a Series (in the case of this data, a PhotoSeries):
```
series = PhotoSeries()
for filename in list_of_filenames:
	series.append(olis.load(filename)
```
Series objects are iterable, and can be indexed by integer keys:
```
for spectrum in series:
	spectrum.show()
```
```
spectrum = series[0]
```
Many of the same methods which can be applied to individual spectra can also be applied batch-wise to all spectra in a series:
```
series + 5
series - 5
series * 5
series / 5

series.show()					#Displays all spectra in series in active Matplotlib window
series.normalize('basepeak')	#Applies base-normalization to all spectra in series, then returns the normalized series
series.slice(250,500)			#Slices all spectra along the same bounds, returns new series populated by sliced spectra
series.copy()					#Returns an identical Series object
```
Additional methods applicable only to multiple spectra are available through the Series class:
```
series.sum()					#Returns the sum of all spectra in series
series.average()				#Returns the average spectrum from all spectra in series
series.PCA(n_components=5)		#Calculates and returns 5-component PCA of series
```

### Example

An example is given for import, Savitzky-Golay filtering, and calculation of a calibration curve for a series of UV-Vis spectra collected on the Olis instrument. Imagine a set of 8 UV-Vis spectra of an aqueous solution of some analyte with a strong absorbance band centered at 470 nm.

Begin by importing the Instruments module:
```
import Instruments
```
An Olis data file interface object can be spawned with:
```
olis = Instruments.Olis()
```
A single PhotoSpectrum can be imported from the data file *filename* and displayed by:
```
imported_spectrum = olis.load(filename)
imported_spectrum.show()
```
Given a list of our 8 filenames (*list_of_filenames*), you can quickly create a PhotoSeries and populate it with PhotoSpectrum objects by:
```
imported_series = Instruments.PhotoSeries()
for filename in list_of_filenames:
	new_spectrum = olis.load(filename)
	imported_series.append(new_spectrum)
```
You can display all individual spectra and the average spectrum in separate Matplotlib windows:
```
imported_series.show()
average = imported_series.average()
average.show(append=False)
```
A Savitzky-Golay filter is applied to all spectra in *imported_series* individually (window width = 11 points, polynomial order = 3):
```
filtered = imported_series.savgol_filter(window_length=11, order=3)
```
Because the specialized PhotoSeries class is being used to handle the imported data, a calibration curve can be calculated from the filtered spectra using a method not available to the base Series class.
If, for example, the spectra were collected from solutions with concentrations of 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, and 1.4 molar, a calibration curve at 470 nm can be calculated and displayed by:
```
concentrations = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.4]
p, r2 = filtered.calibrate(concentrations, 470, plot=True)
print(p, r2)
#p is a tuple containing the coefficients describing the line-of-best-fit for the Beer-Lambert plot
#r2 is the r-squared of the fitted line
```
