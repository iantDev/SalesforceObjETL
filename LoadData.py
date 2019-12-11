from pathlib import Path
import logging
import psycopg2
import configSetting


def load_rest_result(data: dict, connection: dict) -> None:
    """
    :param data: dict, key = status_code, url, data:{ totalSize, done, [records] }; records[n]:{attributes, field_1:value ... field_n}

    """
    if data['data']['records']:
        records = data['data']['records']
    else:
        logging.error('No records in data variable. Rest result not loaded.')


def load_to_postgres(connection: dict, data):
    pass


def csv_to_postgres(connection: dict, file_path: str, field_list: list) -> None:
    pass


def data_to_csv(data, path: str, file_name: str, delimiter="|") -> None:
    """
    :param data: must be one of the data types in dict, list, set, tuple, or string.
    :param path: ex. /home/users
    :param file_name: ex. sf_[obj_name]_[yyyy_dd_mm]_n
    :param delimiter: default is " | "
    :return: None
    """
    # TODO: Validate path and avoid duplicate file_name
    anchor = Path.anchor
    file_path = f"{path}{anchor}{file_name}"
    output = ""
    for item in data:
        if isinstance(item, dict):
            output += f"{dict_to_line(item)}\n"
        elif isinstance(data, (list, set, tuple)):
            output += f"{iterable_to_line(item)}\n"
        elif isinstance(data, str):
            output += f"data\n"
        else:
            logging.error(
                f"Data element must be in string, list, dict, tuple, or set data type. Data is not output to {file_path}. Item = {str(item)}.")

    with open(file_path, 'w') as f:
        f.write(output)


def dict_to_line(item: dict, delimiter="|") -> str:
    return delimiter.join(str(v) for v in item.values())


def iterable_to_line(item, delimiter="|") -> str:
    if isinstance(item, (list, set, tuple)):
        return delimiter.join(item)
    else:
        logging.error("Item is not a data type of list, set, or tuple.")
        return ""
