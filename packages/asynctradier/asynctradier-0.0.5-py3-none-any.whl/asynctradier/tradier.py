from typing import List, Optional

from asynctradier.common import Duration, OptionOrderSide, OrderClass, OrderType
from asynctradier.common.order import Order
from asynctradier.common.position import Position
from asynctradier.exceptions import (
    InvalidExiprationDate,
    InvalidStrikeType,
    MissingRequiredParameter,
)
from asynctradier.utils.common import build_option_symbol, is_valid_expiration_date

from .utils.webutils import WebUtil


class TradierClient:
    def __init__(self, account_id: str, token: str, sandbox: bool = False) -> None:
        self.account_id = account_id
        self.token = token
        base_url = (
            "https://api.tradier.com" if not sandbox else "https://sandbox.tradier.com"
        )
        self.session = WebUtil(base_url, token)

    async def get_positions(self) -> List[Position]:
        url = f"/v1/accounts/{self.account_id}/positions"
        response = await self.session.get(url)
        positions = response["positions"]["position"]
        if response["positions"] == "null":
            positions = []
        if not isinstance(positions, list):
            positions = [positions]
        for position in positions:
            yield Position(
                **position,
            )

    async def get_order(self, order_id: str) -> Order:
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        params = {"includeTags": "true"}
        response = await self.session.get(url, params=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def buy_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        return await self._option_operation(
            OptionOrderSide.buy_to_open,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def sell_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        return await self._option_operation(
            OptionOrderSide.sell_to_close,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def _option_operation(
        self,
        side: OptionOrderSide,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)

        if not isinstance(strike, float) and not isinstance(strike, int):
            raise InvalidStrikeType(strike)

        if order_type == OrderType.limit and price is None:
            raise MissingRequiredParameter("Price must be specified for limit orders")

        if order_type == OrderType.stop and stop is None:
            raise MissingRequiredParameter("Stop must be specified for stop orders")

        url = f"/v1/accounts/{self.account_id}/orders"
        params = {
            "class": OrderClass.option.value,
            "symbol": symbol,
            "option_symbol": build_option_symbol(
                symbol, expiration_date, strike, option_type
            ),
            "side": side.value,
            "quantity": str(quantity),
            "type": order_type.value,
            "duration": order_duration.value,
            "tag": tag,
        }
        response = await self.session.post(url, data=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def cancel_order(self, order_id: str | int) -> None:
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        response = await self.session.delete(url)
        order = response["order"]
        return Order(
            **order,
        )
