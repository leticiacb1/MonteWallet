import pandas as pd
import yfinance as yf

from typing import Optional
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

from logger import get_logger
from indexes import indexes


logger = get_logger('DATA LOADER')


def fetch_stock(
        ticker: str,
        start_date: Optional[str],
        end_date: Optional[str],
        path_to_save: Optional[str] = None,
        save: Optional[bool] = False
) -> pd.DataFrame:

    if not end_date:
        end_date = datetime.today().date()
        if not start_date:
            start_date = end_date - relativedelta(months=1)
            start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    elif not start_date:
        start_date = datetime.strptime(end_date, '%Y-%m-%d').date() - relativedelta(months=1)
        start_date = start_date.strftime('%Y-%m-%d')

    data = yf.Ticker(ticker)
    historical_data = data.history(start=start_date, end=end_date)

    if save:
        if not path_to_save:
            logger.warning('No path to save specified, skipping saving')
        else:
            path = Path(path_to_save)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f'Created directory {path}')

            filename = f"{ticker}_from_{start_date}_to_{end_date}.csv"
            file_path = path / filename
            historical_data.to_csv(file_path)
            logger.debug(f'Data saved to {file_path}')

    return historical_data


def read_data(path: Path) -> pd.DataFrame:

    if not path.exists():
        logger.warning(f'File {path} does not exist')
        return pd.DataFrame()

    if not path.is_file():
        logger.warning(f'Path {path} is not a file.')
        return pd.DataFrame()

    if path.suffix.lower() != '.csv':
        logger.warning(f'File {path} does not have a .csv extension.')
        return pd.DataFrame()

    logger.debug(f'Reading data from {path}')
    return pd.read_csv(path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--index', type=str, required=True)
    parser.add_argument('--start_date', type=str, required=True)
    parser.add_argument('--end_date', type=str, required=True)
    parser.add_argument('--save_path', type=str, required=True)

    args = parser.parse_args()

    ASSETS = indexes[args.index]

    for stock in ASSETS:
        logger.debug(f'Fetching data for {stock} from {args.start_date} to {args.end_date}')
        STORE = False
        if args.save_path:
            STORE = True
            logger.debug(f'Storing data at {args.save_path}')

        _ = fetch_stock(
            ticker=stock,
            start_date=args.start_date,
            end_date=args.end_date,
            path_to_save=args.save_path,
            save=STORE
        )
