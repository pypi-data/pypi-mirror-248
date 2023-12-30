import click
import sys, os, re, io
import tomllib as toml
import shutil
import pandas as pd
import numpy as np
import pyarrow as pa, pyarrow.parquet as pq
from IPython.display import display

pd.set_option('display.max_colwidth', None)

@click.group()
def specs():
    """Managed specs for structured conversion from CSV to Parquet"""
    pass

@specs.command()
@click.option('--specs-location', default='.structured-specs', required=True,
              help='Location of specs files. Defaults to .structured-specs in current directory')
@click.option('--yes', is_flag=True)
def reset(specs_location, yes):
    """Reset specs."""
    if not yes:
        if not click.confirm(f"Specs in folder {specs_location} will be reset. Do you want to continue?", abort=True):            
            print("Aborted")
    
    if not valid_specs_location(specs_location):
        return 0
    else:
        if os.path.exists(specs_location):
            shutil.rmtree(specs_location)

    os.makedirs(specs_location)

    # create default global specs if not exist
    f = open(os.path.join(specs_location,"global-defaults.toml"),'w')
    toml.dump(global_default_specs, f)
    f.close()

@specs.command()
@click.option('--raw-zone', default="raw-zone", required=True, 
              help='Location of Raw Zone')
@click.option('--specs-location', default='.structured-specs', 
              help='Location of the specs files. Defaults to .structured-specs in current directory')
@click.option('--autogenerate', is_flag=True, 
              help='Automatically generate structure specs based on templates if no existing specs file found for a dataset. Additional specs properties are added based on sample data.')
@click.option('--raw-zone-filter',
              help='Simple text filter for raw-zone files.')
@click.option('--partition-indicator-regex',
              help='Regular expression to differentiate partitioned and non-partitioned datasets. If not set, global default PARTITION_INDICATOR_REGEX will be used.')
@click.option('--dataset-capturing-group',
              help='Regular expression to group different raw-zone files into common datasets. If not set, global default DATASET_CAPTURING_GROUP will be used.')
def scan(specs_location, raw_zone, autogenerate, raw_zone_filter, 
            partition_indicator_regex, dataset_capturing_group):
    """Scan raw-zone for specs. If autogenerate flag is set, specs for available dataset are updated only for missing properties. Existing properties in a particular specs file will not be affected"""
    result = scan_func(specs_location, raw_zone, autogenerate, raw_zone_filter, 
            partition_indicator_regex, dataset_capturing_group, "scan")
    return result
    
def scan_func(specs_location, raw_zone, autogenerate, raw_zone_filter, 
            partition_indicator_regex, dataset_capturing_group, caller):
    if not valid_specs_location(specs_location):
        return 1
           
    if not os.path.exists(global_default_specs_path := os.path.join(specs_location,"global-defaults.toml")):
        if autogenerate:
            if not os.path.exists(specs_location):
                os.makedirs(specs_location)
            f = open(global_default_specs_path,'w')
            toml.dump(global_default_specs, f)
            f.close()
            scan_specs = global_default_specs
        else:
            scan_specs = global_default_specs
    else:
        scan_specs = toml.load(os.path.join(specs_location,"global-defaults.toml"))

    if partition_indicator_regex is None:
        partition_indicator_regex = scan_specs["PARTITION_INDICATOR_REGEX"]
    if dataset_capturing_group is None:
        dataset_capturing_group = scan_specs["DATASET_CAPTURING_GROUP"]

    inputfiles = []
    for root, dirs, files in os.walk(raw_zone):
        for name in files:
            if raw_zone_filter is not None:
                if not raw_zone_filter in name:
                    continue

            if name.endswith(('.csv', '.txt')):
                dataset = os.path.basename(os.path.splitext(name)[0])
                try:
                    partition = re.search(partition_indicator_regex, dataset).group(0)[1:]
                except(AttributeError):
                    partition = None

                if partition:
                    dataset = re.search(dataset_capturing_group, dataset).groups(1)[0]
                else:
                    pass
                
                dataset_specs = os.path.join(specs_location, f"{dataset}.toml")
                inputfiles_item = (dataset, (os.path.join(root, name)), partition, dataset_specs)
                inputfiles.append(inputfiles_item)
    
    if inputfiles == []:
        print("No datasets found.")
        return 0

    specs_df = pd.DataFrame(inputfiles, columns=["Dataset", "Source Files", "Partition", "Specs"])
    np_datasets = specs_df[specs_df["Partition"].isna()].reset_index(drop=True).copy()
    np_datasets.index = np_datasets.index + 1
    p_datasets = specs_df[specs_df["Partition"].notnull()].reset_index(drop=True).copy()
    p_datasets["Location"] = p_datasets["Source Files"].apply(os.path.dirname)
    p_datasets_stats = p_datasets.groupby(['Dataset', 'Location']).agg(
        Partitions = pd.NamedAgg("Dataset", "count"), Specs= pd.NamedAgg("Specs", "max")).reset_index()
    p_datasets_stats.index = p_datasets_stats.index + 1
    
    # check for multiple source writing to the same output
    duplicates = specs_df[(specs_df["Specs"].duplicated()) & (specs_df["Partition"].isna())]
    duplicates = specs_df[specs_df["Dataset"].isin(duplicates["Dataset"].unique())].reset_index(drop=True)
    duplicates.index = duplicates.index + 1

    if not autogenerate:
        # if not autogenerate, scan results will be printed if the caller is "scan"
        if caller == "scan":
            if len(np_datasets) > 0:
                print("Non-partitioned Datasets")
                print(np_datasets[["Dataset", "Source Files", "Specs"]])
                print()

            if len(p_datasets) > 0:               
                print("Partitioned Datasets")        
                print(p_datasets_stats)
                print()

            if len(duplicates) > 0:
                print("Warning: Multiple non-partitioned datasets having the same specs.")
                print(duplicates)

    else:
        # if autogenerate, update specs file
        if len(duplicates) > 0:
            print("Error: Multiple non-partitioned datasets having the same specs.")
            print(duplicates)
            print("Aborted!")
            sys.exit(0)

        for dataset_specs in (list(p_datasets_stats["Specs"].unique()) + list(np_datasets["Specs"].unique())):
            # create dataset specs if not exist    
            if not os.path.exists(dataset_specs):
                f = open(dataset_specs,'w')
                current_dataset_specs = dataset_default_specs
                current_dataset_specs.update({"DATASET_NAME": os.path.basename(dataset_specs)[:-5]})
                toml.dump(current_dataset_specs, f)
                f.close()
        
        for i, (dataset, raw_zone_file, partition, specs) in specs_df.assign(partlen = lambda d: d["Partition"].str.len()).sort_values(
                by=["Dataset","partlen", "Partition"]).drop_duplicates(subset=["Dataset"], keep="last").drop(columns=["partlen"]).iterrows():
            dataset_specs = toml.load(specs)
            
            for k in dataset_default_specs:
                if k not in dataset_specs:
                    dataset_specs[k] = dataset_default_specs[k]

            try:
                if dataset_specs["READER"]["CSV_READER"] == "pandas":
                    csvreader = pd.read_csv
                else:
                    print(f"Only pandas is supported as CSV reader. Skip processing {dataset}.")
                    continue
            except(KeyError):
                print("No CSV reader specified.")

            try:
                if dataset_specs["READER"]["CRLF_HANDLING"]:
                    f = open(raw_zone_file,'r+b', newline=None).read()
                    f =  io.BytesIO(f.replace(b'\\\r\n', b',').replace(b'\\', b''))
            except(AttributeError):
                f = raw_zone_file

            csvreader_kwargs = {}
            try:
                if dataset_specs["READER"]["SEPARATOR"] == "auto":
                    csvreader_kwargs["sep"] = None
                    csvreader_kwargs["engine"] = "python"
                else:
                    sep = dataset_specs["READER"]["SEPARATOR"]
            except(KeyError):
                csvreader_kwargs["sep"] = ","

            try:
                if "PANDAS_DTYPES" in dataset_specs:
                    dataset_dtypes = dataset_specs["PANDAS_DTYPES"]
                else:
                    dataset_dtypes = {}
                dataset_df = csvreader(raw_zone_file, **csvreader_kwargs, nrows=1000, dtype=dataset_dtypes)
                
            except(pd.errors.EmptyDataError):
                print(f"{raw_zone_file} is empty. Unable to autogenerate specs")
                sys.exit()

            try:
                if dataset_specs["READER"]["DROP_UNNAMED"]:
                    unnamed_columns = [ c for c in dataset_df.columns if c.startswith('Unnamed:') ]
                    dataset_df.drop(unnamed_columns, axis=1, inplace=True)
            except(KeyError):
                pass

            dataset_df.fillna(pd.NA, inplace=True)

            datecols = {}
            for c in dataset_df.select_dtypes(include=['object']).columns:
                try:
                    # does not work if total row less than sample size 100
                    value_lengths = set(dataset_df[c].sample(100).dropna().apply(len))                     
                    dataset_df[c] = pd.to_datetime(dataset_df[c])
                    if value_lengths.issubset({8,10}):
                        datecols[c] = pa.date32()
                    elif max(value_lengths) == 19:
                        datecols[c] = pa.timestamp('s')
                    elif max(value_lengths) > 19:
                        datecols[c] = pa.timestamp('ns')
                except(pd.errors.ParserError, ValueError):
                    pass                        

            dataset_df_dtypes = dataset_df.dtypes.to_dict()
            cols = { k:dtypes_mapping[dataset_df_dtypes[k]] for k in dataset_df.columns}
            cols.update(datecols)

            if not "PANDAS_DTYPES" in dataset_specs:
                dataset_specs["PANDAS_DTYPES"] = { 
                    k:str(dataset_df_dtypes[k]) for k in dataset_df_dtypes if 
                        str(dataset_df_dtypes[k]) not in pandas_timestamp_dtypes
                }

                # change to nullable dtypes
                for k in dataset_specs["PANDAS_DTYPES"]:
                    if dataset_specs["PANDAS_DTYPES"][k] == "float64":
                        dataset_specs["PANDAS_DTYPES"][k] = "Float64"
                    elif dataset_specs["PANDAS_DTYPES"][k] == "int64":
                        dataset_specs["PANDAS_DTYPES"][k] = "Int64"

                f = open(specs,'w')            
                toml.dump(dataset_specs, f)
                f.close()    

            if not "PYARROW_SCHEMA" in dataset_specs:
                schema = pa.schema(pa.field(k,cols[k]) for k in cols.keys())
                s = dict(zip(schema.names, [str(field) for field in schema.types]))
                dataset_specs["PYARROW_SCHEMA"] = s
                f = open(specs,'w')            
                toml.dump(dataset_specs, f)
                f.close()    
                continue
            else:
                # no update is done to existing specs if property already available
                pass

    return specs_df

global_default_specs = {
    "VERSION": 1,
    "OUTPUT_PARQUET_VERSION": "2.6",
    "PARTITION_INDICATOR_REGEX": r"[_-]{1}\d{1,10}$",
    "DATASET_CAPTURING_GROUP": r"(^.*)[_-]{1}\d{1,10}$"
}

dataset_default_specs = {
    "SKIP": False,
    "READER": {
        "CRLF_HANDLING": False,
        "CSV_READER": "pandas",
        "SEPARATOR": ","
    },
    "TIMESTAMP": {
        "DEFAULTS": {
            "LOCAL_TIMEZONE": 'Asia/Kuala_Lumpur',
            "DAYFIRST": True
        },
        "CUSTOM": {
            "COLUMN_NAME_1": {
                "FORMAT": "%Y-%m-%d",
                "TIMEZONE_READ_AS": None,
                "TIMEZONE_CONVERT_TO": None
            }, 
            "COLUMN_NAME_2": {
                "FORMAT": "%Y-%m-%d",
                "TIMEZONE_READ_AS": "UTC",
                "TIMEZONE_CONVERT_TO": "Asia/Kuala_Lumpur"
            },
        }
    },
    "TRANSFORM": {
        "VALUE_TRIM": ['*'],
        "DROP_UNNAMED_COLUMNS": True
    }
}

dtypes_mapping = {
    np.dtype('O'): pa.string(),
    np.dtype('int64') : pa.int64(),
    np.dtype('int32') : pa.int32(),
    np.dtype('float64') : pa.float64(),
    np.dtype('<M8[ns]') : pa.timestamp('ns'),
    pd.Int64Dtype(): pa.int64(),
    pd.Float64Dtype(): pa.float64(),
}

pandas_timestamp_dtypes = [    
    "datetime64[ns]"
]

def valid_specs_location(specs_location):
    if not specs_location.endswith("-specs"):
        print("The name for specs location must end with '-specs' to avoid potentially corrupting folders containing data")
        print("Reset aborted.")
        return False
    else:
        if os.path.exists(specs_location):
            if not os.path.isdir(specs_location):
                print(f"Location {specs_location} already exists and is not a directory")
                print("Reset aborted.")
                return False
            elif os.listdir(specs_location):
                if { f[-5:] for f in (os.listdir(specs_location))} != {'.toml'}:
                    print(f"Location {specs_location} contains non-TOML files")
                    print("Reset aborted.")
                    return False
    return True