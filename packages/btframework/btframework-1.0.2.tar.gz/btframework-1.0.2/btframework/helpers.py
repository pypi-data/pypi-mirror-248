from datetime import datetime, timedelta
import zipfile
import pandas as pd
import numpy as np
import math
from ta.volume import volume_weighted_average_price
import psycopg2
import os
from dotenv import load_dotenv
import ast
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import openpyxl
import io
import btlib
import pandas as pd
from portfolio import Portfolio


load_dotenv()

pd.options.mode.chained_assignment = None

DBCONN = psycopg2.connect(
    host=os.environ["DB"],
    port=5432,
    database="historicaldata",
    user=os.environ["DBUSERNAME"],
    password=os.environ["DBUSERPWD"],
)

COLUMN_ORDER = [
    "date",
    "month",
    "year",
    "expiry",
    "strike",
    "entry_time",
    "entry_price",
    "sl",
    "exit_price",
    "exit_date",
    "exit_time",
    "pnl",
    "pnl_percent",
    "dd",
    "n",
    "signal",
    "day_type",
    "mfe",
    "mfe_date",
    "mae",
    "mae_date",
    "total",
    "ce_count",
    "pe_count",
    "s_count",
    "underlying",
    "qty",
    "hedge_cost",
    "hedge_strike",
    "comment",
    "underlying_range",
    "spot_val",
    "side",
    "c_rr",
    "c_max_rr",
    "c_stoploss",
]


def vwap(df: pd.DataFrame):
    def internal(df, row):
        df = df[df["Date"] <= row["Date"]]
        vwap = volume_weighted_average_price(
            df["High"], df["Low"], df["Close"], df["Volume"], window=len(df)
        )
        return vwap.values[-1]

    return df.apply(lambda row: internal(df, row), axis=1)


def time_to_dt(time: str, dt: str):
    return f"{dt}T{time}:00+0530"


def get_dte(dt: str, expiry: str):
    expiry = datetime.strptime(expiry, "%Y-%m-%d")
    dt = datetime.strptime(dt, "%Y-%m-%d")
    count = 0
    while True:
        if dt == expiry:
            return count
        expiry -= timedelta(days=1)
        count += 1


def get_strike_range(underlying):
    if underlying == "BANKNIFTY":
        return 100
    if underlying == "MIDCPNIFTY":
        return 25
    return 50


def straddle_supertrend(df: pd.DataFrame, a: int, b: int):
    df["HL"] = abs(df["High"] - df.shift(1)["High"])
    df["ATR"] = df["HL"].rolling(a).mean()
    df["STCURRDOWN"] = df["Close"] + df["ATR"] * b
    df["STCURRUP"] = df["Close"] - df["ATR"] * b
    df["STDOWN"] = 0.0
    df["STUP"] = 0.0

    df = df.fillna(0)
    last_dir = "down"
    for idx, row in df.iterrows():
        if idx == 0:
            continue

        try:
            if (
                row["STCURRDOWN"] < df.at[idx - 1, "STDOWN"]
                or df.at[idx - 1, "Close"] > df.at[idx - 1, "STDOWN"]
            ):
                df.at[idx, "STDOWN"] = row["STCURRDOWN"]
            else:
                df.at[idx, "STDOWN"] = df.at[idx - 1, "STDOWN"]
        except Exception as e:
            df.at[idx, "STDOWN"] = 0

        try:
            if (
                row["STCURRUP"] > df.at[idx - 1, "STUP"]
                or df.at[idx - 1, "Close"] < df.at[idx - 1, "STUP"]
            ):
                df.at[idx, "STUP"] = row["STCURRUP"]
            else:
                df.at[idx, "STUP"] = df.at[idx - 1, "STUP"]
        except Exception as e:
            df.at[idx, "STUP"] = 0

        if row["Close"] >= df.at[idx, "STDOWN"] and df.at[idx, "STDOWN"] != 0:
            last_dir = "up"
        if row["Close"] <= df.at[idx, "STUP"] and df.at[idx, "STUP"] != 0:
            last_dir = "down"
        df.at[idx, "STX"] = last_dir

    return df


def get_strike_from_name(f: str):
    f = f.lower()
    f = f.replace("banknifty", "").replace("nifty", "").replace("fin", "")
    return f[5:].upper()


def get_all_strikes(match: str, expiry: str, underlying: str):
    archive = zipfile.ZipFile(f"../data/{expiry}.zip", "r")

    req_file = [
        get_strike_from_name(f.filename.split("/")[-1].split(".csv")[0])
        for f in archive.filelist
        if f"/{underlying}/" in f.filename and match in f.filename
    ]

    req_file.sort()

    return req_file


def find_nearest_strike_ce(start_price, expiry, dt, underlying):
    cursor = DBCONN.cursor()
    query = f"SELECT strike FROM {underlying}_{expiry.replace('-', '')} WHERE date = '{dt}' AND optiontype = 'C' ORDER BY ABS(c - {start_price}) LIMIT 1"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return f"{rows[0][0]}CE"


def find_nearest_strike_pe(start_price, expiry, dt, underlying):
    cursor = DBCONN.cursor()
    query = f"SELECT strike FROM {underlying}_{expiry.replace('-', '')} WHERE date = '{dt}' AND optiontype = 'P' ORDER BY ABS(c - {start_price}) LIMIT 1"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return f"{rows[0][0]}PE"


def read_file_from_zip(expiry: str, strike: str, underlying: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_{expiry.replace('-', '')} WHERE strike = '{strike[:-2]}' AND optiontype = '{strike[-2]}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_specific_row(expiry: str, strike: str, underlying: str, dt: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_{expiry.replace('-', '')} WHERE strike = '{strike[:-2]}' AND optiontype = '{strike[-2]}' AND date = '{dt}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    if len(df) == 0:
        return read_specific_row(expiry, strike, underlying, add_time(dt, -1))
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_spot_from_db(underlying: str, startdate: str, enddate: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_spot where date <= '{(datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')}' and date >= '{startdate}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_fut_from_db(underlying: str, startdate: str, enddate: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_fut where date <= '{enddate}' and date >= '{startdate}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_spot_daily(underlying: str, startdate: str, enddate: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_spot_daily where date <= '{enddate}' and date >= '{startdate}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_fut_daily(underlying: str, startdate: str, enddate: str):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_fut_daily where date <= '{enddate}' and date >= '{startdate}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def read_options_from_db(
    underlying: str,
    startdate: str,
    enddate: str,
    expiry: str,
    strike: str,
):
    cursor = DBCONN.cursor()
    query = f"SELECT date, o, h, l, c, v, oi FROM {underlying}_{expiry.replace('-', '')} where date <= '{enddate}' and date >= '{startdate}' and strike = '{strike[:-2]}' and optiontype = '{strike[-2]}' order by date asc;"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OI"]
    df = pd.DataFrame(rows, columns=columns)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%dT%H:%M:%S+0530")
    df["Justdate"] = df["Date"].str.split("T").str[0]
    for c in columns[1:]:
        df[c] = df[c].astype(float)
    cursor.close()
    return df


def get_atm(curr_strike: int, range_strike: int) -> int:
    if range_strike == 100:
        return int(round(curr_strike, -2))
    if range_strike == 50:
        t = round(curr_strike, -2)
        if abs(curr_strike) % 100 > 50 and abs(curr_strike - t) % 50 > 25:
            return int(t - 50)
        elif abs(curr_strike - t) % 50 > 25:
            return int(t + 50)
        elif abs(curr_strike - t) % 50 == 0:
            return int(curr_strike)
        return int(t)
    return int(curr_strike)


def get_nearest_expiry(today, underlying):
    cursor = DBCONN.cursor()
    daylimit = (datetime.strptime(today, "%Y-%m-%d") + timedelta(days=7)).strftime(
        "%Y-%m-%d"
    )
    query = f"SELECT expiry FROM expiryinfo WHERE underlying = '{underlying}' AND expiry >= '{today}' AND expiry <= '{daylimit}' order by expiry asc limit 1;"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        print("no weekly expiry")
        return ""
    return rows[0][0]


def create_trade(
    et: str,
    ep: float,
    sl: float,
    exp: float,
    ext: str,
    strike: str,
    expiry: str,
    signal_type: str,
    underlying: str,
    qty: int,
    side: int,
    comment: str = "",
    c_rr: float = 0,
    c_max_rr: float = 0,
    c_stoploss: float = 0,
    **kwargs,
):
    return {
        "date": et.split("T")[0],
        "entry_time": et,
        "entry_price": ep,
        "sl": sl,
        "exit_price": exp,
        "exit_time": ext,
        "strike": strike,
        "expiry": expiry,
        "signal": signal_type,
        "day_type": "expiry" if et.split("T")[0] == expiry else "non-expiry",
        "underlying": underlying,
        "qty": qty,
        "comment": comment,
        "side": side,
        "c_rr": c_rr,
        "c_max_rr": c_max_rr,
        "c_stoploss": c_stoploss,
        **kwargs,
    }


def post_process(
    trades: pd.DataFrame,
):
    trades = trades.copy(deep=True)
    trades.round(2)
    trades["date"] = trades["entry_time"].str.split("T").str[0]
    trades["exit_date"] = trades["exit_time"].str.split("T").str[0]

    # Calculate s_count column
    trades["s_count"] = trades.apply(
        lambda x: f"{'pe_' if 'PE' in x['strike'] else 'ce_'}"
        f"{math.ceil(len(trades[(trades['date'] == x['date']) & (trades['entry_time'] <= x['entry_time']) & (trades['strike'].str.endswith(x['strike'][-2:]))]))}",
        axis=1,
    )

    trades["total"] = trades.apply(
        lambda x: len(trades[trades["date"] == x["date"]]), axis=1
    )

    only_time = []

    cols = trades.columns
    for idx, item in trades.iterrows():
        for col in cols:
            v = item[col]
            if type(v) == str and "T" in v and "+0530" in v:
                only_time.append(col)
        break

    for r in only_time:
        trades[r] = trades[r].str.split("T").str[1].str[:5]

    trades["year"] = trades["date"].str.split("-").str[0]
    trades["month"] = trades["date"].str.split("-").str[1]
    columns = [c for c in COLUMN_ORDER if c in trades.columns]
    trades = trades.loc[
        :,
        columns,
    ]
    return trades


def day_wise_trades(df: pd.DataFrame, slippage: float):
    ep = "entry_price"
    exp = "exit_price"
    side = "side"
    data = []
    dates = df["date"].unique()
    for d in dates:
        df_mini = df[df["date"] == d]
        pnl_condition = np.where(
            df_mini[side] == -1,
            (
                (
                    (df_mini[ep] * (1 - slippage / 100))
                    - (df_mini[exp] * (1 + slippage / 100))
                )
                * df_mini["qty"]
                * -df_mini["side"]
            ),
            (
                (
                    (df_mini[exp] * (1 - slippage / 100))
                    - (df_mini[ep] * (1 + slippage / 100))
                )
                * df_mini["qty"]
                * df_mini["side"]
            ),
        )
        data.append(
            {
                "date": d,
                "n": len(df_mini) / 2,
                # "pnl": (((df_mini[ep] * (1 - slippage / 100)) - (df_mini[exp] * (1 + slippage / 100))) * df_mini["qty"] * -df_mini["side"]).sum(),
                "pnl": pnl_condition.sum(),
            }
        )
    df = pd.DataFrame.from_dict(data)
    df.sort_values(by="date", inplace=True)
    df["dd"] = df["pnl"].cumsum() - df["pnl"].cumsum().cummax()
    return df


def add_time(t: str, min=1):
    return datetime.strftime(
        datetime.strptime(t, "%Y-%m-%dT%H:%M:%S%z") + timedelta(minutes=min),
        "%Y-%m-%dT%H:%M:%S%z",
    )


def process_time_str(t: str) -> datetime:
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S%z")


def create_format(
    trades_df,
    slippage,
    filename,
    underlying,
    calculate_mtm,
    in_rupees=False,
    buy_side=False,
    settings_file=None,
):
    summaries = []
    summaries.append(add_results(trades_df, slippage, "All"))

    day_wise = day_wise_trades(trades_df, slippage)
    summaries.append(add_results(day_wise, slippage, "Daywise"))

    expiry_trades = trades_df[trades_df["date"] == trades_df["expiry"]]
    if len(expiry_trades):
        summaries.append(add_results(expiry_trades, slippage, "ExpiryAll"))

        day_wise_expiry = day_wise_trades(expiry_trades, slippage)
        summaries.append(add_results(day_wise_expiry, slippage, "ExpiryDaywise"))

    non_exp = trades_df[trades_df["date"] != trades_df["expiry"]]
    if len(non_exp):
        summaries.append(add_results(non_exp, slippage, "Non-Expiry"))

        non_day_wise_expiry = day_wise_trades(non_exp, slippage)
        summaries.append(
            add_results(non_day_wise_expiry, slippage, "Non-ExpiryDaywise")
        )

    # Create a DataFrame for the summaries and daywise
    summaries_df = pd.DataFrame.from_dict(summaries)

    with pd.ExcelWriter(f"{filename}.xlsx") as writer:
        summaries_df.to_excel(
            writer, "summary", index=False
        )  # Write summaries to "summary" sheet

        # Write monthwise data after summaries
        d1m, d2m = divide_results_month_year(day_wise, buy_side, slippage, in_rupees)
        pd.DataFrame.from_dict(d1m).T.to_excel(
            writer, "summary", startrow=len(summaries_df) + 3
        )
        pd.DataFrame.from_dict(d2m).T.to_excel(
            writer, "summary", startrow=len(summaries_df) + len(d1m) + 6
        )

        d1d, d2d = divide_results_dayofweek(
            day_wise_trades(trades_df, slippage), buy_side, slippage, in_rupees
        )
        pd.DataFrame.from_dict(d1d).T.to_excel(
            writer, "summary", startrow=len(summaries_df) + len(d1m) + len(d2m) + 9
        )
        pd.DataFrame.from_dict(d2d).T.to_excel(
            writer,
            "summary",
            startrow=len(summaries_df) + len(d1m) + len(d2m) + len(d1d) + 12,
        )

        sheet = writer.sheets["summary"]
        fig = make_subplots(rows=2, cols=1)

        pnl_trace = go.Scatter(
            x=trades_df["date"],
            y=trades_df["pnl"].cumsum(),
            mode="lines",
            fill="tozeroy",
        )
        fig.add_trace(pnl_trace, row=1, col=1)
        fig.update_yaxes(title_text="Equity Curve", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=1)

        dd_trace = go.Scatter(
            x=trades_df["date"],
            y=trades_df["dd"],
            mode="lines",
            line=dict(color="red"),
            fill="tozeroy",
        )
        fig.add_trace(dd_trace, row=2, col=1)
        fig.update_yaxes(title_text="Drawdown", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)

        fig.update_layout(title="Plot", width=700, height=1000)
        combined_image_bytes = pio.to_image(fig, format="png")
        combined_image = openpyxl.drawing.image.Image(io.BytesIO(combined_image_bytes))
        combined_image.anchor = "P12"  # Adjust the anchor location as needed
        sheet.add_image(combined_image)

        post_process(trades_df).to_excel(writer, "trades")

        day_wise.to_excel(writer, "daywise")

        if len(expiry_trades):
            post_process(expiry_trades).to_excel(writer, "expiry")
            day_wise_expiry.to_excel(writer, "expiry-daywise")

        if len(non_exp):
            post_process(non_exp).to_excel(writer, "non-expiry")
            non_day_wise_expiry.to_excel(writer, "non-expiry-daywise")

        create_settings_dataframe("settings.py").to_excel(writer, "settings")

        trades_df.to_excel(writer, "original_trades")

    # autoresize columns
    try:
        from openpyxl.utils import get_column_letter

        writer = pd.ExcelWriter(f"{filename}.xlsx", mode="a")
        sheets = writer.sheets
        for s in sheets:
            for column_cells in writer.sheets[s].columns:
                length = max(len(str(cell.value)) for cell in column_cells) + 2
                writer.sheets[s].column_dimensions[
                    get_column_letter(column_cells[0].column)
                ].width = length

        writer.save()
    except:
        pass


def add_pnl_dd(trades: pd.DataFrame, buy_side, slippage, in_rupees):
    ep = "entry_price"
    exp = "exit_price"
    side = "side"

    # pnl = (((trades[ep] * (1 - slippage / 100)) - (trades[exp] * (1 + slippage / 100))) * trades["qty"] * -trades["side"])
    pnl = np.where(
        trades[side] == -1,
        (
            ((trades[ep] * (1 - slippage / 100)) - (trades[exp] * (1 + slippage / 100)))
            * trades["qty"]
            * -trades["side"]
        ),
        (
            ((trades[exp] * (1 - slippage / 100)) - (trades[ep] * (1 + slippage / 100)))
            * trades["qty"]
            * trades["side"]
        ),
    )

    if "hedge_cost" in trades.columns:
        hedge_cost = trades["hedge_cost"] * trades["qty"].values[0]
        pnl = pnl - hedge_cost

    return pnl.sum(), (pnl.cumsum() - pnl.cumsum().cummax()).min()


def add_results(
    trades: pd.DataFrame,
    slippage: float,
    name: str,
) -> dict:
    ep = "entry_price"
    exp = "exit_price"
    side = "side"

    if "pnl" not in trades.columns:
        # trades["pnl"] = (((trades[ep] * (1 - slippage / 100)) - (trades[exp] * (1 + slippage / 100))) * trades["qty"] * -trades["side"])
        trades["pnl"] = np.where(
            trades[side] == -1,
            (
                (
                    (trades[ep] * (1 - slippage / 100))
                    - (trades[exp] * (1 + slippage / 100))
                )
                * trades["qty"]
                * -trades["side"]
            ),
            (
                (
                    (trades[exp] * (1 - slippage / 100))
                    - (trades[ep] * (1 + slippage / 100))
                )
                * trades["qty"]
                * trades["side"]
            ),
        )

    if "entry_price" in trades.columns:
        trades["pnl_percent"] = trades["pnl"] * 100 / trades["entry_price"]

    # Group trades by date and calculate daily pnl
    daily_pnl = trades.groupby("date")["pnl"].sum()

    # Calculate EOD drawdown (dd) for daily pnl
    eod_dd = daily_pnl.cumsum() - daily_pnl.cumsum().cummax()

    # Assign the calculated EOD drawdown to a new column
    trades["dd_eod"] = trades["date"].map(eod_dd)

    trades["dd"] = trades["pnl"].cumsum() - trades["pnl"].cumsum().cummax()

    results = {
        "name": name,
        "trades": len(trades),
        "pnl": round(trades["pnl"].sum(), 2),
        "dd": round(trades["dd"].min(), 2),
        "dd_eod": round(trades["dd_eod"].min(), 2),
        "accuracy": round(len(trades[trades["pnl"] > 0]) / len(trades), 2),
        "avg_profit_pts": round(trades[trades["pnl"] > 0]["pnl"].mean(), 2),
        "avg_loss_pts": round(trades[trades["pnl"] < 0]["pnl"].mean(), 2),
    }
    results["Returns to MDD"] = round(results["pnl"] / -results["dd"], 2)
    results["Average RR"] = round(
        abs(results["avg_profit_pts"] / results["avg_loss_pts"]), 2
    )
    results["Expectancy"] = round(
        (results["accuracy"] * results["Average RR"]) - (1 - results["accuracy"]), 2
    )
    results["2019"] = trades[
        (trades["date"] >= "2019-01-01") & (trades["date"] < "2020-01-01")
    ]["pnl"].sum()
    results["2020"] = trades[
        (trades["date"] >= "2020-01-01") & (trades["date"] < "2021-01-01")
    ]["pnl"].sum()
    results["2021"] = trades[
        (trades["date"] >= "2021-01-01") & (trades["date"] < "2022-01-01")
    ]["pnl"].sum()
    results["2022"] = trades[
        (trades["date"] >= "2022-01-01") & (trades["date"] < "2023-01-01")
    ]["pnl"].sum()
    results["2023"] = trades[
        (trades["date"] >= "2023-01-01") & (trades["date"] < "2024-01-01")
    ]["pnl"].sum()

    if "hedge_cost" in trades.columns:
        results["hedge_cost"] = trades["hedge_cost"].sum() * trades["qty"].values[0]
        results["net"] = results["pnl"] - results["hedge_cost"]

    print(results)
    return results


def divide_results_month_year(trades: pd.DataFrame, buy_side, slippage, in_rupees):
    start_date = trades["date"].values[0]
    end_date = trades["date"].values[-1]
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    data_pnl = {}
    data_dd = {}

    while start_year <= end_year:
        yearwise = trades[
            (trades["date"] >= f"{start_year}-01-01")
            & (trades["date"] <= f"{start_year}-12-31")
        ]
        months = [i for i in range(1, 13)]
        data_pnl[start_year] = {}
        data_dd[start_year] = {}

        for m in months:
            curr = yearwise[yearwise["date"].str.split("-").str[1].astype(int) == m]
            if len(curr) != 0:
                if "entry_price" in curr.columns:
                    pnl, dd = add_pnl_dd(curr, buy_side, slippage, in_rupees)
                    data_pnl[start_year][m] = pnl
                    data_dd[start_year][m] = dd
                else:
                    pnl, dd = curr["pnl"].sum(), curr["dd"].min()
                    data_pnl[start_year][m] = pnl
                    data_dd[start_year][m] = dd
            else:
                data_pnl[start_year][m] = 0
                data_dd[start_year][m] = 0

        if len(yearwise) != 0:
            if "entry_price" in yearwise.columns:
                pnl, dd = add_pnl_dd(yearwise, buy_side, slippage, in_rupees)
                data_pnl[start_year][13] = pnl
                data_dd[start_year][13] = dd
            else:
                pnl, dd = yearwise["pnl"].sum(), yearwise["dd"].min()
                data_pnl[start_year][13] = pnl
                data_dd[start_year][13] = dd

        start_year += 1

    return data_pnl, data_dd


def divide_results_dayofweek(trades: pd.DataFrame, buy_side, slippage, in_rupees):
    start_date = trades["date"].values[0]
    end_date = trades["date"].values[-1]
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    data_pnl = {}
    data_dd = {}

    weekdays = [0, 1, 2, 3, 4]
    names = [0, 1, 2, 3, 4]
    while start_year <= end_year:
        yearwise = trades[
            (trades["date"] >= f"{start_year}-01-01")
            & (trades["date"] <= f"{start_year}-12-31")
        ]
        data_pnl[start_year] = {}
        data_dd[start_year] = {}
        yearwise["ndd"] = pd.to_datetime(yearwise["date"])
        for idx, m in enumerate(weekdays):
            curr = yearwise[yearwise["ndd"].dt.weekday == m]
            if len(curr) != 0:
                if "entry_price" in curr.columns:
                    pnl, dd = add_pnl_dd(curr, buy_side, slippage, in_rupees)
                    data_pnl[start_year][names[idx]] = pnl
                    data_dd[start_year][names[idx]] = dd
                else:
                    pnl, dd = curr["pnl"].sum(), curr["dd"].min()
                    data_pnl[start_year][m] = pnl
                    data_dd[start_year][m] = dd
            else:
                data_pnl[start_year][names[idx]] = 0
                data_dd[start_year][names[idx]] = 0
        start_year += 1
    return data_pnl, data_dd


def combine_tf(df: pd.DataFrame, tf: int or str) -> pd.DataFrame:
    dfs = []
    dates = df["Justdate"].unique()

    for d in dates:
        dm = df[df["Justdate"] == d]
        dm["NewDate"] = pd.to_datetime(dm["Date"])
        if isinstance(tf, int) and tf > 0:
            if 15 % tf != 0:
                dm["NewDate"] = dm["NewDate"] - pd.Timedelta(minutes=15)
            ohlc: pd.DataFrame = dm.resample(f"{tf}T", on="NewDate")
        elif isinstance(tf, str):
            ohlc: pd.DataFrame = dm.resample(tf, on="NewDate")
        else:
            raise ValueError("Invalid time frame value")

        agg_dict = {
            "Date": "first",
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum",
            "Justdate": "first",
        }
        ohlc: pd.DataFrame = ohlc.agg(agg_dict)
        ohlc.dropna(inplace=True)
        dfs.append(ohlc)

    df = pd.concat(dfs)
    df.index = [i for i in range(len(df))]
    return df


def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat(
        [df[:period][base].rolling(window=period).mean(), df[period:][base]]
    )

    if alpha == True:
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def ATR(df, period, ohlc=["open", "high", "low", "close"]):
    """
    Function to compute Average True Range (ATR)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = "ATR_" + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not "TR" in df.columns:
        df["h-l"] = df[ohlc[1]] - df[ohlc[2]]
        df["h-yc"] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df["l-yc"] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

        df["TR"] = df[["h-l", "h-yc", "l-yc"]].max(axis=1)

        df.drop(["h-l", "h-yc", "l-yc"], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, "TR", atr, period, alpha=True)

    return df


def SuperTrend(df, period, multiplier, ohlc=["Open", "High", "Low", "Close"]):
    """
    Function to compute SuperTrend
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = "ATR_" + str(period)
    st = "ST"  # + str(period) + '_' + str(multiplier)
    stx = "STX"  # + str(period) + '_' + str(multiplier)

    """
    SuperTrend Algorithm :
        BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
        BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                            THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LOWERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                    Current FINAL UPPERBAND
    """

    # Compute basic upper and lower bands
    df["basic_ub"] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df["basic_lb"] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    # Compute final upper and lower bands
    df["final_ub"] = 0.00
    df["final_lb"] = 0.00
    for i in range(period, len(df)):
        df["final_ub"].iat[i] = (
            df["basic_ub"].iat[i]
            if df["basic_ub"].iat[i] < df["final_ub"].iat[i - 1]
            or df[ohlc[3]].iat[i - 1] > df["final_ub"].iat[i - 1]
            else df["final_ub"].iat[i - 1]
        )
        df["final_lb"].iat[i] = (
            df["basic_lb"].iat[i]
            if df["basic_lb"].iat[i] > df["final_lb"].iat[i - 1]
            or df[ohlc[3]].iat[i - 1] < df["final_lb"].iat[i - 1]
            else df["final_lb"].iat[i - 1]
        )

    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = (
            df["final_ub"].iat[i]
            if df[st].iat[i - 1] == df["final_ub"].iat[i - 1]
            and df[ohlc[3]].iat[i] <= df["final_ub"].iat[i]
            else df["final_lb"].iat[i]
            if df[st].iat[i - 1] == df["final_ub"].iat[i - 1]
            and df[ohlc[3]].iat[i] > df["final_ub"].iat[i]
            else df["final_lb"].iat[i]
            if df[st].iat[i - 1] == df["final_lb"].iat[i - 1]
            and df[ohlc[3]].iat[i] >= df["final_lb"].iat[i]
            else df["final_ub"].iat[i]
            if df[st].iat[i - 1] == df["final_lb"].iat[i - 1]
            and df[ohlc[3]].iat[i] < df["final_lb"].iat[i]
            else 0.00
        )

        # Mark the trend direction up/down
    df[stx] = np.where(
        (df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), "down", "up"), np.NaN
    )

    # Remove basic and final bands from the columns
    df.drop(
        ["basic_ub", "basic_lb", "final_ub", "final_lb", "TR", f"ATR_{period}"],
        inplace=True,
        axis=1,
    )

    df.fillna(0, inplace=True)
    return df


def get_settings(settings_set):
    try:
        to_ignore = ["calculate_mtm", "atm_range", "output_filename"]
        settings = {}
        for name, values in vars(settings_set).items():
            if name.upper() == name:
                if name.lower() not in to_ignore:
                    settings[name] = str(values)
    except:
        return {}
    return settings


def import_settings_module(settings_file):
    import importlib

    module_name = "settings_module"  # Choose a unique module name
    spec = importlib.util.spec_from_file_location(module_name, settings_file)
    settings_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings_module)
    return settings_module


def create_settings_dataframe(settings_file_path):
    # Read the content of the settings file
    with open(settings_file_path, "r") as f:
        settings_content = f.read()

    # Create an AST (Abstract Syntax Tree) from the settings content
    settings_ast = ast.parse(settings_content)

    # Extract variable assignments from the AST
    settings_data = {}
    for node in ast.walk(settings_ast):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id

                    # Handle different types of node values
                    if isinstance(node.value, ast.Str):
                        var_value = node.value.s
                    elif isinstance(node.value, ast.Num):
                        var_value = node.value.n
                    elif isinstance(node.value, ast.List):
                        var_value = [
                            el.n if isinstance(el, ast.Num) else el.s
                            for el in node.value.elts
                        ]
                    else:
                        continue  # Skip unsupported types

                    settings_data[var_name] = var_value

    # Create a DataFrame from the settings data
    df = pd.DataFrame(settings_data.items(), columns=["Setting", "Value"])

    return df


def backtest(
    core_logic: callable,
    underlying: str,
    slip: float,
    output_fname: str,
    calculate_mtm: bool = False,
):
    portfolio: Portfolio = core_logic()
    trades = portfolio.get_all_trades()

    format_trades = []
    for t in trades:
        format_trades.append(
            btlib.create_trade(
                t["entry_time"],
                t["entry_price"],
                t["stoploss"],
                t["exit_price"],
                t["exit_time"],
                t["strike"],
                t["expiry"],
                t["signal_name"],
                underlying,
                t["qty"],
                t["side"],
                t["comment"],
            )
        )

    format_trades.sort(key=lambda x: x["entry_time"])
    trades_df = pd.DataFrame.from_dict(format_trades)

    btlib.create_format(trades_df, slip, output_fname, underlying, calculate_mtm)
