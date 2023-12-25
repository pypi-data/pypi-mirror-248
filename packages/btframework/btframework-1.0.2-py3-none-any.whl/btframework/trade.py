import pandas as pd
from typing import Dict, Any, List
import btlib

WARNING = False


class Trade:
    def __init__(
        self,
        df: pd.DataFrame,
        entry_price: float,
        stop_loss: float,
        side: int,
        entry_time: str,
        squareoff_time: str,
        strike: str,
        expiry: str,
        signal_name: str = "",
        comment: str = "",
        stoploss_property: str = "C",
        qty: int = 1,
        target: float = 0,
    ) -> None:
        if df is not None:
            self.trade_df = df[(df["Date"] <= squareoff_time)]
        self.entry_price = entry_price
        self.stoploss = stop_loss
        self.entry_time = entry_time
        self.squareoff_time = squareoff_time
        self.exit_time: str = ""
        self.exit_price: float = 0
        self.strike = strike
        self.signal_name = signal_name
        self.comment = comment
        self.expiry = expiry
        self.in_trade: bool = True
        self.stoploss_property = stoploss_property
        self.side = side
        self.qty = qty
        self.target = target
        self.partials: List[Trade] = []
        self.validate_side()
        self.validate_stoploss_property()

    def validate_side(self):
        if self.side not in [1, -1]:
            print(
                f"warning: considering default side as -1 (sell). {self.side} is invalid"
            )
            self.side = -1

    def validate_stoploss_property(self):
        if self.stoploss_property not in ["HL", "C", "O"]:
            print(
                f"warning: considering default High/Low for stoploss calculation. {self.stoploss_property} is invalid"
            )
            self.stoploss_property = "HL"

        if self.stoploss_property == "C":
            self.stoploss_property = "Close"
        elif self.stoploss_property == "O":
            self.stoploss_property = "Open"
        else:
            if self.side == 1:
                self.stoploss_property = "Low"
            else:
                self.stoploss_property = "High"

    def get_curr_time_row(self, curr_dt: str):
        try:
            return self.trade_df[self.trade_df["Date"] == curr_dt].to_dict(
                orient="records"
            )[0]
        except:
            d = self.trade_df[self.trade_df["Date"] <= curr_dt].to_dict(
                orient="records"
            )[-1]
            if WARNING:
                print(
                    "missing candle, adjusting to last available candle",
                    self.strike,
                    curr_dt,
                    d["Date"],
                )
            return d

    def get_trade_df(self) -> pd.DataFrame:
        return self.trade_df

    def get_trade_details(self) -> Dict[str, Any]:
        return {**self.dict}

    def exit_trade(self, curr_dt: str, comment: str = "", property: str = ""):
        curr_row = self.get_curr_time_row(curr_dt)
        if self.in_trade:
            self.exit_time = btlib.add_time(curr_row["Date"], 1)
            self.exit_price = (
                curr_row["Close"]
                if property == ""
                else curr_row[property]  # Change to Open if executing on open values
            )
            self.in_trade = False
            self.comment = comment

    def check_stoploss(self, curr_dt: str, comment: str = ""):
        self.comment = comment
        curr_row = self.get_curr_time_row(curr_dt)
        if self.in_trade:
            if self.side == 1 and curr_row[self.stoploss_property] <= self.stoploss:
                self.exit_time = btlib.add_time(curr_row["Date"], 1)
                self.exit_price = (
                    curr_row["Close"]
                    if self.stoploss_property == "Close"
                    else self.stoploss
                )
                self.in_trade = False
            elif self.side == -1 and curr_row[self.stoploss_property] >= self.stoploss:
                self.exit_time = btlib.add_time(curr_row["Date"], 1)
                self.exit_price = (
                    curr_row["Close"]
                    if self.stoploss_property == "Close"
                    else self.stoploss
                )
                self.in_trade = False

    def check_target(self, curr_dt: str):
        curr_row = self.get_curr_time_row(curr_dt)
        if self.in_trade and self.target != 0:
            if self.side == 1 and curr_row[self.stoploss_property] >= self.target:
                self.exit_trade(curr_dt, comment="TARGET")
            elif self.side == -1 and curr_row[self.stoploss_property] <= self.target:
                self.exit_trade(curr_dt, comment="TARGET")

    def get_current_pnl(self, curr_dt: str) -> float:
        if self.in_trade:
            cmp = self.get_curr_time_row(curr_dt)["Close"]
        else:
            cmp = self.exit_price

        return (cmp - self.entry_price) * self.side * self.qty + sum(
            [p.get_current_pnl(curr_dt) for p in self.partials]
        )

    def exit_expiry(self, curr_dt: str):
        if (
            self.expiry == curr_dt.split("T")[0]
            and curr_dt >= f"{self.expiry}T15:25:00+0530"
        ):
            self.exit_trade(curr_dt, "EXPIRED")

    def create_partial_trade(self, qty):
        t = Trade(
            self.trade_df,
            self.entry_price,
            self.stoploss,
            self.side,
            self.entry_time,
            self.squareoff_time,
            self.strike,
            self.expiry,
            self.signal_name,
            self.comment,
            "C",
            qty,
            self.target,
        )
        return t

    def exit_partial(self, curr_dt: str, qty, comment: str = "", property: str = ""):
        if self.in_trade:
            if self.qty > qty:
                tr = self.create_partial_trade(qty)
                curr_row = tr.get_curr_time_row(curr_dt)
                tr.exit_time = btlib.add_time(curr_row["Date"], 1)
                tr.exit_price = (
                    curr_row["Close"]
                    if property == ""
                    else curr_row[
                        property
                    ]  # Change to Open if executing on open values
                )
                tr.in_trade = False
                tr.comment = comment
                self.qty = self.qty - qty
                self.partials.append(tr)
            else:
                self.exit_trade(curr_dt, comment, property)
