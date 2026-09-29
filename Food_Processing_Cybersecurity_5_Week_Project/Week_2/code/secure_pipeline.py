"""Week 2: sample ingestion and validation pipeline using synthetic food-batch data."""
from pathlib import Path
import hashlib
import json
import pandas as pd

RAW = Path("sample_batches.csv")
OUT = Path("validated_batches.csv")
QUARANTINE = Path("quarantine_batches.csv")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

df = pd.read_csv(RAW)
required = {"batch_id", "product", "temperature_c", "supplier_id", "event_time"}
missing_cols = required - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required columns: {sorted(missing_cols)}")

df["temperature_valid"] = df["temperature_c"].between(-30, 100)
df["batch_id_valid"] = df["batch_id"].notna() & ~df["batch_id"].duplicated(keep=False)
df["supplier_valid"] = df["supplier_id"].notna()
df["valid_record"] = df[["temperature_valid", "batch_id_valid", "supplier_valid"]].all(axis=1)

clean = df[df["valid_record"]].copy()
quarantine = df[~df["valid_record"]].copy()
clean.drop(columns=["temperature_valid","batch_id_valid","supplier_valid","valid_record"]).to_csv(OUT,index=False)
quarantine.to_csv(QUARANTINE,index=False)

manifest = {"input_file": str(RAW), "sha256": sha256_file(RAW),
            "rows_received": int(len(df)), "rows_accepted": int(len(clean)),
            "rows_quarantined": int(len(quarantine))}
Path("pipeline_manifest.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
# Production note: send data over TLS using a maintained client, verify server certificates,
# and load secrets from a secret manager/environment—not from source code.
