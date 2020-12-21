"""Модуль с классами для получения NER'ов"""
import re
from collections import namedtuple


class Match:
    """Класс для парсинга"""
    def __init__(self, new_span, new_text):
        self.span = new_span
        self.text = new_text


class Extractor():
    """Класс для парсинга"""
    def __init__(self):
        self.regex = ""

    def __call__(self, text):
        matches = []
        regex = re.compile(self.regex)
        for match in regex.finditer(text):
            matches.append(Match(match.span(), match.group()))
        return matches


class PhoneExtractor(Extractor):
    """Класс для парсинга номера телефона"""
    def __init__(self):
        super(PhoneExtractor, self).__init__()
        self.regex = r"((\+7|7|8|9)+(([0-9]){9,10}|\-[0-9]{3}\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}))"


class NumberExtractor(Extractor):
    """Класс для парсинга чисел"""
    def __init__(self):
        super(NumberExtractor, self).__init__()
        self.regex = r"\d+((.|,)\d+)?"


class PhotoExtractor(Extractor):
    """Класс для парсинга фоток"""
    def __init__(self):
        super(PhotoExtractor, self).__init__()
        self.regex = r"((https?://(www\.)?|www\.)[^\s'`]+)*jpg"


class ExtraDatesExtractor(Extractor):
    """Класс для парсинга дат по типу: <месяц>.<день>"""
    def __init__(self):
        super(ExtraDatesExtractor, self).__init__()
        self.regex = r"(0|1)?[0-9]\.[0-3][0-9]"


class StickerExtractor(Extractor):
    """Класс для парсинга стикеров"""
    def __init__(self):
        super(StickerExtractor, self).__init__()
        self.regex = r"((https?://(www\.)?|www\.)[^\s'`]+)*png"


class LinkExtractor(Extractor):
    """Класс для парсинга ссылок"""
    def __init__(self):
        super(LinkExtractor, self).__init__()
        self.regex = r"((https?://(www\.)?|www\.)[^\s'`]+)"


class TimeExtractor(Extractor):
    """Класс для парсинга ссылок"""
    def __init__(self):
        super(TimeExtractor, self).__init__()
        self.regex = r"[0-9]{1,2}\:[0-2][0-9]"


class CensorExtractor:
    """Класс для замены мата"""
    def __init__(self):
        self.Match = namedtuple('Match', ['span'])

    def __call__(self, text: str):
        trigger = '*censored*'
        if trigger not in text:
            return []
        utterance = text.index(trigger)
        span = [
            utterance,
            utterance + len(trigger)
        ]
        match = [self.Match(span=span)]

        return match
