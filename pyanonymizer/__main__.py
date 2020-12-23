"""
Скрипт для анонимизации текстовых данных
"""
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from deeppavlov import build_model

ROOT_DIR = Path(__file__).resolve().parents[1]


def main(filename: Path, savepath: Path, column: int):
    """main"""
    preprocessor = build_model(f"{ROOT_DIR}/full_preprocessing.json")

    if "csv" in filename:
        data = pd.read_csv(filename, header=None)
    else:
        data = pd.read_excel(filename, header=None)

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
    args = parser.parse_args()
    main(args.filename, args.savepath, args.column - 1)
