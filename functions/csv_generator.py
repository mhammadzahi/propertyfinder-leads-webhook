import os, csv, json
from collections.abc import MutableMapping


def flatten_dict(d: MutableMapping, parent_key: str = "", sep: str = "."):
    """Recursively flatten nested JSON into dot-notation keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    return dict(items)


def save_to_csv(data, filename="propertyfinder_listings.csv", schema_file="propertyfinder_schema.json"):
    """
    Save Property Finder data into a CSV file with a stable column structure.
    - First run: creates CSV + schema.
    - Subsequent runs: aligns to existing schema, fills missing fields as blank.
    """
    if not data:
        print("No data found to write to CSV.")
        return

    # Flatten all data items
    flattened_data = [flatten_dict(item) for item in data]

    # Step 1: Load or build schema (column order)
    schema = []
    if os.path.isfile(schema_file):
        with open(schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)

    # Collect current keys from data
    current_keys = sorted({key for item in flattened_data for key in item.keys()})

    # Step 2: If schema doesn’t exist, create it
    if not schema:
        schema = current_keys
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
        print(f"🧩 New schema created and saved to '{schema_file}' with {len(schema)} columns.")
    else:
        # Merge new keys into schema if any new columns appear
        new_columns = [k for k in current_keys if k not in schema]
        if new_columns:
            print(f"⚙️ Detected {len(new_columns)} new columns, updating schema.")
            schema.extend(new_columns)
            with open(schema_file, "w", encoding="utf-8") as f:
                json.dump(schema, f, ensure_ascii=False, indent=2)

    # Step 3: Write or append data to CSV
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=schema)

        # Write header only on first creation
        if not file_exists:
            writer.writeheader()

        # Fill missing columns as empty string
        for item in flattened_data:
            row = {col: item.get(col, "") for col in schema}
            writer.writerow(row)

    print(f"✅ Appended {len(flattened_data)} records to '{filename}' "
          f"({'created' if not file_exists else 'updated'}).")



# -----------------------------------------------------------------------------------------------------


def generate_listing_by_id(filepath, val1, val2, val3):
    # Check if file already exists
    file_exists = os.path.isfile(filepath)

    # Open file in append mode
    with open(filepath, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # If file does not exist, write the header first
        if not file_exists:
            writer.writerow(["listing_id", "row_number", "listing_data"])

        # Write the passed values
        writer.writerow([val1, val2, val3])
