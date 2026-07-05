"""
cloud_upload.py - Upload clean_data.csv to Google Cloud Storage (GCS)
and load it into a BigQuery table.

Prerequisites:
    - Google Cloud SDK authenticated (gcloud auth application-default login)
      OR a service account JSON key set via GOOGLE_APPLICATION_CREDENTIALS env var.
    - A GCP project with Storage and BigQuery APIs enabled.

Usage:
    python -m src.person_a.cloud_upload
    # or:
    python src/person_a/cloud_upload.py

Environment variables (override defaults):
    GCP_PROJECT_ID      - your GCP project ID
    GCS_BUCKET_NAME     - bucket name (will be created if it doesn't exist)
    BQ_DATASET          - BigQuery dataset name  (default: loan_underwriting)
    BQ_TABLE            - BigQuery table name     (default: loan_applicants)
"""

import os
import sys

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ---------------------------------------------------------------------
# Configuration (override via environment variables)
# ---------------------------------------------------------------------
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "loan-underwriting-data")
BQ_DATASET = os.environ.get("BQ_DATASET", "loan_underwriting")
BQ_TABLE = os.environ.get("BQ_TABLE", "loan_applicants")

CLEAN_CSV = os.path.join(_PROJECT_ROOT, "data", "clean_data.csv")
GCS_BLOB_NAME = "clean_data.csv"


def upload_to_gcs(local_path: str = CLEAN_CSV) -> str:
    """Upload a local CSV to GCS. Returns the gs:// URI."""
    from google.cloud import storage

    client = storage.Client(project=GCP_PROJECT_ID)

    # Create bucket if it doesn't exist
    bucket = client.bucket(GCS_BUCKET_NAME)
    if not bucket.exists():
        print(f"[cloud] Creating GCS bucket: {GCS_BUCKET_NAME}")
        bucket = client.create_bucket(GCS_BUCKET_NAME, location="US")
    else:
        print(f"[cloud] Using existing GCS bucket: {GCS_BUCKET_NAME}")

    blob = bucket.blob(GCS_BLOB_NAME)
    print(f"[cloud] Uploading {local_path} -> gs://{GCS_BUCKET_NAME}/{GCS_BLOB_NAME} ...")
    blob.upload_from_filename(local_path)

    gs_uri = f"gs://{GCS_BUCKET_NAME}/{GCS_BLOB_NAME}"
    print(f"[cloud] [OK] Upload complete: {gs_uri}")
    return gs_uri


def load_into_bigquery(gs_uri: str) -> None:
    """Load a CSV from GCS into a BigQuery table (auto-detect schema)."""
    from google.cloud import bigquery

    client = bigquery.Client(project=GCP_PROJECT_ID)

    # Create dataset if it doesn't exist
    dataset_ref = client.dataset(BQ_DATASET)
    try:
        client.get_dataset(dataset_ref)
        print(f"[cloud] Using existing BigQuery dataset: {BQ_DATASET}")
    except Exception:
        print(f"[cloud] Creating BigQuery dataset: {BQ_DATASET}")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)

    # Configure the load job
    table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,             # skip header row
        autodetect=True,                 # auto-detect schema from CSV
        write_disposition="WRITE_TRUNCATE",  # overwrite table if it exists
    )

    print(f"[cloud] Loading {gs_uri} -> BigQuery table {table_id} ...")
    load_job = client.load_table_from_uri(gs_uri, table_id, job_config=job_config)
    load_job.result()  # wait for completion

    table = client.get_table(table_id)
    print(f"[cloud] [OK] Loaded {table.num_rows:,} rows into {table_id}")


def main():
    if GCP_PROJECT_ID == "your-gcp-project-id":
        print("[cloud] [WARN]  Set GCP_PROJECT_ID env var before running this script.")
        print("[cloud]    export GCP_PROJECT_ID=my-project")
        sys.exit(1)

    if not os.path.exists(CLEAN_CSV):
        print(f"[cloud] [WARN]  Clean data not found at {CLEAN_CSV}")
        print("[cloud]    Run clean_data.py first.")
        sys.exit(1)

    gs_uri = upload_to_gcs()
    load_into_bigquery(gs_uri)
    print("\n[cloud] [OK] Cloud pipeline complete.")


if __name__ == "__main__":
    main()
