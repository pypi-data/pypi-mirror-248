import pandas as pd
from pandas import DataFrame

from uw_file_processor_api.workflows.services.file_service import get_file_from_local
from uw_file_processor_api.workflows.services.processor_service import get_and_convert_file
from uw_file_processor_api.workflows.utils.dictionary import MONTHS_PT_BR


def mapper_data_to_process(mapper_func_name: str, path_file: str, content_type: str, path_save_parquet: str):
    if mapper_func_name is not None:
        if mapper_func_name in locals():
            locals()[func_name](path_file, content_type)
        else:
            raise Exception(f'Function {func_name} not found')


def mapper_data_client_iquine(df: DataFrame) -> DataFrame:
    # Transformando as colunas de datas em linhas
    df = df.melt(id_vars=['Codigo'], var_name='date', value_name='quantity')

    # Convertendo os nomes das datas para o formato 'AAAA-MM-DD'
    df['date'] = df['date'].apply(lambda x: f"20{x.split('_')[1]}-{MONTHS_PT_BR[x.split('_')[0]]}-01")
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Renomeando as colunas
    return df.rename(columns={'Codigo': 'product_id'})


def process_mapper_data_client_iquine(path_file: str, content_type: str,
                                      path_to_save_file: str = None, save_file: bool = False) -> DataFrame:
    file = get_file_from_local(path_file)

    df = get_and_convert_file(file, content_type)

    # Transformando as colunas de datas em linhas
    df = mapper_data_client_iquine(df)

    if save_file:
        if path_to_save_file is None:
            raise Exception('path to save file is required')

        df.to_parquet(path_to_save_file, engine='pyarrow', index=False)

    return df


if __name__ == "__main__":
    func_name = 'mapper_data_client_iquine'

    if func_name in locals():
        locals()[func_name]('/home/lffranca/Downloads/base_UP_OWL.xlsx',
                            'application/vnd.ms-excel')
