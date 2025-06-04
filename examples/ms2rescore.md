# MS²ReScore configuration

_MS²ReScore JSON configuration file._

## Properties

- <a id="properties/general"></a>**`general`** _(object)_: General MS²ReScore settings. Cannot contain additional properties.
  - <a id="properties/general/properties/pipeline"></a>**`pipeline`** _(string)_: Pipeline to use, depending on input format. Must be one of: "infer", "pin", "tandem", "maxquant", "msgfplus", or "peptideshaker". Default: `"infer"`.
  - <a id="properties/general/properties/feature_sets"></a>**`feature_sets`** _(array)_: Feature sets for which to generate PIN files and optionally run Percolator. Length must be at least 1. Items must be unique. Default: `["all"]`.
    - <a id="properties/general/properties/feature_sets/items"></a>**Items** _(string)_: Must be one of: "all", "ms2pip_rt", "searchengine", "rt", or "ms2pip".
  - <a id="properties/general/properties/id_decoy_pattern"></a>**`id_decoy_pattern`**: Pattern used to identify the decoy PSMs in identification file. Passed to `--pattern` option of Percolator converters. Default: `null`.
    - **One of**
      - <a id="properties/general/properties/id_decoy_pattern/oneOf/0"></a>_string_
      - <a id="properties/general/properties/id_decoy_pattern/oneOf/1"></a>_null_
  - <a id="properties/general/properties/run_percolator"></a>**`run_percolator`** _(boolean)_: Run Percolator within MS²ReScore. Default: `false`.
  - <a id="properties/general/properties/num_cpu"></a>**`num_cpu`** _(number)_: Number of parallel processes to use; -1 for all available. Minimum: `-1`. Must be an integer. Default: `-1`.
  - <a id="properties/general/properties/config_file"></a>**`config_file`**: Path to configuration file.
    - **One of**
      - <a id="properties/general/properties/config_file/oneOf/0"></a>_string_
      - <a id="properties/general/properties/config_file/oneOf/1"></a>_null_
  - <a id="properties/general/properties/identification_file"></a>**`identification_file`** _(string)_: Path to identification file.
  - <a id="properties/general/properties/mgf_path"></a>**`mgf_path`**: Path to MGF file or directory with MGF files.
    - **One of**
      - <a id="properties/general/properties/mgf_path/oneOf/0"></a>_string_
      - <a id="properties/general/properties/mgf_path/oneOf/1"></a>_null_
  - <a id="properties/general/properties/tmp_path"></a>**`tmp_path`**: Path to directory to place temporary files.
    - **One of**
      - <a id="properties/general/properties/tmp_path/oneOf/0"></a>_string_
      - <a id="properties/general/properties/tmp_path/oneOf/1"></a>_null_
  - <a id="properties/general/properties/output_filename"></a>**`output_filename`**: Path and root name for output files.
    - **One of**
      - <a id="properties/general/properties/output_filename/oneOf/0"></a>_string_
      - <a id="properties/general/properties/output_filename/oneOf/1"></a>_null_
  - <a id="properties/general/properties/log_level"></a>**`log_level`** _(string)_: Logging level. Must be one of: "debug", "info", "warning", "error", or "critical".
  - <a id="properties/general/properties/const"></a>**`const`** _(string)_: Const attribute. Must be: `"value"`.
- <a id="properties/ms2pip"></a>**`ms2pip`** _(object)_: MS²PIP settings. Cannot contain additional properties.
  - <a id="properties/ms2pip/properties/model"></a>**`model`** _(string)_: MS²PIP model to use (see MS²PIP documentation). Default: `"HCD"`.
  - <a id="properties/ms2pip/properties/frag_error"></a>**`frag_error`** _(number)_: MS2 error tolerance in Da. Minimum: `0`. Default: `0.02`.
  - <a id="properties/ms2pip/properties/modifications"></a>**`modifications`** _(array)_: Array of peptide mass modifications.
    - <a id="properties/ms2pip/properties/modifications/items"></a>**Items**: Refer to _[#/definitions/modifications](#definitions/modifications)_.
- <a id="properties/percolator"></a>**`percolator`** _(object)_: Command line options directly passed to Percolator (see the Percolator wiki).
- <a id="properties/maxquant_to_rescore"></a>**`maxquant_to_rescore`** _(object)_: Settings specific to the MaxQuant pipeline. Cannot contain additional properties.
  - <a id="properties/maxquant_to_rescore/properties/mgf_dir"></a>**`mgf_dir`** _(string, required)_: Path to directory with MGF files.
  - <a id="properties/maxquant_to_rescore/properties/modification_mapping"></a>**`modification_mapping`** _(object, required)_: Mapping of MaxQuant modification labels to modifications names for MS²PIP. Default: `{}`.
  - <a id="properties/maxquant_to_rescore/properties/fixed_modifications"></a>**`fixed_modifications`** _(object, required)_: Mapping of amino acids with fixed modifications to the modification name. Default: `{}`.

## Definitions

- <a id="definitions/modifications"></a>**`modifications`** _(object)_: Peptide mass modifications, per amino acid. Cannot contain additional properties.
  - <a id="definitions/modifications/properties/name"></a>**`name`** _(string, required)_: Unique name for modification.
  - <a id="definitions/modifications/properties/unimod_accession"></a>**`unimod_accession`** _(number, required)_: Unimod accession of modification. Must be an integer.
  - <a id="definitions/modifications/properties/mass_shift"></a>**`mass_shift`** _(number, required)_: Mono-isotopic mass shift.
  - <a id="definitions/modifications/properties/amino_acid"></a>**`amino_acid`**: Amino acid one-letter code, or null if amino acid-agnostic (e.g. N-term acetylation).
    - **One of**
      - <a id="definitions/modifications/properties/amino_acid/oneOf/0"></a>_string_: Length must be equal to 1.
      - <a id="definitions/modifications/properties/amino_acid/oneOf/1"></a>_null_
  - <a id="definitions/modifications/properties/n_term"></a>**`n_term`** _(boolean, required)_: Modification is N-terminal.
