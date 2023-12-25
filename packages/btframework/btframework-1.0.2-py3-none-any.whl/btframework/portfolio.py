from typing import List
from trade import Trade
from enum import Enum


class POSTYPEFILTER(Enum):
    CE = "CE"
    PE = "PE"
    FUT = "FUT"
    EQ = "EQ"
    ALL = "ALL"
    OPT = "OPT"


class POSFILTER(Enum):
    CLOSE = 0
    OPEN = 1
    ALL = 2


class Portfolio:
    def __init__(self) -> None:
        self.pe_positions: List[Trade] = []
        self.ce_positions: List[Trade] = []
        self.fut_positions: List[Trade] = []
        self.eq_positions: List[Trade] = []
        self.trades: List[Trade] = []

    def get_pnl(
        self,
        curr_dt: str,
        typefilter: POSTYPEFILTER = POSTYPEFILTER.ALL,
        filter: POSFILTER = POSFILTER.ALL,
    ):
        positions = self.get_all_positions(typefilter, filter)
        pnl = sum([p.get_current_pnl(curr_dt) for p in positions])
        return pnl

    def add_position(self, trade: Trade, typefilter: POSTYPEFILTER):
        if typefilter == POSTYPEFILTER.CE:
            self.ce_positions.append(trade)
        if typefilter == POSTYPEFILTER.PE:
            self.pe_positions.append(trade)
        if typefilter == POSTYPEFILTER.FUT:
            self.fut_positions.append(trade)
        if typefilter == POSTYPEFILTER.EQ:
            self.eq_positions.append(trade)

    def get_all_positions(
        self,
        typefilter: POSTYPEFILTER = POSTYPEFILTER.ALL,
        filter: POSFILTER = POSFILTER.ALL,
    ) -> List[Trade]:
        positions: List[Trade] = []
        if typefilter == POSTYPEFILTER.ALL:
            positions = (
                self.pe_positions
                + self.ce_positions
                + self.fut_positions
                + self.eq_positions
            )
        if typefilter == POSTYPEFILTER.CE:
            positions = self.ce_positions
        if typefilter == POSTYPEFILTER.PE:
            positions = self.pe_positions
        if typefilter == POSTYPEFILTER.FUT:
            positions = self.fut_positions
        if typefilter == POSTYPEFILTER.EQ:
            positions = self.eq_positions
        if typefilter == POSTYPEFILTER.OPT:
            positions = self.ce_positions + self.pe_positions

        if filter == POSFILTER.ALL:
            return positions

        if filter == POSFILTER.OPEN:
            open_positions: List[Trade] = []
            for pos in positions:
                if pos.in_trade:
                    open_positions.append(pos)
            return open_positions

        if filter == POSFILTER.CLOSE:
            close_positions: List[Trade] = []
            for pos in positions:
                if not pos.in_trade:
                    close_positions.append(pos)

            return close_positions

    def get_all_trades(self) -> List[Trade]:
        return self.trades

    def flush(self) -> List[Trade]:
        if len(self.get_all_positions(filter=POSFILTER.OPEN)) != 0:
            print("warning: there are still some open positions")
        trades = self.get_all_positions(filter=POSFILTER.CLOSE)
        trades = [t.__dict__ for t in trades]
        for t in self.get_all_positions(filter=POSFILTER.CLOSE):
            for m in t.partials:
                trades.append(m.__dict__)
        self.trades.extend(trades)

        self.ce_positions.clear()
        self.pe_positions.clear()
        self.fut_positions.clear()
        self.eq_positions.clear()
        return trades
