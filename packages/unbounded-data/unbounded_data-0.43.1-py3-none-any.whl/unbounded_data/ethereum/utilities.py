import pandas as pd
from pandas import DataFrame


def sort_columns_lexi(data_frame: pd.DataFrame):
    """description: used to sort columns in a dataframe in the
                 lexicographical order.
    arguments: df - dataframe to be sorted
    returns:   dataframe with sorted columns
    """
    return data_frame.reindex(sorted(data_frame.columns), axis=1)


def handle_null_column(data_frame: DataFrame, column_name: str, default_value):
    """
    description:    used to fill NaNs of a column with a default value. If
                    column is does not exist in the dataframe, it is created
                    and populated with the default values.

    arguments:      data_frame - data frame with the null column
                    column_name - name of the column that has NaN values
                    default_value - default value to be used in place of NaN

    returns:        data frame with the populated column values
    """
    if column_name in data_frame.columns:
        data_frame[column_name] = data_frame[column_name].fillna(default_value)
    else:
        data_frame[column_name] = default_value

    return data_frame


def convert_column_to_float(data_frame: DataFrame, column_name: str):
    """
     description:   used to create a new column as a result of a conversion
                    of a string column to a float in a dataframe

    arguments:      data_frame - data frame wit the column to be converted
                    column_name - name of the column to be converted

    returns:        data frame with a new converted column
    """
    converted_column_name = column_name + "_float"
    data_frame[converted_column_name] = data_frame[column_name].astype("float")
    return data_frame


def convert_multiple_columns_to_float(
    data_frame: DataFrame, columns_list: list, drop_originals: bool = False
):
    """
     description:   used to create a new set of column as a result of a conversion
                    of columns based on provided list of columns names. Drops original
                    columns if needed.

    arguments:      data_frame - data frame wit the column to be converted
                    columns_list - names of the columns to be converted
                    drop_originals - indicates whether original columns (the
                    ones that are being converted) should be dropped.

    returns:        data frame with new converted columns
    """
    for column_name in columns_list:
        if column_name in data_frame.columns:
            data_frame = convert_column_to_float(data_frame, column_name)
            if drop_originals:
                data_frame = data_frame.drop(column_name, axis=1)

    return data_frame


def convert_column_to_timestamp(data_frame: DataFrame, column_name: str):
    """
     description:   used to convert a string column to a datetime
                    format in a dataframe.

    arguments:      data_frame - data frame wit the column to be converted
                    column_name - name of the column to be converted

    returns:        data frame with a new converted column
    """
    data_frame[column_name] = pd.to_datetime(data_frame[column_name])
    return data_frame


def convert_multiple_columns_to_timestamp(data_frame: DataFrame, columns_list: list):
    """
     description:   used to convert a set of string columns to a datetime
                    format in a dataframe.

    arguments:      data_frame - data frame wit the column to be converted
                    columns_list - names of the columns to be converted

    returns:        data frame with new converted columns
    """
    for column_name in columns_list:
        if column_name in data_frame.columns:
            data_frame = convert_column_to_timestamp(data_frame, column_name)

    return data_frame
