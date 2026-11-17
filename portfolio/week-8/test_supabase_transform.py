# Testime rollide A ja B koostööd Supabase'i andmetega

from data_fetcher import fetch_sales, fetch_customers

from transform import (
    clean_data,
    calculate_weekly_aggregates,
    calculate_kpis,
    merge_datasets
)

# Laeme andmed otse Supabase'ist
df_sales = fetch_sales("2023-01-01", "2026-06-28")
df_customers = fetch_customers()

# Kontrollime, et andmed saabusid
assert not df_sales.empty
assert not df_customers.empty

# Töötleme andmed roll B funktsioonidega
df_clean = clean_data(df_sales)
df_weekly = calculate_weekly_aggregates(df_clean)
kpis = calculate_kpis(df_clean)
df_merged = merge_datasets(df_clean, df_customers)

# Kuvame tulemused
print("Puhastatud müügiridu:", len(df_clean))
print("Nädalate arv:", len(df_weekly))
print("KPI-d:", kpis)
print("Ühendatud ridu:", len(df_merged))

# Kontrollime, et ühendamisel ei lisandunud ridu
assert len(df_merged) == len(df_clean)

print("Supabase'i ja roll B test edukalt läbitud!")