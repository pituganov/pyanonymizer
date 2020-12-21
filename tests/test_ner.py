"""Тесты для модуля предобработки текста

NOTE: Данные тесты не показывают качество распознавания.
      Они необходимы, чтобы отловить ошибки при изменении в предобработке.
"""
import pytest

from nlp_models.data.components.preprocessing import EntityExtractor

NERPreprocessor = EntityExtractor()


test_names = [
    (
        "Отрицал существование Иисуса и пророка Мухаммеда,",
        "Отрицал существование <name> и пророка <name>,",
    ),
    (
        "Хочу поблагодарить учителей моего Бушуева Вячеслава Владимировича",
        "Хочу поблагодарить учителей моего <name>",
    ),
    ("президент Николя Саркози", "президент <name>"),
    (
        "Вице-премьер правительства РФ Дмитрий Козак",
        "Вице-премьер правительства РФ <name>",
    ),
    ("Вице-президент Генадий Рушайло", "Вице-президент <name>"),
    (
        "Благодарственное письмо Хочу поблагодарить учителей:  "
        "Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну.",
        "Благодарственное письмо Хочу поблагодарить учителей:  "
        "<name> и <name>.",
    ),
    (
        "Иван, как именно выглядят помехи? Рябь или рассыпание на квадратики?",
        "<name>, как именно выглядят помехи? Рябь или рассыпание на квадратики?",
    ),
]

test_phone = [
    ("Мой телефон 88005553535", "Мой телефон <phone>"),
    ("Мой телефон +78005553535", "Мой телефон <phone>"),
    ("Мой телефон +7-800-555-35-35", "Мой телефон <phone>"),
]

test_sticker = [
    (
        "Я буду Вашим электронным помощником. "
        "https://image.ibb.co/d7Kd9b/3_2.png Что у Вас произошло?",
        "Я буду Вашим электронным помощником. "
        "<sticker> Что у Вас произошло?",
    ),
    (
        "мобильного приложенияhttps://image.ibb.co/bzGHsR/imgonline_com_ua_Transparent_backgr_i_Ec5d_Z485xsx_SVN.png",
        "мобильного приложения<sticker>",
    ),
    ("Всего доброго https://sticker.png", "Всего доброго <sticker>"),
]

test_photo = [
    ("Всего доброго https://sticker.jpg", "Всего доброго <photo>"),
]

test_url = [
    (
        "Всего доброго https://sticker.com/blabla. Всех благ.",
        "Всего доброго <url> Всех благ.",
    ),
    (
        "Со способами оплаты услуг нашей компании можно ознакомится по ссылке https://www.site.ru/home/pay/",
        "Со способами оплаты услуг нашей компании можно ознакомится по ссылке <url>",
    ),
    (
        "С тарифами можете ознакомится на нашем сайте www.site.ru",
        "С тарифами можете ознакомится на нашем сайте <url>",
    ),
]


test_money = [
    ("стоимость 1 доллара была около", "стоимость <money> была около"),
    (
        "стоимость была около 800 рублей 50 копеек",
        "стоимость была около <money>",
    ),
    (
        "стоимость была около 800 рублей и 50 рублей",
        "стоимость была около <money> и <money>",
    ),
    (
        "Я еще и должен суетиться за 20 рублей )))",
        "Я еще и должен суетиться за <money> )))",
    ),
    (
        "Платеж на следующий месяц  640,00 руб.",
        "Платеж на следующий месяц  <money>",
    ),
    (
        "оплачиваются только кабель - 15 руб/метр для интернета, и 10 руб/метр - телевизионный",
        "оплачиваются только кабель - <money>/метр для интернета, и <money>/метр - телевизионный",
    ),
    (
        "метр кабеля кабельного телевидения - 15 рублей, а  интернета - 20 рублей.",
        "метр кабеля кабельного телевидения - <money>, а  интернета - <money>.",
    ),
    (
        "К оплате 501 рублей.Сможете сейчас оплатить?",
        "К оплате <money>.Сможете сейчас оплатить?",
    ),
]


test_dates = [
    (
        "Подведем итог. Заявку назначили на 01.09, дома обязательно должен находиться кто-либо совершеннолетний.",
        "Подведем итог. Заявку назначили на <date>, дома обязательно должен находиться кто-либо совершеннолетний.",
    ),
    (
        "За ноябрь нужно будет внести в конце октября, до 1.11.",
        "За ноябрь нужно будет внести в конце октября, до <date>.",
    ),
    (
        "Я посмотрел на инфляцию в России, взял период с декабря 2002 года",
        "Я посмотрел на инфляцию в России, взял период с <date>",
    ),
    (
        "Ближайшая заявка есть на 03.01.2019, во сколько сможете встретить инженера?",
        "Ближайшая заявка есть на <date>, во сколько сможете встретить инженера?",
    ),
    (
        "Договор успешно приостановлен.Временное приостановление с 30.06.2019 до 31.07.2019",
        "Договор успешно приостановлен.Временное приостановление с <date> до <date>",
    ),
]


test_number = [
    (
        "дома обязательно должен находиться кто-либо 18-и летний.",
        "дома обязательно должен находиться кто-либо <number>-и летний.",
    ),
    ("стоимость была около 800", "стоимость была около <number>"),
    (
        "Мы можем приостановить действие Вашего договора на 1, 2 или 3 месяца, до 2 раз в год.",
        "Мы можем приостановить действие Вашего договора на <number>, <number> или <number> месяца, до <number> раз в год.",
    ),
]


test_address = [
    (
        "По этому адресу: ул. Ворошилова, д. 213 А, кв. 666, планируете установить видеотрубку?",
        "По этому адресу: <address>, планируете установить видеотрубку?",
    ),
    (
        "Ваш адрес: Челябинск, ул. Харлова, д. 19, кв. 167?",
        "Ваш адрес: <address>?",
    ),
    (
        "Интересует перенос услуг с ул. Братьев Кашириных, д. 68, кв. 222   ?",
        "Интересует перенос услуг с <address>   ?",
    ),
    (
        "Вы хотите перенести линию с этого адреса: ул. 410-летия Победы, д. 28, кв. 334?",
        "Вы хотите перенести линию с этого адреса: <address>?",
    ),
    (
        'Комсомольский пр-т, 38-б Остановка: Поликлиника (Комсомольский пр-т) ул.Труда, 1174 "Манхэттен" Остановка: ТРК Родник',
        '<address> Остановка: Поликлиника (Комсомольский пр-т) <address> "Манхэттен" Остановка: ТРК Родник',
    ),
    ("ул. Двинская, д. 21, кв. 31?", "<address>?"),
    (
        "Заявку оформил по адресу: Кыштым ул. Мичурина, д. 311, кв. 615. Если что-то изменится, пожалуйста, сообщите нам.",
        "Заявку оформил по адресу: Кыштым <address>. Если что-то изменится, пожалуйста, сообщите нам.",
    ),
]

test_censor = [("иди на *censored*", "иди на <censored>")]

test_time = [
    (
        "Ближайшая свободная заявка есть на завтра с 13:00 до 15:00.",
        "Ближайшая свободная заявка есть на завтра с <time> до <time>.",
    ),
    (
        "Тогда напишите нам в течение месяца, не завтра, с 9:00 до 20:00.",
        "Тогда напишите нам в течение месяца, не завтра, с <time> до <time>.",
    ),
    (
        "Время работы: 09:00-20:00Остановка: 5-й микрорайон",
        "Время работы: <time>-<time>Остановка: 5-й микрорайон",
    ),
]

# TODO: комбинированные тесты (когда в тексте несколько неров)

test_samples = (
    test_dates
    + test_money
    + test_address
    + test_names
    + test_number
    + test_phone
    + test_photo
    + test_sticker
    + test_url
    + test_censor
)


@pytest.mark.parametrize("raw,expected", test_samples)
def test_convert_numbers(raw: str, expected: str):
    """Тест на обработку именованных сущностей"""
    assert NERPreprocessor([raw])[0] == expected
