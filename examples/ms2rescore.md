# MS²ReScore configuration

_MS²ReScore JSON configuration file._

## Properties

- **`general`** _(object)_: General MS²ReScore settings. Cannot contain additional properties.
  - **`pipeline`** _(string)_: Pipeline to use, depending on input format. Must be one of: `["infer", "pin", "tandem", "maxquant", "msgfplus", "peptideshaker"]`. Default: `"infer"`.
  - **`feature_sets`** _(array)_: Feature sets for which to generate PIN files and optionally run Percolator. Length must be at least 1. Items must be unique. Default: `["all"]`.
    - **Items** _(string)_: Must be one of: `["all", "ms2pip_rt", "searchengine", "rt", "ms2pip"]`.
  - **`id_decoy_pattern`**: Pattern used to identify the decoy PSMs in identification file. Passed to `--pattern` option of Percolator converters. Default: `null`.
    - **One of**
      - _string_
      - _null_
  - **`run_percolator`** _(boolean)_: Run Percolator within MS²ReScore. Default: `false`.
  - **`num_cpu`** _(number)_: Number of parallel processes to use; -1 for all available. Minimum: `-1`. Must be an integer. Default: `-1`.
  - **`config_file`**: Path to configuration file.
    - **One of**
      - _string_
      - _null_
  - **`identification_file`** _(string)_: Path to identification file.
  - **`mgf_path`**: Path to MGF file or directory with MGF files.
    - **One of**
      - _string_
      - _null_
  - **`tmp_path`**: Path to directory to place temporary files.
    - **One of**
      - _string_
      - _null_
  - **`output_filename`**: Path and root name for output files.
    - **One of**
      - _string_
      - _null_
  - **`log_level`** _(string)_: Logging level. Must be one of: `["debug", "info", "warning", "error", "critical"]`.
  - **`const`** _(string)_: Const attribute. Must be: `"value"`.
- **`ms2pip`** _(object)_: MS²PIP settings. Cannot contain additional properties.
  - **`model`** _(string)_: MS²PIP model to use (see MS²PIP documentation). Default: `"HCD"`.
  - **`frag_error`** _(number)_: MS2 error tolerance in Da. Minimum: `0`. Default: `0.02`.
  - **`modifications`** _(array)_: Array of peptide mass modifications.
    - **Items**: Refer to _[#/definitions/modifications](#definitions/modifications)_.
- **`percolator`** _(object)_: Command line options directly passed to Percolator (see the Percolator wiki).
- **`maxquant_to_rescore`** _(object)_: Settings specific to the MaxQuant pipeline. Cannot contain additional properties.
  - **`mgf_dir`** _(string, required)_: Path to directory with MGF files.
  - **`modification_mapping`** _(object, required)_: Mapping of MaxQuant modification labels to modifications names for MS²PIP. Default: `{}`.
  - **`fixed_modifications`** _(object, required)_: Mapping of amino acids with fixed modifications to the modification name. Default: `{}`.

## Definitions

- <a id="definitions/modifications"></a>**`modifications`** _(object)_: Peptide mass modifications, per amino acid. Cannot contain additional properties.
  - **`name`** _(string, required)_: Unique name for modification.
  - **`unimod_accession`** _(number, required)_: Unimod accession of modification. Must be an integer.
  - **`mass_shift`** _(number, required)_: Mono-isotopic mass shift.
  - **`amino_acid`**: Amino acid one-letter code, or null if amino acid-agnostic (e.g. N-term acetylation).
    - **One of**
      - _string_: Length must be equal to 1.
      - _null_
  - **`n_term`** _(boolean, required)_: Modification is N-terminal.
