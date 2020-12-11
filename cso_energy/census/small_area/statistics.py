from typing import Dict
from typing import List
from typing import Tuple

import pandas as pd

from prefect import Flow
from prefect import Parameter
from prefect import task


@task
def read_glossary(filepath: str) -> pd.DataFrame:

    return pd.read_excel(filepath, engine="openpyxl")


@task
def get_column_names_for_year(year: int) -> List[str]:

    glossary_columns_by_year = {
        2016: [
            "Tables Within Themes",
            "Column Names",
            "Description of Field",
            "GEOGID",
        ],
        2011: [
            "TABLES WITHIN THEMES",
            "FIELD NAME WITHIN SAPS TABLES",
            "DESCRIPTION OF FIELD",
            "GEOGID",
        ],
    }

    try:
        columns = glossary_columns_by_year[year]
    except KeyError:
        raise ValueError(f"{year} is either not a Census year or is not yet supported.")

    return columns


@task
def extract_rows_from_glossary(
    glossary: pd.DataFrame,
    table_names_column: str,
    table_name: str,
) -> pd.DataFrame:

    non_empty_rows = glossary[glossary[table_names_column].notna()].reset_index()

    # The relevant table rows always start one row above the table_name
    start_of_table = (
        non_empty_rows.query(f"`{table_names_column}` == '{table_name}'").index.item()
        - 1
    )
    next_non_empty_row: int = start_of_table + 2
    start_index: int = non_empty_rows.iloc[start_of_table]["index"]
    end_index: int = non_empty_rows.iloc[next_non_empty_row]["index"]

    return glossary.iloc[start_index:end_index].reset_index(drop=True)


@task
def convert_columns_to_dict(
    table: pd.DataFrame,
    encoded_names_column: str,
    decoded_names_column: str,
) -> Dict[str, str]:

    return (
        table[[encoded_names_column, decoded_names_column]]
        .set_index(encoded_names_column)
        .to_dict()[decoded_names_column]
    )


@task
def read_census(
    filepath: str,
    small_areas_column: str,
    table_mappings: Dict[str, str],
) -> pd.DataFrame:

    usecols = [small_areas_column] + list(table_mappings.keys())
    return pd.read_csv(filepath, usecols=usecols).rename(columns=table_mappings)


@task
def write_csv(filepath: str, df: pd.DataFrame) -> None:

    df.to_csv(filepath, index=False)


with Flow("Extract table from CSO Statistics Data") as flow:

    census_filepath = Parameter("census_filepath")
    glossary_filepath = Parameter("glossary_filepath")
    output_filepath = Parameter("output_filepath")
    year = Parameter("year")
    table_name = Parameter("table_name")

    column_names = get_column_names_for_year(year)
    table_names_column = column_names[0]
    encoded_names_column = column_names[1]
    decoded_names_column = column_names[2]
    small_areas_column = column_names[3]

    glossary_raw = read_glossary(glossary_filepath)
    table = extract_rows_from_glossary(
        glossary=glossary_raw,
        table_names_column=table_names_column,
        table_name=table_name,
    )
    table_mappings = convert_columns_to_dict(
        table=table,
        encoded_names_column=encoded_names_column,
        decoded_names_column=decoded_names_column,
    )
    census_table = read_census(
        filepath=census_filepath,
        small_areas_column=small_areas_column,
        table_mappings=table_mappings,
    )

    write_csv(output_filepath, census_table)
