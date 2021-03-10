from csvObject import write_csv
import pandas as pd
import csv


def extract_headers(path):
    """
    Extract the first row from the file and return it as a list
    """
    with open(path) as header_extract:
        csv_data = csv.reader(header_extract)
        for row in csv_data:
            return row


def write_chunks(csv_path, header_list, header_type, write_directory, file_name, chunk_size=1000):
    """
    This iterates through a section of a csv file by using the header_list to only uses certain columns and loads them
    in the type specified in header type.

    :param csv_path: Path to the csv you want to iterate through
    :param header_list: Headers you want to extract from the master csv file
    :param header_type: The type of each column
    :param chunk_size: The number of rows you want to chunk load at a time
    :param write_directory: Write directory
    :param file_name: Write Name
    :return: Nothing, write out the file and then stop.
    """
    row_data = []
    for index, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size, usecols=header_list, dtype=header_type)):
        print((index + 1) * chunk_size)

        raw_list = [chunk[header].to_list() for header in header_list]
        transposed_list = [[row[i] for row in raw_list] for i in range(len(raw_list[0]))]
        for row in transposed_list:
            row_data.append(row)

    write_csv(write_directory, file_name, header_list, row_data)
    print(f"Finished writing {file_name}")