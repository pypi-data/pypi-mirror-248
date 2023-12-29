import io
from functools import reduce
import boto3

import pandas as pd
from pandas import DataFrame

from uw_file_processor_api.workflows.services.file_service import download_file_from_s3, get_file_metadata_from_s3
from uw_file_processor_api.workflows.configs.defines import BUCKET_PATH_RAW, BUCKET_PATH_PARSED, PARQUET_CONTENT_TYPE, \
    PARQUET_EXTENSION, \
    METADATA_CONTENT_TYPE
from uw_file_processor_api.workflows.utils.dictionary import MONTHS_PT_BR


class ProcessorService:
    _bucket_name: str
    _filename: str
    _extension: str

    def __init__(self, bucket_name: str, filename: str, extension: str):
        self._bucket_name = bucket_name
        self._filename = filename
        self._extension = extension

    def run_client_specific_script(self):
        file_key = f'{BUCKET_PATH_RAW}/{self._filename}.{self._extension}'

        file = download_file_from_s3(self._bucket_name, file_key)
        metadata = get_file_metadata_from_s3(self._bucket_name, file_key)
        df = get_and_convert_file(file, metadata[METADATA_CONTENT_TYPE])

        # TODO: run client specific script
        if 'job' in metadata.keys():
            func_name = metadata['job'].replace("-", "_")

            if func_name in locals():
                df = locals()[func_name](df)

        filepath_to_save = f'{BUCKET_PATH_PARSED}/{self._filename}.{PARQUET_EXTENSION}'

        file_parquet = df.to_parquet(None, engine='pyarrow', index=False)

        file_to_save = io.BytesIO(file_parquet)

        metadata[METADATA_CONTENT_TYPE] = PARQUET_CONTENT_TYPE
        metadata['key'] = filepath_to_save

        self._upload_file_to_s3(filepath_to_save, file_to_save, metadata)

    def send_item_to_process_kafka(self):
        file_key = f'{BUCKET_PATH_PARSED}/{self._filename}.{PARQUET_EXTENSION}'
        file = download_file_from_s3(self._bucket_name, file_key)
        metadata = get_file_metadata_from_s3(self._bucket_name, file_key)

    def save_attributes_to_filter_data(self):
        file_key = f'{BUCKET_PATH_PARSED}/{self._filename}.{PARQUET_EXTENSION}'
        file = download_file_from_s3(self._bucket_name, file_key)
        metadata = get_file_metadata_from_s3(self._bucket_name, file_key)

        df = pd.read_parquet(file, engine='pyarrow')

        base = df.groupby([pd.Grouper(freq='M', key='date'), 'product_id']).agg({'quantity': 'sum'}).sort_index()
        base = base.reset_index()

        start_date = base['date'].max() - pd.DateOffset(months=12)
        end_date = base['date'].max()

    def _upload_file_to_s3(self, file_key: str, file: io.BytesIO, metadata: dict = None):
        if self._bucket_name in [None, ''] or file_key in [None, '']:
            raise Exception('Invalid arguments')

        s3_client = boto3.client('s3')

        s3_client.put_object(Bucket=self._bucket_name, Key=file_key, Body=file, Metadata=metadata)


def uw_client_job_iquine_sales(df: DataFrame) -> DataFrame:
    # Transformando as colunas de datas em linhas
    df = df.melt(id_vars=['Codigo'], var_name='date', value_name='quantity')

    # Convertendo os nomes das datas para o formato 'AAAA-MM-DD'
    df['date'] = df['date'].apply(lambda x: f"20{x.split('_')[1]}-{MONTHS_PT_BR[x.split('_')[0]]}-01")
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Renomeando as colunas
    return df.rename(columns={'Codigo': 'product_id'})


# def process_file(path_file: str, content_type: str,
#                  path_save_parquet: str, columns_map: list[ColumnMapping]) -> DataFrame:
#     file = get_file_from_local(path_file)
#     df = _treating_column_map(file, content_type, path_save_parquet, columns_map)
#
#     return df


def get_and_convert_file(file: io.BytesIO, content_type: str) -> DataFrame:
    dfs = _get_dataframes_from_file(file, content_type)
    df = pd.concat(dfs).drop_duplicates().reset_index(drop=True)
    return df


class ColumnMapping:
    name: str
    alias: str
    column_type: str
    column_format: str

    def __init__(self, name: str, alias: str, column_type: str, column_format: str):
        self.name = name
        self.alias = alias
        self.column_type = column_type
        self.column_format = column_format


def _treating_column_map(file: io.BytesIO, content_type: str,
                         path_save_parquet: str, columns_map: list[ColumnMapping]) -> DataFrame:
    dfs = _get_dataframes_from_file(file, content_type)
    df = reduce(lambda df1, df2: df1.union(df2), dfs)

    if columns_map is not None:
        columns_alias = {column.name: column.alias for column in columns_map}
        df = df.rename(columns=columns_alias)
        columns_map_alias = {column.alias: column for column in columns_map}
        for column in df.columns:
            if column not in columns_map_alias.keys():
                df = df.drop(columns=[column])
                continue

            column_type = columns_map_alias[column].column_type
            column_format = columns_map_alias[column].column_format

            if column_type == 'datetime':
                df[column] = pd.to_datetime(df[column], format=column_format)
            elif column_type == 'int':
                df[column] = df[column].fillna(0).astype(int)
            elif column_type == 'float':
                df[column] = df[column].fillna(0).astype(float)
            elif column_type == 'string':
                df[column] = df[column].fillna('').astype(str)

    print('dataframe head:\n', df.head())

    if path_save_parquet is not None:
        df.to_parquet(path_save_parquet, engine='pyarrow', index=False)

    return df


def _get_dataframes_from_file(file: io.BytesIO, content_type: str) -> list[DataFrame]:
    if (content_type == 'application/vnd.ms-excel'
            or content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        file_excel = pd.ExcelFile(file, engine='openpyxl')

        dfs = []

        for index, sheet in enumerate(file_excel.sheet_names):
            df = file_excel.parse(sheet)

            dfs.append(df)

        return dfs
    elif content_type == "text/csv":
        df_data = _get_dataframe_from_csv(file)

        return [df_data]
    else:
        raise Exception('invalid content type')


def _get_dataframe_from_csv(file):
    for delimiter in [';', ',', '\t', '|']:
        aliases_to_try = ['utf-8', 'latin-1']

        for encoding in aliases_to_try:
            try:
                return pd.read_csv(file, sep=delimiter, encoding=encoding, header=None, skip_blank_lines=True,
                                   encoding_errors='ignore')
            except Exception as e:
                print(f'Error reading csv file: {e}')
                continue

    raise Exception('invalid csv file')
