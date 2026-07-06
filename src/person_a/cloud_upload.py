"""
cloud_upload.py - Load data/clean_data.csv directly into BigQuery.

Prerequisites:
    - Google Cloud SDK authenticated (gcloud auth application-default login)
      OR a service account JSON key set via GOOGLE_APPLICATION_CREDENTIALS env var.
    - A GCP project with the BigQuery API enabled.
    - GCP_PROJECT_ID set in the project .env file.

Usage:
    python -m src.person_a.cloud_upload
    # or:
    python src/person_a/cloud_upload.py
"""

import os
import sys

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Load environment variables from .env
from dotenv import load_dotenv

load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
CLEAN_CSV = os.path.join(_PROJECT_ROOT, "data", "clean_data.csv")
BQ_DATASET = "loan_underwriting"
BQ_TABLE = "loan_applicants"


def main():
    # ------------------------------------------------------------------
    # 1. Validate prerequisites
    # ------------------------------------------------------------------
    gcp_project_id = os.environ.get("GCP_PROJECT_ID")
    if not gcp_project_id:
        print(
            "[cloud] [ERROR] GCP_PROJECT_ID is not set.\n"
            "       Add it to your .env file or export it:\n"
            "         GCP_PROJECT_ID=my-project-id"
        )
        sys.exit(1)

    if not os.path.exists(CLEAN_CSV):
        print(
            f"[cloud] [ERROR] CSV file not found at {CLEAN_CSV}\n"
            "       Run clean_data.py first to generate it."
        )
        sys.exit(1)

    # ------------------------------------------------------------------
    # 2. Upload to BigQuery
    # ------------------------------------------------------------------
    try:
        
        from google.cloud import bigquery
        from google.api_core.exceptions import NotFound

        client = bigquery.Client(project=gcp_project_id)

        # -- Ensure dataset exists -------------------------------------
        dataset_ref = client.dataset(BQ_DATASET)
        try:
            client.get_dataset(dataset_ref)
            print(f"[cloud] Using existing BigQuery dataset: {BQ_DATASET}")
        except NotFound:
            print(f"[cloud] Creating BigQuery dataset: {BQ_DATASET}")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            client.create_dataset(dataset)

        # -- Load CSV directly into BigQuery ---------------------------
        table_id = f"{gcp_project_id}.{BQ_DATASET}.{BQ_TABLE}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition="WRITE_TRUNCATE",
        )

        print(f"[cloud] Loading {CLEAN_CSV} -> BigQuery table {table_id} ...")

        with open(CLEAN_CSV, "rb") as csv_file:
            load_job = client.load_table_from_file(
                csv_file, table_id, job_config=job_config
            )

        # Wait for the load job to complete
        load_job.result()

        # Confirm row count
        table = client.get_table(table_id)
        print(f"[cloud] [OK] Loaded {table.num_rows:,} rows into {table_id}")

    except FileNotFoundError as e:
        print(f"[cloud] [ERROR] File not found: {e}")
        sys.exit(1)

    except ImportError:
        print(
            "[cloud] [ERROR] google-cloud-bigquery is not installed.\n"
            "       Run: pip install google-cloud-bigquery"
        )
        sys.exit(1)

    except Exception as e:
        error_msg = str(e).lower()
        if "credentials" in error_msg or "authentication" in error_msg or "auth" in error_msg:
            print(
                f"[cloud] [ERROR] Authentication failed: {e}\n"
                "       Run: gcloud auth application-default login\n"
                "       Or set GOOGLE_APPLICATION_CREDENTIALS to your service account key."
            )
        else:
            print(f"[cloud] [ERROR] BigQuery upload failed: {e}")
        sys.exit(1)

    print("\n[cloud] [OK] Cloud upload complete.")


if __name__ == "__main__":
    main()
