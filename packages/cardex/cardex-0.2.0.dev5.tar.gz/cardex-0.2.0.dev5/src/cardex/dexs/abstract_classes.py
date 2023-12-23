from abc import ABC
from abc import abstractmethod

from pycardano import Address
from pycardano import PlutusData
from pycardano import TransactionOutput

from cardex.dataclasses.models import Assets
from cardex.dataclasses.models import PoolSelector
from cardex.dexs.base_classes import BasePoolState
from cardex.utility import asset_to_value


class AbstractPoolState(ABC, BasePoolState):
    """A particular pool state, either current or historical."""

    datum_parsed: PlutusData | None = None

    @property
    @abstractmethod
    def pool_id(self) -> str:
        """A unique identifier for the pool.

        This is a unique string differentiating this pool from every other pool on the
        dex, and is necessary for dexs that have more than one pool for a pair but with
        different fee structures.
        """
        raise NotImplementedError("Unique pool id is not specified.")

    @classmethod
    @abstractmethod
    def dex(self) -> str:
        """Official dex name."""
        raise NotImplementedError("DEX name is undefined.")

    @classmethod
    @abstractmethod
    def pool_selector(self) -> PoolSelector:
        """Pool selection information."""
        raise NotImplementedError("DEX name is undefined.")

    @abstractmethod
    def get_amount_out(self, asset: Assets) -> tuple[Assets, float]:
        raise NotImplementedError("")

    @abstractmethod
    def get_amount_in(self, asset: Assets) -> tuple[Assets, float]:
        raise NotImplementedError("")

    @property
    @abstractmethod
    def swap_forward(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def inline_datum(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def stake_address(self) -> Address:
        raise NotImplementedError

    @property
    @abstractmethod
    def pool_datum_class(self) -> type[PlutusData]:
        raise NotImplementedError

    @property
    @abstractmethod
    def order_datum_class(self) -> type[PlutusData]:
        raise NotImplementedError

    @property
    def pool_datum(self) -> PlutusData:
        """The pool state datum."""
        if not self.datum_parsed:
            if not self.datum_cbor:
                raise ValueError("No datum specified.")
            self.datum_parsed = self.pool_datum_class.from_cbor(self.datum_cbor)

        return self.datum_parsed

    def swap_datum(
        self,
        address: Address,
        in_assets: Assets,
        out_assets: Assets,
        forward_address: Address | None = None,
    ) -> PlutusData:
        if self.swap_forward and forward_address is not None:
            print(f"{self.__class__.__name__} does not support swap forwarding.")

        return self.order_datum_class.create_datum(
            address=address,
            in_assets=in_assets,
            out_assets=out_assets,
            batcher_fee=self.batcher_fee,
            deposit=self.deposit,
            forward_address=forward_address,
        )

    def swap_utxo(
        self,
        address: Address,
        in_assets: Assets,
        out_assets: Assets,
        forward_address: Address | None = None,
    ):
        # Basic checks
        if len(in_assets) != 1 or len(out_assets) != 1:
            raise ValueError(
                "Only one asset can be supplied as input, "
                + "and one asset supplied as output.",
            )

        order_datum = self.swap_datum(
            address=address,
            in_assets=in_assets,
            out_assets=out_assets,
            forward_address=forward_address,
        )

        in_assets.root["lovelace"] = (
            in_assets["lovelace"]
            + self.batcher_fee.quantity()
            + self.deposit.quantity()
        )

        if self.inline_datum:
            output = TransactionOutput(
                address=self.stake_address,
                amount=asset_to_value(in_assets),
                datum=order_datum,
            )
        else:
            output = TransactionOutput(
                address=self.stake_address,
                amount=asset_to_value(in_assets),
                datum_hash=order_datum.hash(),
            )

        return output, order_datum


class AbstractConstantProductPoolState(AbstractPoolState):
    def get_amount_out(
        self,
        asset: Assets,
        precise: bool = True,
    ) -> tuple[Assets, float]:
        """Get the output asset amount given an input asset amount.

        Args:
            asset: An asset with a defined quantity.

        Returns:
            A tuple where the first value is the estimated asset returned from the swap
                and the second value is the price impact ratio.
        """
        assert len(asset) == 1, "Asset should only have one token."
        assert asset.unit() in [
            self.unit_a,
            self.unit_b,
        ], f"Asset {asset.unit} is invalid for pool {self.unit_a}-{self.unit_b}"

        if asset.unit() == self.unit_a:
            reserve_in, reserve_out = self.reserve_a, self.reserve_b
            unit_out = self.unit_b
        else:
            reserve_in, reserve_out = self.reserve_b, self.reserve_a
            unit_out = self.unit_a

        # Calculate the amount out
        fee_modifier = 10000 - self.volume_fee
        numerator: int = asset.quantity() * fee_modifier * reserve_out
        denominator: int = asset.quantity() * fee_modifier + reserve_in * 10000
        amount_out = Assets(**{unit_out: numerator // denominator})
        if not precise:
            amount_out.root[unit_out] = numerator / denominator

        if amount_out.quantity() == 0:
            return amount_out, 0

        # Calculate the price impact
        price_numerator: int = (
            reserve_out * asset.quantity() * denominator * fee_modifier
            - numerator * reserve_in * 10000
        )
        price_denominator: int = reserve_out * asset.quantity() * denominator * 10000
        price_impact: float = price_numerator / price_denominator

        return amount_out, price_impact

    def get_amount_in(
        self,
        asset: Assets,
        precise: bool = True,
    ) -> tuple[Assets, float]:
        """Get the input asset amount given a desired output asset amount.

        Args:
            asset: An asset with a defined quantity.

        Returns:
            The estimated asset needed for input in the swap.
        """
        assert len(asset) == 1, "Asset should only have one token."
        assert asset.unit() in [
            self.unit_a,
            self.unit_b,
        ], f"Asset {asset.unit} is invalid for pool {self.unit_a}-{self.unit_b}"
        if asset.unit == self.unit_b:
            reserve_in, reserve_out = self.reserve_a, self.reserve_b
            unit_out = self.unit_a
        else:
            reserve_in, reserve_out = self.reserve_b, self.reserve_a
            unit_out = self.unit_b

        # Estimate the required input
        fee_modifier = 10000 - self.volume_fee
        numerator: int = asset.quantity() * 10000 * reserve_in
        denominator: int = (reserve_out - asset.quantity()) * fee_modifier
        amount_in = Assets(**{unit_out: numerator // denominator})
        if not precise:
            amount_in.root[unit_out] = numerator / denominator

        # Estimate the price impact
        price_numerator: int = (
            reserve_out * numerator * fee_modifier
            - asset.quantity() * denominator * reserve_in * 10000
        )
        price_denominator: int = reserve_out * numerator * 10000
        price_impact: float = price_numerator / price_denominator

        return amount_in, price_impact


class AbstractStableSwapPoolState(AbstractPoolState):
    @property
    def amp(cls) -> Assets:
        return 75

    def _get_D(self) -> float:
        """Regression to learn the stability constant."""
        # TODO: Expand this to operate on pools with more than one stable
        N_COINS = 2
        Ann = self.amp * N_COINS**N_COINS
        S = self.reserve_a + self.reserve_b
        if S == 0:
            return 0

        # Iterate until the change in value is <1 unit.
        D = S
        for i in range(256):
            D_P = D**3 / (N_COINS**N_COINS * self.reserve_a * self.reserve_b)
            D_prev = D
            D = D * (Ann * S + D_P * N_COINS) / ((Ann - 1) * D + (N_COINS + 1) * D_P)

            if abs(D - D_prev) < 1:
                break

        return D

    def _get_y(self, in_assets: Assets, out_unit: str):
        """Calculate the output amount using a regression."""
        N_COINS = 2
        Ann = self.amp * N_COINS**N_COINS
        D = self._get_D()

        # Make sure only one input supplied
        if len(in_assets) > 1:
            raise ValueError("Only one input asset allowed.")
        elif in_assets.unit() not in [self.unit_a, self.unit_b]:
            raise ValueError("Invalid input token.")
        elif out_unit not in [self.unit_a, self.unit_b]:
            raise ValueError("Invalid output token.")

        in_quantity = in_assets.quantity() * (10000 - self.volume_fee) / 10000
        if in_assets.unit() == self.unit_a:
            in_reserve = self.reserve_a + in_quantity
        else:
            in_reserve = self.reserve_b + in_quantity

        S = in_reserve
        c = D**3 / (N_COINS**2 * Ann * in_reserve)
        b = S + D / Ann
        out_prev = 0
        out = D

        for i in range(256):
            out_prev = out
            out = (out**2 + c) / (2 * out + b - D)

            if abs(out - out_prev) < 1:
                break

        return Assets(**{out_unit: int(out)})

    def get_amount_out(self, asset: Assets) -> tuple[Assets, float]:
        out_unit = self.unit_a if asset.unit() == self.unit_b else self.unit_b
        out_asset = self._get_y(asset, out_unit)
        out_reserve = self.reserve_b if out_unit == self.unit_b else self.reserve_a
        out_asset.__root__[out_asset.unit()] = int(out_reserve - out_asset.quantity())
        return out_asset, 0

    def get_amount_in(self, asset: Assets) -> tuple[Assets, float]:
        in_unit = self.unit_a if asset.unit() == self.unit_b else self.unit_b
        asset[asset.unit] = -asset[asset.unit]
        in_asset = self._get_y(asset, in_unit)
        in_reserve = self.reserve_b if in_unit == self.unit_b else self.reserve_a
        in_asset.root[in_asset.unit()] = int(in_asset.quantity() - in_reserve)
        asset[asset.unit] = -asset[asset.unit]
        return in_asset, 0


class AbstractConstantLiquidityPoolState(AbstractPoolState):
    def get_amount_out(self, asset: Assets) -> tuple[Assets, float]:
        raise NotImplementedError("CLPP amount out is not yet implemented.")
        return out_asset, 0

    def get_amount_in(self, asset: Assets) -> tuple[Assets, float]:
        raise NotImplementedError("CLPP amount out is not yet implemented.")
        return out_asset, 0
