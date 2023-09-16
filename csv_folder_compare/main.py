import logging
import csv
from pathlib import Path

try:
    from csv_folder_compare.parse_args import app_arg
except ImportError:
    from parse_args import app_arg

logger: logging


def csv_compare(input1_data: dict, input2_data: list[str]) -> list[str]:
    # calculate common keys of data
    input1_data_keys = set(input1_data.keys())
    input2_data_keys = set(input2_data)
    intersection_21 = input2_data_keys.intersection(input1_data_keys)
    # print(intersection_21)
    return list(intersection_21)


def get_folder_data(input_folder: Path) -> list[str]:
    result = []
    if input_folder.is_dir():
        result = [item.stem for item in input_folder.glob("*.*")]
    return result


def get_csv_data(
    input_file: Path, key_index: int = 0, delimiter=",", encoding="utf-8-sig"
) -> tuple[list[str], dict[str, list[str]]]:
    input_data: dict[str, list[str]] = {}
    input_header: list[str] = []
    if input_file.is_file():
        with input_file.open(newline="", encoding=encoding) as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            try:
                while not (input_header := next(reader)):
                    logger.info(f"reread csv header: {input_header}")
                key: str = ""
                try:
                    for row in reader:
                        if row:
                            key = Path(row[key_index]).stem
                            input_data[key] = row
                except IndexError:
                    logger.error(f"{input_file} key index error: {key_index}")
            except StopIteration:
                logger.error(f"Is empty '{input_file}' ?")
    else:
        logger.error(f"File {input_file} is not found")
    return input_header, input_data


def save_result_csv(
    input_header: list[str],
    input_data: dict,
    keys: list[str],
    output: Path,
    delimiter=",",
    encoding="utf-8-sig",
):
    try:
        with output.open("w", newline="", encoding=encoding) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)
            writer.writerow(input_header)
            for key in keys:
                writer.writerow(input_data[key])
    except OSError as e:
        logger.error(f"Output data is not saved to a file: '{output}', error: {e}")
    else:
        logger.info(f"Output data is saved to a file: '{output}'")


def csv_operation(input1: Path, input2: Path, output: Path, idx1: int = 0):
    input1_header: list[str]
    input1_data: dict[str, list[str]]
    input2_header: list[str]
    input2_data: list[str]
    input1_header, input1_data = get_csv_data(input1, key_index=idx1)
    input1_data_keys = list(input1_data.keys())
    input2_data = get_folder_data(input2)

    if not input1_data or not input2_data:
        logger.error("Initial data are missing. Exit.")
        return
    else:
        input_1_k = input1_data_keys[:5]
        logger.info(f"input1 first 5 keys in list: {input_1_k}")
        input_2_k = input2_data[:5]
        logger.info(f"input2 first 5 keys in list: {input_2_k}")

    # print(input1_header, input1_data)
    # print(input2_header, input2_data)

    intersection_21 = csv_compare(input1_data, input2_data)
    # print(intersection_21)

    input1_records = len(input1_data_keys)
    input2_records = len(input2_data)
    output_records = len(intersection_21)
    report_txt = f"{input1_records=}, {input2_records=}, {output_records=}"
    logger.info(report_txt)
    if intersection_21:
        save_result_csv(input1_header, input1_data, intersection_21, output)
    else:
        logger.error("No output data. Nothing to save.")


def main():
    global logger
    args = app_arg()
    logging.basicConfig(
        level=logging.DEBUG if args.get("verbose") else logging.INFO,
        format="%(asctime)s  %(message)s",
    )
    logger = logging.getLogger(__name__)
    work_path = args.get("work")
    input1_path = args.get("input1")
    input2_path = args.get("input2")
    output_path = args.get("output")
    if not input1_path.is_absolute():
        input1_path = work_path.joinpath(input1_path)
    if not input2_path.is_absolute():
        input2_path = work_path.joinpath(input2_path)
    if not output_path.is_absolute():
        output_path = work_path.joinpath(output_path)
    input1_key_idx = args.get("input1_key_idx")

    csv_operation(input1_path, input2_path, output_path, input1_key_idx)


if __name__ == "__main__":
    main()
