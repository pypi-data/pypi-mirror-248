import sys, os, io, re
import click
import tomllib as toml, json
import pandas as pd
import numpy as np
import pyarrow as pa, pyarrow.parquet as pq
from datetime import datetime
from hashlib import sha1
from ..specs.commands import scan_func as scan

@click.command()
@click.option('--raw-zone', default='raw-zone',
              help='Location of Raw Zone that contains CSV files. Defaults to raw-zone')
@click.option('--structured-zone', default='structured-zone', 
              help='Location of Structured Zone. Defaults to structured-zone')
@click.option('--specs-location', default='.structured-specs', 
              help='Location of specs files. Defaults to .structured-specs in current director')
@click.option('--raw-zone-filter',
              help='Simple text filter for raw-zone files.')             
@click.option('--testonly', default=False, is_flag=True,
              help='Testing conversion without saving to Structured Zone') 
def convert(raw_zone, structured_zone, specs_location, raw_zone_filter, testonly):
    """Converts CSV files in raw zone to Parquet files in structured zone."""
    specs_df = scan(specs_location, raw_zone, True, raw_zone_filter, 
            None, None, "convert")
    if type(specs_df) == int and specs_df == 1:
        sys.exit()

    for i, (dataset, raw_zone_file, partition, spec) in specs_df.iterrows():
        if partition is None:
            structured_zone_file = os.path.join(structured_zone, f"{dataset}.parquet")
        else:
            structured_zone_file = os.path.join(structured_zone, dataset, f"{dataset}_{partition}.parquet")
        
        if os.path.exists(structured_zone_file):
            if os.path.getmtime(raw_zone_file) <= os.path.getmtime(structured_zone_file):
                continue
        
        print("Processing", dataset, raw_zone_file)
        dataset_specs = toml.load(spec)

        try:
            if dataset_specs["READER"]["CSV_READER"] == "pandas":
                csvreader = pd.read_csv
            else:
                print(f"Only pandas is supported as CSV reader. Skip processing {dataset}.")
                continue
        except(KeyError):
            print("No CSV reader specified.")

        csvreader_kwargs = {}
        try:
            if dataset_specs["READER"]["SEPARATOR"] == "auto":
                csvreader_kwargs["sep"] = None
                csvreader_kwargs["engine"] = "python"
            else:
                sep = dataset_specs["READER"]["SEPARATOR"]
        except(KeyError):
            csvreader_kwargs["sep"] = ","
        
        if "PANDAS_DTYPES" in dataset_specs:
            csvreader_kwargs["dtype"] = dataset_specs["PANDAS_DTYPES"]

        try:
            if dataset_specs["READER"]["CRLF_HANDLING"]:
                f = open(raw_zone_file,'r+b', newline=None).read()
                f =  io.BytesIO(f.replace(b'\\\r\n', b',').replace(b'\\', b''))
        except(AttributeError):
            f = raw_zone_file

        try:            
            dataset_df = csvreader(raw_zone_file, **csvreader_kwargs)
        except(pd.errors.EmptyDataError):            
            dataset_df = pa.Table.from_pandas(pd.DataFrame())
            if partition is None:
                pq.write_table(dataset_df, structured_zone_file, version="2.6")
            else:
                if not os.path.exists(os.path.join(structured_zone, dataset)):
                    os.makedirs(os.path.join(structured_zone, dataset))
                pq.write_table(dataset_df, structured_zone_file, version="2.6")
            continue

        try:
            if dataset_specs["READER"]["DROP_UNNAMED"]:
                unnamed_columns = [ c for c in df.columns if c.startswith('Unnamed:') ]
                dataset_df.drop(unnamed_columns, axis=1, inplace=True)
        except(KeyError):
            pass

        ####
        #### READ TIMESTAMP RELATED PROPERTIES IN SPECS, APPLY CONVERSION TO DATASET_DF
        pa_schema = dataset_specs["PYARROW_SCHEMA"]
        timestamp_conversion = []
        for c in pa_schema:
            if type(pa_schema[c]) == list:
                type_check = pa_schema[c][0]
            else:
                type_check = pa_schema[c]
            if type_check in [
                "date32[day]", 
                "timestamp[s]", 
                "timestamp[ns]", 
                "timestamp[s, tz=Asia/Kuala_Lumpur]",
                "timestamp[ns, tz=Asia/Kuala_Lumpur]"
            ]:
                timestamp_conversion.append(c)
        
        
        for c in timestamp_conversion:  
            if c in dataset_specs["TIMESTAMP"]["CUSTOM"]:             
                timestamp_format = dataset_specs["TIMESTAMP"]["CUSTOM"][c]["FORMAT"]

                if "OUT_OF_BOUND" in dataset_specs["TIMESTAMP"]:
                    ### pre-processing to manage out of bound datetime
                    def manage_out_of_bound(datestr, dateformat, minyear, maxyear):
                        mindate = datetime(minyear,1,1)
                        maxdate = datetime(maxyear,1,1)
                        try:
                            if datetime.strptime(datestr, dateformat) < mindate:
                                return mindate.strftime(dateformat)
                            elif datetime.strptime(datestr, dateformat) > maxdate:
                                return maxdate.strftime(dateformat)
                            else:
                                return datestr
                        except ValueError as e:
                            msg = e.args[0]                            
                            match = re.search(r'year (\d+) is out of range', msg)
                            if match is not None:
                                if int(match.group(1)) < minyear:
                                    return mindate.strftime(dateformat)
                            else:
                                raise e

                    if dataset_specs["TIMESTAMP"]["OUT_OF_BOUND"]["MANAGE"]:
                        dataset_df[c] = dataset_df[c].apply(lambda s: manage_out_of_bound(s, timestamp_format, 1800, 2260))

                try:                                        
                    timezone_read_as = dataset_specs["TIMESTAMP"]["CUSTOM"][c]["TIMEZONE_READ_AS"]
                    timezone_convert_to = dataset_specs["TIMESTAMP"]["CUSTOM"][c]["TIMEZONE_CONVERT_TO"]

                    if timezone_read_as is None:
                        # read as naive timestamp
                        dataset_df[c] = pd.to_datetime(dataset_df[c],format=timestamp_format)
                    else:
                        dataset_df[c] = pd.to_datetime(dataset_df[c],format=timestamp_format).dt.tz_localize(timezone_read_as)
                        if timezone_convert_to is not None:
                            dataset_df[c] = dataset_df[c].dt.tz_convert(timezone_convert_to)  
                except(KeyError):
                    dataset_df[c] = pd.to_datetime(dataset_df[c],format=timestamp_format)
            else:                   
                dataset_df[c] = pd.to_datetime(dataset_df[c], errors="coerce")

        dataset_df.fillna(pd.NA, inplace=True)        
        
        if "MASK" in dataset_specs:
            maskcols = dataset_specs["MASK"]
            for col in maskcols:
                dataset_df[col] = dataset_df[col].apply(
                    lambda s: sha1(str.encode(str(s))).hexdigest() if s != '' else None
                )        

        pyarrow_schema = dataset_specs["PYARROW_SCHEMA"]
        schema_fields = []
         
        for field in pyarrow_schema:
            field_nullable = True
            if type(pyarrow_schema[field]) == list:
                field_type = pyarrow_schema[field][0]
                if len(pyarrow_schema[field]) >= 3:
                    field_nullable = True if pyarrow_schema[field][2] != "non-nullable" else False
            else:
                field_type = pyarrow_schema[field]

            field_metadata = {}

            if field_type == "timestamp[s, tz=Asia/Kuala_Lumpur]":
                field_type = pa.timestamp("s", tz="Asia/Kuala_Lumpur")
            elif field_type == "timestamp[ns, tz=Asia/Kuala_Lumpur]":
                field_type = pa.timestamp("ns", tz="Asia/Kuala_Lumpur")
            elif field_type.startswith("["):
                # categorical
                categorical_colspec = field_type[1:-1].split(',')
                if ":" in categorical_colspec[0]:
                    categorical_colspec = { k.split(":")[0].strip(): k.split(":")[1].strip()
                         for k in categorical_colspec }
                    field_type = pa.field(field, pa.dictionary(pa.int64(), pa.string()))
                    field_metadata = {'description':json.dumps(categorical_colspec)}
                else:
                    categorical_colspec = [ k.strip() for k in categorical_colspec ]
                    field_type = pa.dictionary(pa.int64(), pa.string())
                    field_metadata = {'description':json.dumps(f"{len(categorical_colspec)} categories")}

                dataset_df[field] = dataset_df[field].fillna(pd.NA)
                dataset_df[field] = convertCategoricals(dataset_df[field], field, categorical_colspec)

            if field_metadata != {}:
                schema_fields.append(pa.field(field, field_type, 
                nullable=field_nullable,
                metadata=field_metadata))
            else:
                schema_fields.append(pa.field(field, field_type, nullable=field_nullable))

        for field in pyarrow_schema:
            if type(pyarrow_schema[field]) == list:
                test_flags = pyarrow_schema[field][3:]
                for test in test_flags:
                    if test == "TEST_UNIQUE":
                        assert dataset_df[field].is_unique, f"Column {field} not unique."
            else:
                continue

        common_schema = pa.schema(schema_fields)
        schema = pa.schema([common_schema.field(c) for c in dataset_df.columns])
        tbl = pa.Table.from_pandas(dataset_df, preserve_index=False)
        tbl = tbl.cast(schema)        

        if not testonly:
            if partition is None:
                if not os.path.exists(structured_zone):
                    os.makedirs(structured_zone)
                pq.write_table(tbl, structured_zone_file, version="2.6")
            else:
                if not os.path.exists(os.path.join(structured_zone, dataset)):
                    os.makedirs(os.path.join(structured_zone, dataset))
                pq.write_table(tbl, structured_zone_file, version="2.6")
                pq.write_metadata(common_schema, os.path.join(structured_zone, dataset, "_common_metadata"))
        else:
            print("Converted dataset not saved as test flag is set.")

        if "DATASET_TESTS" in dataset_specs:
            for dataset_test in dataset_specs["DATASET_TESTS"]:
                if dataset_test == "ROW_COUNT":
                    raw_zone_file_rowcount = sum(1 for _ in open(raw_zone_file))
                    if not test:
                        structured_zone_file_rowcount = pq.read_metadata(structured_zone_file).num_rows
                    else:
                        structured_zone_file_rowcount = len(dataset_df)
                    assert raw_zone_file_rowcount-1 == structured_zone_file_rowcount
        
        

# convert categoricals
def convertCategoricals(col, colname, colspec):
    try:
        if col.dtypes == pd.Int64Dtype():
            placeholders = {int(e) for i, e in enumerate(colspec) if e==str(i)}
            non_placeholders = set(range(len(colspec))) - placeholders
            diff = set(col) - non_placeholders - set([pd.NA])
        
            if diff != set():
                raise ValueError(f'Contains unregistered or invalid categorical values in column {colname}: {diff}')
            s = pd.Categorical.from_codes(col.fillna(-1), categories=colspec)
            return s
    except(TypeError):
        pass
    
    diff = set(col) - set(colspec) - set([pd.NA])
    if diff != set():
        raise ValueError(f'Contains unregistered or invalid values in column {colname}: {diff}')
    else:
        s = pd.Categorical(col.fillna(-1), categories=colspec)
        return s
