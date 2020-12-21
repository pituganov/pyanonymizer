"""Модуль для предобработки текста"""
import re
import string
from typing import List

import pymorphy2
from tqdm import tqdm
from deeppavlov.core.models.component import Component
from natasha import (
    AddressExtractor,
    DatesExtractor,
    MoneyExtractor,
    NamesExtractor,
)
from nltk.corpus import stopwords

from pyanonymizer.ner import (
    CensorExtractor,
    TimeExtractor,
    ExtraDatesExtractor,
    LinkExtractor,
    NumberExtractor,
    PhoneExtractor,
    PhotoExtractor,
    StickerExtractor,
)

STOP_WORDS = [
    "доброе",
    "утро",
    "добрый",
    "день",
    "вечер",
    "пожалуйста",
    "подсказать",
    "сказать",
    "девушка",
    "мефодий",
    "спасибо",
] + stopwords.words("russian")
STOP_WORDS += ["не_" + x for x in STOP_WORDS]
STOP_WORDS += ["не"]

# местоимение-существительное, предлог, союз, частица, междометие
STOP_POS = ["NPRO", "PREP", "CONJ", "PRCL", "INTJ"]

CHAR_TABLE = str.maketrans(
    {
        key: " "
        for key in string.punctuation.replace("<", "").replace(">", "")
        + "…？‘«»‘♂️”“’[]'™"
    }
)
NERS = [
    (DatesExtractor(), "<date>"),
    (TimeExtractor(), "<time>"),
    (ExtraDatesExtractor(), "<date>"),
    (MoneyExtractor(), "<money>"),
    (PhoneExtractor(), "<phone>"),
    (PhotoExtractor(), "<photo>"),
    (StickerExtractor(), "<sticker>"),
    (LinkExtractor(), "<url>"),
    (AddressExtractor(), "<address>"),
    (NamesExtractor(), "<name>"),
    (NumberExtractor(), "<number>"),
    (CensorExtractor(), "<censored>"),
]


class EntityExtractor(Component):
    """Распознает именованные сущности"""

    def __init__(self, cache=None, verbose=False, **kwargs):
        super(EntityExtractor, self).__init__()
        self.kwargs = kwargs
        self.verbose = verbose

        self.cache = cache or {}
        self.extractors = NERS

    def iter_sample(self, text: str) -> str:
        """Заменяет именованные сущности на теги, итерируя по словам в тексте"""
        for extractor, tag in self.extractors:
            matches = extractor(text)
            while matches:
                match = matches[0]
                word = text[match.span[0] : match.span[1]]
                self.cache[word] = tag
                text = text[: match.span[0]] + tag + text[match.span[1] :]
                matches = extractor(text)
        return text

    def __call__(self, texts: List[str], *args, **kwargs) -> List[str]:
        """Возвращает текста с распознанными NER'ами"""
        if self.verbose:
            texts = tqdm(texts, desc="Ner", total=len(texts), ascii=True)
        return list(map(self.iter_sample, texts))
