"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.
    """
    import pandas as pd
    import zipfile
    from pathlib import Path

    input_path = Path("files/input")
    output_path = Path("files/output")
    output_path.mkdir(parents=True, exist_ok=True)

    # Leer todos los CSV comprimidos sin descomprimirlos
    df_list = []
    for zip_file in sorted(input_path.glob("bank-marketing-campaing-*.csv.zip")):
        with zipfile.ZipFile(zip_file) as z:
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                df_list.append(pd.read_csv(f))

    df = pd.concat(df_list, ignore_index=True)

    # ======================================================
    # CLIENT.CSV
    # ======================================================
    client = df[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage",
    ]].copy()

    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)

    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    client.to_csv(output_path / "client.csv", index=False)

    # ======================================================
    # CAMPAIGN.CSV
    # ======================================================
    campaign = df[[
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "day",
        "month",
    ]].copy()

    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # Crear fecha
    campaign["last_contact_date"] = pd.to_datetime(
        "2022-" + campaign["month"].astype(str) + "-" + campaign["day"].astype(str),
        format="%Y-%b-%d"
    ).dt.strftime("%Y-%m-%d")

    campaign = campaign.drop(columns=["day", "month"])

    campaign.to_csv(output_path / "campaign.csv", index=False)

    # ======================================================
    # ECONOMICS.CSV
    # ======================================================
    economics = df[[
        "client_id",
        "cons_price_idx",
        "euribor_three_months",
    ]].copy()

    economics.to_csv(output_path / "economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()

