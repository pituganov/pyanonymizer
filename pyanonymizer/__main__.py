"""
Скрипт для анонимизации текстовых данных
"""
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from deeppavlov import build_model

ROOT_DIR = Path(__file__).resolve().parents[1]


def main(
    filename: Path,
    savepath: Path,
    column,
    encoding: str,
    sep: str,
    verbose: bool,
):
    """main"""
    preprocessor = build_model(f"{ROOT_DIR}/full_preprocessing.json")

    try:
        column = int(column)
        column = column - 1
    except Exception:
        pass

    if "csv" in filename.suffix:
        data = pd.read_csv(
            filename,
            header="infer" if isinstance(column, int) else None,
            sep=sep,
            encoding=encoding,
        )
    else:
        data = pd.read_excel(filename, header=None)

    if isinstance(column, str):
        texts = data[data.columns[column]].astype(str)
    elif isinstance(column, int):
        texts = data[data.columns[column]].astype(str)

    if verbose:
        batch_size = 32
        anon_text = []
        for i in tqdm(range(0, len(texts), batch_size)):
            anon_text += preprocessor.batched_call(texts[i : i + batch_size])
    else:
        anon_text = preprocessor.batched_call(texts)
    data[data.columns[column]] = anon_text

    data.to_excel(savepath, index=False)


if __name__ == "__main__":

    parser = ArgumentParser(__doc__)
    parser.add_argument("filename", type=Path, help="Путь до файла с текстами")
    parser.add_argument(
        "savepath", type=Path, help="Название файла для сохранения"
    )
    parser.add_argument(
        "--column", "-c", help="Столбец, который нужно анонимизировать"
    )
    parser.add_argument("--sep", help="Символ-разделитель", type=str)

    parser.add_argument(
        "--encoding", "-e", help="Кодировка", type=str, default="windows-1251"
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Выводить доп информацию",
    )
    args = parser.parse_args()
    main(
        args.filename,
        args.savepath,
        args.column,
        args.encoding,
        args.sep,
        args.verbose,
    )
