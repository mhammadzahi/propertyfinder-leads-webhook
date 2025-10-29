import os
import csv
import requests
import time

def download_file(url, file_name, save_dir, force_download, retries):
    """
    Download a file from URL and save it as file_name in save_dir.
    Skips if file exists unless force_download=True.
    Retries on failure up to `retries` times.
    """
    if not url or not url.startswith("http"):
        print(f"⚠️ Skipping empty/invalid URL")
        return None

    os.makedirs(save_dir, exist_ok=True)
    if not file_name.lower().endswith(".mp3"):
        file_name += ".mp3"

    file_path = os.path.join(save_dir, file_name)

    if os.path.exists(file_path) and not force_download:
        print(f"⏩ Already downloaded: {file_name}")
        return file_path

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Downloaded: {file_name}")
            return file_path
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"❌ Error downloading {file_name} (attempt {attempt}/{retries}): {e}")
            time.sleep(1)  # wait before retrying

    print(f"⚠️ Failed to download {file_name} after {retries} attempts")
    return None



def download_all_from_csv(csv_file, url_column, save_dir, force_download):
    """
    Read CSV and download all files using row_number as filename.
    Skips rows which already exist in `save_dir` BEFORE starting downloads,
    making the script much faster for large batches.
    """
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return

    # ✅ Collect already-downloaded row numbers (from existing .mp3 files)
    os.makedirs(save_dir, exist_ok=True)
    existing_files = {
        os.path.splitext(f)[0]  # filename without extension (row number)
        for f in os.listdir(save_dir)
        if f.lower().endswith(".mp3")
    }

    # Read CSV and collect rows with URLs
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if url_column not in reader.fieldnames:
            print(f"❌ Column '{url_column}' not found in CSV. Columns: {reader.fieldnames}")
            return

        rows = [(i + 2, row[url_column]) for i, row in enumerate(reader) if row.get(url_column)]

    print(f"🎧 Total recordings found in CSV: {len(rows)}")

    # ✅ Filter out already downloaded rows
    rows_to_download = [(row_number, url) for row_number, url in rows if str(row_number) not in existing_files]

    print(f"⏭️ Already downloaded: {len(rows) - len(rows_to_download)}")
    print(f"📥 To download now: {len(rows_to_download)}")

    # Proceed with only files not yet downloaded
    for i, (row_number, url) in enumerate(rows_to_download, start=1):
        print(f"[{i}/{len(rows_to_download)}] Downloading row: {row_number}")
        download_file(url, f"{row_number}", save_dir=save_dir, force_download=force_download, retries=2)
        time.sleep(1)

    print(f"✅ Finished downloading new recordings to '{save_dir}'")
