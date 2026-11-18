
from datetime import date
import logging
import time

from data_fetcher import (
    fetch_sales,
    fetch_customers,
    fetch_products
)

from transform import (
    clean_data,
    calculate_weekly_aggregates,
    calculate_kpis,
    merge_datasets
)

from visualizer_export import export_results

# LOGIMISE SEADISTAMINE
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():

    start_time = time.time()

    logger.info("PIPELINE KÄIVITATUD")

    try:

        # ROLL A – EXTRACT

        print("\n1. ROLL A: ANDMETE PÄRIMINE")

        df_sales = fetch_sales(
            start_date="2023-01-01",
            end_date=date.today().isoformat()
        )

        df_customers = fetch_customers()
        df_products = fetch_products()

        if df_sales.empty:
            raise ValueError("Müügiandmed puuduvad!")

        print(f"Müügikirjeid: {len(df_sales)}")
        print(f"Kliente: {len(df_customers)}")
        print(f"Tooteid: {len(df_products)}")

        # ROLL B – TRANSFORM

        print("\n2. ROLL B: ANDMETE TÖÖTLEMINE")

        df_clean = clean_data(df_sales)

        if df_clean.empty:
            raise ValueError(
                "Puhastatud müügiandmed puuduvad!"
            )

        # Andmestike ühendamine
        df_merged = merge_datasets(
            df_clean,
            df_customers,
        )

        if df_merged.empty:
            raise ValueError(
                "Ühendatud andmed puuduvad!"
            )

        # Nädalapõhised koondandmed
        df_weekly = calculate_weekly_aggregates(
            df_merged
        )

        # KPI arvutamine
        kpis = calculate_kpis(df_merged)

        print("Andmed puhastatud!")
        print("Andmestikud ühendatud!")
        print("KPI-d arvutatud!")

        # ROLL C – VISUALIZATION + SAVING

        print(
            "\n3. ROLL C: VISUALISEERIMINE JA SALVESTAMINE"
        )

        export_results(
            df_merged,
            output_dir="output"
        )

        print("\nPIPELINE EDUKALT LÕPETATUD!")

        print(
            f"Kogukäive: {kpis['total_revenue']} €"
        )

        print(
            f"Unikaalsed kliendid: "
            f"{kpis['unique_customers']}"
        )

        print(
            f"Keskmine ost: "
            f"{kpis['avg_order_value']} €"
        )

        elapsed = round(
            time.time() - start_time,
            2
        )

        print(f"Tööaeg: {elapsed} sekundit")

        return True

    except Exception:

        logger.exception(
            "PIPELINE KÄIVITAMISEL TEKKIS VIGA"
        )

        raise


if __name__ == "__main__":

    run_pipeline()
