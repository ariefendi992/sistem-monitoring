from datetime import datetime
import pytz
import time
import calendar


def utc_makassar():
    utc = pytz.timezone("Asia/Makassar")
    utc_mks = datetime.now(utc)

    return utc_mks


def today_():
    week_days = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
    local_time = time.localtime()
    today = local_time.tm_wday
    return week_days[today]


def tomorrow_():
    week_days = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
    local_time = time.localtime()
    tomorrow = local_time.tm_wday
    return week_days[tomorrow - 6] if tomorrow == 6 else week_days[tomorrow + 1]
    # return week_days[tomorrow + 1]


def day_now_indo():
    WEEKDAYSLIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    now = time.localtime()

    hari = WEEKDAYSLIST[now.tm_wday]
    tgl = now.tm_mday
    bulan = MONTHLIST[now.tm_mon - 1]
    tahun = now.tm_year
    format_indo = hari, tgl, bulan, tahun
    return format_indo


def day_in_date(date):
    return date.day


def format_indo(date: datetime):
    WEEKDAYSLIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    hari = WEEKDAYSLIST[date.weekday()]
    tgl = date.day
    bulan = MONTHLIST[date.month - 1]
    tahun = date.year
    format_indo = hari + ", " + str(tgl) + "-" + str(bulan) + "-" + str(tahun)
    return format_indo


def format_indo_non_weekday(date):
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    tgl = date.day
    bulan = MONTHLIST[date.month - 1]
    tahun = date.year
    format_indo = (
        (str(tgl) if len(str(tgl)) == 2 else "0" + str(tgl))
        + " "
        + bulan
        + " "
        + str(tahun)
    )
    return format_indo


def format_datetime_id(datetime):
    WEEKDAYSLIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    hari = WEEKDAYSLIST[datetime.weekday()]
    tgl = datetime.day
    bulan = MONTHLIST[datetime.month - 1]
    tahun = datetime.year
    hour = datetime.hour
    minute = datetime.minute
    second = datetime.second

    format_indo = (
        hari
        + ", "
        + str(tgl)
        + "-"
        + bulan
        + "-"
        + str(tahun)
        + " | "
        + f"{hour}:{minute}:{second}"
    )
    return format_indo


def format_date_today(datetime):
    WEEKDAYSLIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    hari = WEEKDAYSLIST[datetime.weekday()]
    tgl = datetime.day
    bulan = MONTHLIST[datetime.month - 1]
    tahun = datetime.year
    # hour = datetime.hour
    # minute = datetime.minute
    # second = datetime.second

    format_indo = hari + ", " + str(tgl) + "-" + bulan + "-" + str(tahun)
    return format_indo


def nama_bulan():
    MONTHLIST = (
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    )

    return MONTHLIST


def string_format(date_string):
    # mengambil nilai dari string 05-09-1992
    # konvert ke 1992-09-05
    # utk input ke database
    date = date_string.split("-")[0]
    month = date_string.split("-")[1]
    year = date_string.split("-")[2]

    format = year + "-" + month + "-" + date
    return format


def standart_date_format(date):
    pass
