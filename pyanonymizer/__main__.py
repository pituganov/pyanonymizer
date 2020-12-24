"""
Скрипт для анонимизации текстовых данных
"""
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from deeppavlov import build_model

ROOT_DIR = Path(__file__).resolve().parents[1]


def main(filename: Path, savepath: Path, column: int, encoding: str, sep: str):
    """main"""
    preprocessor = build_model(f"{ROOT_DIR}/full_preprocessing.json")

    if "csv" in filename.suffix:
        data = pd.read_csv(filename, header=None, sep=sep, encoding=encoding)
    else:
        data = pd.read_excel(filename, header=None)

    print(data.columns)
    print(data.head(1))

    anon_text = preprocessor.batched_call(
        data[data.columns[column].astype(str)]
    )
    data[data.columns[column]] = anon_text

    data.to_excel(savepath, index=False)


if __name__ == "__main__":

    parser = ArgumentParser(__doc__)
    parser.add_argument("filename", type=Path, help="Путь до файла с текстами")
    parser.add_argument(
        "savepath", type=Path, help="Название файла для сохранения"
    )
    parser.add_argument(
        "--column",
        "-c",
        help="Номер столбца, который нужно анонимизировать",
        type=int,
    )
    parser.add_argument("--sep", help="Символ-разделитель", type=str)

    parser.add_argument(
        "--encoding", "-e", help="Кодировка", type=str, default="windows-1251"
    )
    args = parser.parse_args()
    main(
        args.filename, args.savepath, args.column - 1, args.encoding, args.sep
    )
