# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2.5 - 2023-12-23

This version fixes an installation error on recent OSX versions, and a segmentation fault that triggers in some edge cases.

Thanks to Francesco Coti Zelati for [reporting the original issue](https://github.com/v-morello/riptide/issues/4) that led to both fixes.

### Fixed

- Fixed a serious bug where some intermediate output arrays were unexpectedly allocated with a size one element smaller than expected, causing segmentation faults. This was found to be a side effect of the compilation flag `-freciprocal-math`. See issue [#4](https://github.com/v-morello/riptide/issues/4) for a detailed explanation. The set of compilation flags for the C++ extensions has been reviewed and adjusted.
- The C++ extensions can now be built with the C++17 standard enabled without throwing any errors or warnings. Recent `clang` versions (the default compiler on OSX) would throw a number of narrowing conversion errors, which would in turn make the installation of riptide fail with a cryptic error message. 


## 0.2.4 - 2022-02-03

This version fixes a bug where all the functions in the python bindings to the C++ code (exposed in `riptide.libcpp` on the Python side) assume that their input numpy arrays are contiguous in memory. In practice, passing a column slice of a two-dimensional `float32` array to `fast_running_median` was found to produce incorrect results: the rather than reading `data[:, col_index]`, the code read `data[0, col_index:col_index+num_cols]`. The issue would only trigger on the `float32` type, because otherwise an implicit copy (contiguous in memory) of the input was created.

Thanks to Akshay Suresh for finding the bug and reporting it.

### Fixed
- All C++ functions in `python_bindings.cpp` now explicitly check that all input arrays are contiguous in memory, and throw `std::invalid_argument` otherwise (maps to `ValueError` in Python).
- The size equality check of the input arrays for the `rollback` function in `python_bindings.cpp` is now correct

### Added
- `running_median` function that wraps its counterpart in the C++ library. It ensures that the array passed to it is contiguous in memory, and if not, makes a temporary contiguous copy before doing so.
- Unit test that checks the correctness of `running_median` on non-contiguous data slices.
- The `riptide` module now exposes the functions `running_median` and `fast_running_median`. Document how boundary conditions are handled in running median calculation. Added entries for both functions in the documentation, in Kernel Functions section.

### Changed
- Renamed the file `running_median.py` to `running_medians.py` to avoid name collisions.


## 0.2.3 - 2021-08-01

### Updated
- Packaging is now PEP 517/518 compliant
- Using `setuptools-scm` instead of `versioneer` (which is not maintained anymore) for automatic versioning


## 0.2.2 - 2021-07-24

### Added
- Added full documentation and readthedocs integration. The docs can be found [here](https://riptide-ffa.readthedocs.io).
- Fixed typos in docstrings, extra docstrings for `Periodogram` class

### Updated
- Base Dockerfile on python:3.8, ensure all tests pass during the build

### Fixed
- It is now possible to specify period ranges so that the data are searched at their raw resolution (no downsampling). This corresponds to choosing period range parameters such that `period_min = bins_min x tsamp`. In this case, the code would previously raise an error saying that it could not downsample the data with a factor equal to 1, which was not the intended behaviour.
- Fixed an issue where the C++ functions `check_trial_widths` and `check_stdnoise` would systematically throw an exception regardless of their input arguments. The issue was occurring with `gcc 8.3.0` on some systems, and appears to have been caused by said functions having a return type `bool` while they actually did not return anything. The functions have `void` return type now.


## 0.2.1 - 2020-10-27

### Added
- Limited support for X-ray and Gamma time series in PRESTO inf/dat format. `TimeSeries.from_presto_inf()` will now correctly read these. However, a warning will be issued when doing so, because `riptide` is currently designed to process data where the background noise is Gaussian. **Be aware that processing high-energy data may produce junk results.**

### Fixed
- Docstring of `TimeSeries.generate()` was missing the `period` parameter


## 0.2.0 - 2020-08-10

**This release contains significant improvements and additions but breaks compatibility with** `v0.1.x`.

### Changed
- The `ffa_search()` function now only returns two values: the de-reddened `TimeSeries` that was actually searched, and a `Periodogram` object. The `ProcessingPlan` class has been removed.
- Clean rewrite of all kernels in C++. Python bindings for said kernels are now generated with `pybind11` which requires a lot less boilerplate code. Kernel functions can imported in python from the `riptide.libcpp` submodule.
- The python function `get_snr()` has been renamed `boxcar_snr()`
- Moved unit tests to `riptide/tests` so they can be packaged with the rest of the module


### Added
- The `Periodogram` returned by `ffa_search` now has a `foldbins` member, which is the number of phase bins that were used when folding the data for a particular trial period. Using this information, the pipeline now returns the *true* duty cycle of the candidates; it was previously returning only an estimate equal to `width / bins_avg` where `width` was the best pulse width in bins, and `bins_avg = (bins_min + bins_max) / 2`.
- `running_median()` function in C++, it is around 8x faster than its former python counterpart.
- Tests for `running_median()`
- Tests for `boxcar_snr()`
- DM trial selection by the pipeline is now considerably faster
- The pipeline now infers the observing min/max frequencies and the number of channels from the input data if possible. It is now recommended to leave the fields `fmin`, `fmax`, and `nchans` blank in the pipeline configuration file. It is necessary to specify these values only when the dedispersed time series data format (e.g. SIGPROC) does not contain that information.
- In the pipeline configuration file, the minimum and maximum trial DM fields can also be left blank. If so, the minimum and/or maximum DMs of the search are determined by the DM trials available to process.
- Added careful validation of the pipeline configuration file (using the `schema` library). The pipeline will raise an exception early in the processing if the configuration is invalid, with a helpful error message.
- Can now run the unit test suite from python code or IPython by calling `riptide.test()`

### Removed
- Removed `ProcessingPlan` class. It used to be passed to the old C function that was computing the periodogram. Its job is now directly performed by the new C++ function `periodogram()`.
- Removed old C kernels


## 0.1.5 - 2020-05-23

### Changed
- `find_peaks()` now always returns peaks in decreasing S/N order

### Added
- `rseek` command-line application that searches a single dedispersed time series and prints a list of significant peaks found


## 0.1.4 - 2020-05-03

This version reduces RAM usage significantly. Trial periods are now stored as double precision floats.

### Fixed
- Trial periods are now stored as *double* precision floats (`double` in C, `float` in python). When searching very long time series (several hours) and short trial periods, single precision floats were inaccurate enough that small groups of consecutive period trials erroneously ended up having the exact same value. Incorrect detection periods would propagate down the pipeline, and `Candidate` objects could end up being folded with a period slightly offset from the true value.

### Changed
- The pipeline worker sub-processes now get passed a *file path* to a time series as an input, rather than a full `TimeSeries` object, which saves the cost of communicating a lot of data between processes
- The buffers used for downsampling and FFA transforming the data when calculating periodograms are now given the smallest possible size. They only need to hold `N / f` data points, where `N` is the number of samples in the raw time series, and `f` the first downsampling factor in the search plan. Buffers were previously given a size of `N` which was often wasteful.

### Added
- Added option to save pipeline logs to file


## 0.1.3 - 2020-04-27

### Fixed
- Fixed a rare but serious bug in the C function downsample() where the code would attempt to read one element beyond the end of the input array. This would happen only when the downsampling factor was such that `nsamp_input / dsfactor` was exactly an integer. This would cause the last sample in the output to have an absurd value, or a segmentation fault.
- Fixed a crash in the pipeline that would occur when significant peak clusters were found, but none had a S/N that would exceed the `candidate_filters.snr_min` configuration parameter. Turning the resulting empty list of clusters into a CSV would then fail. 
- Fixed a related problem where clusters whose S/N was below `candidate_filters.snr_min` were not saved to the CSV file, which was not the intended behaviour.

### Added
- Unit test suite, to be improved and expanded
- Travis CI
- Codecov integration


## 0.1.2 - 2020-04-15

### Fixed
- `Metadata` is now correctly carrying the "tobs" attribute for TimeSeries loaded from SIGPROC data. This was causing a cryptic error when processing SIGPROC dedispersed time series with the pipeline.

### Added
- Can now read and process 8-bit SIGPROC data
- Can now read SIGPROC header keys of boolean type. In particular the "signed" key (which defines the signedness of 8-bit SIGPROC data) is now supported by default.


## 0.1.1 - 2020-04-08

### Fixed
- Module should now properly install on OSX, where some C compilation options had to be adapted. `numpy.ctypeslib` also expects shared libraries to have a `.dylib` extension on OSX rather than the linux standard `.so`


## 0.1.0 - 2020-04-08

**This release contains major improvements and additions but breaks compatibility with** `v0.0.x`. If you have any ongoing large-scale searches or projects, stick with the older release you were using. Other users should **definitely** use this new version.

### Fixed
- Ensure that each subprocess spawned by the pipeline consumes only one CPU, as initially intended to achieve optimal CPU usage. In previous versions, some `numpy` functions would attempt to run on all CPUs at once which was detrimental. As a result the pipeline is now considerably faster.
- The impact of downsampling by a non-integer factor on the noise variance is now correctly dealt with when normalizing the output S/N values. Refer to the paper for details. The difference should be negligible, except when downsampling the original input data by factors close to 1.
- The Makefile used to build the C sources does not explicitly set `CC=gcc` anymore. The default system compiler will now be used instead. `gcc` will be used by default if the environment variable `CC` is undefined.

### Changed
- Clean rewrite of peak detection algorithm. It uses the same method as before, but the arguments of the `find_peaks()` function have changed. See docstring.
- Now using JSON instead of HDF5 as the data product file format. This is vastly easier to maintain and future-proof. Read/write speed and file sizes remain similar.
- Clean rewrite of the pipeline, which has been improved and runs faster, see below for all related changes.
    - Improved DM trial selection, now uses a method similar to PRESTO's `DDPlan` to achieve the least expensive DM space coverage
    - Input de-reddening and normalisation is now common to all search period sub-ranges, further improving pipeline run time
    - Harmonic flagging is now always performed
    - Removing harmonics from the output candidate list is now optional
    - Added option to produce all candidate plots at the end of the pipeline run
    - Candidate plots look nicer
    - Saving candidate files and plots is done with multiple CPUs and runs faster
    - The pipeline configuration file keywords / schema has been adjusted to match all pipeline changes, see example provided and documentation
- `Candidate` class has been refactored, its attribute and method names have changed
- Changed name of high level FFA transforms to `ffa1()` and `ffa2()`. 
- Updated signal generation functions so that the 'amplitude' parameter now represents the expected true signal-to-noise ratio

### Added
- `TimeSeries` now has a `fold()` method that returns a numpy array representing either sub-integrations or a folded profile
- Timing of all pipeline stages
- Dynamic versioning using the `versioneer` module. In python, the current version is accessible via `riptide.__version__`
- Added `ffafreq()` and `ffaprd()` to generate list of FFA transform trial freqs / periods.

### Removed
- Removed the `SubIntegrations` class which added unneeded complexity, sub-integrations are now represented as a 2D numpy array


## 0.0.3 - 2019-11-30
### Added
- Full docstring for `ffa_search()`

### Changed
- Cleaner and faster FFA C kernels, which have been moved to separate files
- Slight optimisation to S/N calculation, where only the best value across all pulse phases is normalized, instead of normalizing at every phase trial
- S/N calculation separated into smaller functions
- Removed OpenMP multithreading from S/N calculation, it was slower in most usual cases. The benefits were visible only for very large input data. As a result, `ffa_search()` does not accept the 'threads' keyword anymore, and the 'threads' keyword has also been removed from the pipeline configuration files (in the 'search' section). Parallelism only happens at the TimeSeries level, i.e. one process per TimeSeries.

### Fixed
- Reinstated the `--fast-math` compilation option that had been accidentally removed in v0.0.2. The code is now much faster.


## 0.0.2 - 2019-11-05
### Added
- `riptide` is now properly packaged with a `setup.py` script. Updated installation instructions in `README.md`
- Updated Dockerfile. Build docker image with `make docker` command.

### Fixed
- When normalising TimeSeries, use a float64 accumulator when calculating mean and variance. This avoid saturation issues on data with high values, e.g. from 8-bit Parkes UWL observations.

### Changed
- Improved candidate plots: docstring for `Candidate` class, DM unit on plots, option to subtract the baseline value of the profile before displaying it, option to plot the profile as either a bar or line chart.

## 0.0.1 - 2018-10-25
### Added
- First stable release of riptide. This is the version that will be run on the LOTAAS survey.
