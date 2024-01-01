MT5_ERROR_10012 = 10012
MT5_ERROR_10014 = 10014
MT5_ERROR_10015 = 10015
MT5_ERROR_10016 = 10016
MT5_ERROR_10017 = 10017
MT5_ERROR_10018 = 10018
MT5_ERROR_10019 = 10019
MT5_ERROR_10020 = 10020
MT5_ERROR_10023 = 10023
MT5_ERROR_10024 = 10024
MT5_ERROR_10025 = 10025
MT5_ERROR_10026 = 10026
MT5_ERROR_10027 = 10027

MT5_ERROR_10030 = 10030
MT5_ERROR_10031 = 10031
MT5_ERROR_10033 = 10033
MT5_ERROR_10034 = 10034
MT5_ERROR_10035 = 10035
MT5_ERROR_10036 = 10036
MT5_ERROR_10039 = 10039

ERROR_CODES = [
    MT5_ERROR_10012,
    MT5_ERROR_10014,
    MT5_ERROR_10015,
    MT5_ERROR_10016,
    MT5_ERROR_10017,
    MT5_ERROR_10018,
    MT5_ERROR_10019,
    MT5_ERROR_10020,
    MT5_ERROR_10023,
    MT5_ERROR_10024,
    MT5_ERROR_10025,
    MT5_ERROR_10026,
    MT5_ERROR_10027,
    MT5_ERROR_10030,
    MT5_ERROR_10030,
    MT5_ERROR_10031,
    MT5_ERROR_10033,
    MT5_ERROR_10034,
    MT5_ERROR_10035,
    MT5_ERROR_10036,
    MT5_ERROR_10039
]

ERROR_REASONS = {
    MT5_ERROR_10012: "Request cancelled by timeout",
    MT5_ERROR_10014: "Invalid Volume",
    MT5_ERROR_10015: "Invalid Price",
    MT5_ERROR_10016: "Invalid Stops in Request",
    MT5_ERROR_10017: "Trade is disabled",
    MT5_ERROR_10018: "Market Closed",
    MT5_ERROR_10019: "No Money",
    MT5_ERROR_10020: "Prices changed",
    MT5_ERROR_10023: "Order state changed",
    MT5_ERROR_10024: "Too many/frequent requests",
    MT5_ERROR_10024: "No change in request",
    MT5_ERROR_10026: "Autotrading disabled by Server",
    MT5_ERROR_10027: "Autotrading disabled by Client",
    MT5_ERROR_10030: "Unsupported Filling Mode",
    MT5_ERROR_10031: "No connection with trade server",
    MT5_ERROR_10033: "Pending order limit hit",
    MT5_ERROR_10034: "Volume limit for ticker hit",
    MT5_ERROR_10035: "Invalid order type",
    MT5_ERROR_10036: "Position closed already or does not exist",
    MT5_ERROR_10039: "Close order already exists",
}


def check_is_mt5_error(code: int):
    return code in ERROR_CODES
