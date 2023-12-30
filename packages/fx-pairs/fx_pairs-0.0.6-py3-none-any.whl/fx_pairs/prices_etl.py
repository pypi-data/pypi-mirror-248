import argparse
import logging
import os
import itertools
import pathlib
import importlib
import json

import arcticdb
import pandas as pd
import fx_pairs.prices as pxs
import yaml

import yfinance as yf

from trading_ig import IGService


ARCTIC_CONNECTION = (
    f"s3://s3.eu-west-2.amazonaws.com:tradingo-price-store?aws_auth=true"
)
ARCTIC_CONNECTION = os.environ.get('TRADINGO_ARCTIC_CONNECTION', "lmdb:///home/rory/.trading/.tradingo-db.test") #://s3.eu-west-2.amazonaws.com") # 
ARCTIC_CONNECTION = os.environ.get('TRADINGO_ARCTIC_CONNECTION', "lmdb:///home/rory/.trading/tradino-db") #://s3.eu-west-2.amazonaws.com") # 

#ARCTIC_CONNECTION = 's3://s3.eu-west-2.amazonaws.com:tradingo-price-store?aws_auth=true'

# TODO: Normalize all library name references
# TODO: Normalize all symbol references to be from fx_pairs.prices module


logger = logging.getLogger(__name__)


def iter_raw_prices(
        source: str,
        epics: list,
        resolution: str,
        start_date: pd.Timestamp,
        end_date: pd.Timestamp,
    ):

    if source == 'igtrading':
        from trading_ig.config import config
        logger.info("api_key=%s username=%s password=%s",
                config.api_key,
                config.username,
                config.password,
            )
        ig_service = IGService(
            config.username, config.password, config.api_key, config.acc_type
        )
        ig_service.create_session()

        get_prices = lambda epic: (ig_service.fetch_historical_prices_by_epic_and_date_range(
                epic=epic,
                resolution=resolution,
                end_date=end_date,
                start_date=start_date,
            )['prices'], ig_service.fetch_market_by_epic(epic))

    elif source == 'yahoo':

        def get_prices(epic):
            t = yf.Ticker(epic)
            pxs = t.history(start=start_date, end=end_date, period=resolution.lower())
            pxs.columns = [('Mid', c) for c in pxs.columns]

            meta = t.info

            return pxs, t.info

    else:
        raise ValueError(source)

    yield from map(get_prices, epics)


def extract(
    arctic,
    epics,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
    source='igtrading',
):

    lib = arctic.get_library(
        f"{source.upper()}_INSTRUMENTS_{resolution.upper()}",
        create_if_missing=True,
    )

    prices_iter = iter_raw_prices(
            source, epics, resolution, start_date, end_date,
        )

    for epic, (prices, meta) in zip(epics, prices_iter):

        prices.columns = [
            "_".join(i).lower() for i in prices.columns.to_series()
        ]

        lib.update(
            epic,
            prices,
            upsert=True,
            date_range=(start_date, end_date),
            metadata=dict(meta),
        )


def _iterfields(source, as_type='tuples'):

    if source == 'igtrading':
        it = itertools.chain(itertools.product(
                ("bid", "ask"), ("open", "close", "high", "low")
            ),
            #(('last', 'volume'),)
        )
    else:
        source == 'yahoo'
        it = itertools.chain(itertools.product(
                ("mid",), ("open", "close", "high", "low")
            ),
            #(('last', 'volume'),)
        )

    if as_type == 'tuples':
        return it

    if as_type == 'names':
        return map(_as_symbol_name, it)

    raise ValueError(as_type)


def _as_symbol_name(field: tuple):
    return '.'.join(field).upper()


def transform(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
    source='igtrading',
):
    in_lib = arctic.get_library(f"{source.upper()}_INSTRUMENTS_{resolution.upper()}")
    out_lib = arctic.get_library(
        f"{universe_name.upper()}_PRICE_{resolution.upper()}",
        create_if_missing=True,
        library_options=arcticdb.LibraryOptions(dedup=True),
    )

    for field, obvs in _iterfields(source):
        symbol = _as_symbol_name((field, obvs))

        out_df = pd.concat(
            (
                in_lib.read(
                    symbol,
                    columns=[f"{field}_{obvs}"],
                    date_range=(start_date, end_date),
                )
                .data.squeeze(axis="columns")
                .rename(symbol)
                for symbol in epics
            ),
            axis=1,
        )

        metadata = {"universe": epics, "universe_name": universe_name}

        out_lib.update(
            symbol,
            out_df,
            upsert=True,
            date_range=(start_date, end_date),
            metadata=metadata,
        )


def transform_derived(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
    obvs: str='CLOSE',
    source: str='igtrading',
):

    if source == 'igtrading':

        obvs = obvs.upper()
        lib = arctic.get_library(
            f"{universe_name.upper()}_PRICE_{resolution.upper()}",
        )

        bid = lib.read(f'BID.{obvs}', date_range=(start_date, end_date)).data
        ask = lib.read(f'ASK.{obvs}', date_range=(start_date, end_date)).data

        mid = (bid + ask)/2

        lib.write(getattr(pxs, f'{obvs}.MID'), mid)

    cash_returns(
        arctic,
        epics,
        universe_name,
        start_date,
        end_date,
        resolution,
        source,
    )


def cash_returns(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
    source: str='igtrading',
):

    lib = arctic.get_library(
        f"{universe_name.upper()}_PRICE_{resolution.upper()}",
    )

    insts = arctic.get_library(f'{source.upper()}_INSTRUMENTS_{resolution.upper()}')
    inst_specs = insts.read_metadata_batch(epics)
    close = lib.read(pxs.CLOSE_MID, date_range=(start_date, end_date)).data

    if source == 'igtrading':
        instruments = pd.DataFrame({i.metadata['instrument']['epic']: i.metadata['instrument'] for i in inst_specs}).transpose()

        one_pip = instruments['valueOfOnePip'].astype(float)

        returns = close.diff() * one_pip

    else:

        returns = close.diff()

    lib.write(pxs.CASH_RETURN, returns)


def load(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    resolution: str = "1D",
    source: str='igtrading',
):
    lib = arctic.get_library(f"{universe_name.upper()}_PRICE_{resolution.upper()}")

    data = {
        fld: lib.read(
            ".".join(fld).upper(),
            date_range=(start_date, end_date),
            columns=epics,
        ).data
        for fld in _iterfields(source)
    }
    return pd.concat(data.values(), keys=data.keys(), axis=1)


def cli_app():
    app = argparse.ArgumentParser("tradingo-price-etl")
    app.add_argument("actions", nargs="+")
    app.add_argument("--epics", required=False, nargs="+")
    app.add_argument("--universe-file", required=False, type=pathlib.Path)
    app.add_argument("--resolution", default="1D")
    app.add_argument(
        "--end-date", type=pd.Timestamp, default=pd.Timestamp.now()
    )
    app.add_argument("--start-date", type=pd.Timestamp)
    app.add_argument("--source", default='igtrading')
    app.add_argument("--universe-name", required=True)
    app.add_argument("--config", type=json.loads)

    return app


def backtest(
    arctic: arcticdb.Arctic,
    epics,
    universe_name: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    config: dict,
    resolution: str = "1D",
    diagnostics=None,
):

    diagnostics = {} if diagnostics is None else diagnostics

    logger.info(config)

    module = importlib.import_module(config['module_name'])

    library = arctic.get_library(f"{universe_name.upper()}_PRICE_{resolution}")

    diagnostics = {}

    config_name = f'{universe_name}.{config["model"]}.{config["instance"]}.{config["flavour"]}'
    lib = arctic.get_library(
            config_name,
            create_if_missing=True
        )

    try:

        positions, diagnostics = module.run(
                library=library,
                start_date=pd.Timestamp(start_date),
                end_date=end_date,
                config=config,
                resolution=resolution,
                diagnostics=diagnostics,
            )

    finally:

        log_diagnostics(lib, diagnostics, start_date, end_date, config)

    lib.update('MODEL_POSITION', positions, metadata=config, date_range=(start_date, end_date))


def log_diagnostics(lib, diagnostics, start_date, end_date, config):
    for field, data in diagnostics.items():
        lib.update(field, data, metadata=config, date_range=(start_date, end_date))


def load_config(filepath: pathlib.Path, args):
    universe_config = yaml.load(filepath.open("r"), yaml.Loader)

    logger.info(universe_config)

    if "epics" in universe_config:
        args.epics = universe_config["epics"]

    if "resolution" in universe_config:
        args.resolution = universe_config["resolution"]

    if "universe_name" in universe_config:
        args.universe_name = universe_config["universe_name"]

    if "config" in universe_config:
        args.config = universe_config["config"]

    if 'source' in universe_config:
        args.config = universe_config['source']

    return args


def main():

    args = cli_app().parse_args()

    if args.universe_file:

        args = load_config(args.universe_file, args)

    arctic = arcticdb.Arctic(ARCTIC_CONNECTION)

    for action in args.actions:
        if action == "extract":
            extract(
                arctic,
                epics=args.epics,
                start_date=args.start_date,
                end_date=args.end_date,
                resolution=args.resolution,
                source=args.source,
            )

        elif action == "transform":
            transform(
                arctic,
                epics=args.epics,
                start_date=args.start_date,
                universe_name=args.universe_name,
                end_date=args.end_date,
                resolution=args.resolution,
                source=args.source,
            )
            transform_derived(
                arctic,
                epics=args.epics,
                start_date=args.start_date,
                universe_name=args.universe_name,
                end_date=args.end_date,
                resolution=args.resolution,
                source=args.source,
            )

        elif action == "load":
            load(
                arctic,
                universe_name=args.universe_name,
                epics=args.epics,
                start_date=args.start_date,
                end_date=args.end_date,
                resolution=args.resolution,
                source=args.source,
            )

        elif action == "backtest":
            backtest(
                arctic,
                universe_name=args.universe_name,
                epics=args.epics,
                start_date=pd.Timestamp(args.config['start_date']),
                end_date=args.end_date,
                resolution=args.resolution,
                config=args.config,
            )

        else:
            raise ValueError(f"Invalid action {action}")


if __name__ == "__main__":
    main()
