from datetime import time
from itertools import chain

from pandas import Timestamp
from pandas.tseries.holiday import (
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
)
from pytz import UTC, timezone

from .trading_calendar import TradingCalendar
from trading_calendars.trading_calendar import HolidayCalendar
from trading_calendars.us_holidays import (
    Christmas,
    USIndependenceDay,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNationalDaysofMourning,
    USNewYearsDay,
)


class IEPAExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for ICE US (IEPA).

    Open Time: 8pm, America/New_York
    Close Time: 6pm, America/New_York

    https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf # noqa
    """

    name = "IEPA"

    tz = timezone("America/New_York")

    open_times = ((None, time(20, 1)),)

    close_times = ((None, time(18)),)

    @property
    def open_offset(self):
        return -1

    @property
    def special_closes(self):
        return [
            (
                time(13),
                HolidayCalendar(
                    [
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        USMemorialDay,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                    ]
                ),
            )
        ]

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                USNationalDaysofMourning,
                # ICE was only closed on the first day of the Hurricane Sandy
                # closings (was not closed on 2012-10-30)
                [Timestamp("2012-10-29", tz=UTC)],
            )
        )

    @property
    def regular_holidays(self):
        # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf # noqa
        return HolidayCalendar([USNewYearsDay, GoodFriday, Christmas])
