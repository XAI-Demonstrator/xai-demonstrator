import os
import re
import hashlib
from bing_image_downloader import downloader

LIMIT = 60
BASE_DIR = "concept_data"
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

def clean_query(query):
    query = query.lower()
    query = query.replace(" ", "_")
    query = re.sub(r"[^a-z0-9_]", "", query)
    return query


def is_folder_filled(folder_path, min_files=20):
    if not os.path.exists(folder_path):
        return False
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(VALID_EXTENSIONS)]
    return len(files) >= min_files


def remove_invalid_files(folder_path):
    for file in os.listdir(folder_path):
        if not file.lower().endswith(VALID_EXTENSIONS):
            os.remove(os.path.join(folder_path, file))


def compute_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def deduplicate_images(folder_path):
    hashes = {}
    removed = 0

    for file in os.listdir(folder_path):
        if not file.lower().endswith(VALID_EXTENSIONS):
            continue

        path = os.path.join(folder_path, file)
        file_hash = compute_hash(path)

        if file_hash in hashes:
            os.remove(path)
            removed += 1
        else:
            hashes[file_hash] = file

    print(f"   → Removed {removed} duplicates")


def move_and_rename_images(src_folder, dst_folder, query_name, prefix):
    files = sorted(os.listdir(src_folder))
    counter = 1

    for file in files:
        if not file.lower().endswith(VALID_EXTENSIONS):
            continue

        ext = file.split(".")[-1]
        new_name = f"{prefix}_{query_name}_{counter}.{ext}"

        src = os.path.join(src_folder, file)
        dst = os.path.join(dst_folder, new_name)

        while os.path.exists(dst):
            counter += 1
            new_name = f"{prefix}_{query_name}_{counter}.{ext}"
            dst = os.path.join(dst_folder, new_name)

        os.rename(src, dst)
        counter += 1

concepts = {
    "object_concepts/phone": [
        "smartphone different angles",
        "android phone black screen",
        "old smartphone on table"
    ],
    "object_concepts/keyboard": [
        "computer keyboard top view",
        "mechanical keyboard variety",
        "keyboard on desk"
    ],
    "object_concepts/mouse": [
        "computer mouse top view",
        "wireless mouse desk",
        "mouse different styles"
    ],
    "object_concepts/camera": [
        "dslr camera top view",
        "camera lens up",
        "old camera desk"
    ],
    "object_concepts/cup": [
        "coffee cup top view",
        "mug filled coffee",
        "cup on desk"
    ],
    "object_concepts/glasses": [
        "glasses folded top view",
        "eyeglasses on table",
        "spectacles different styles"
    ],
    "object_concepts/notebook": [
        "notebook closed top view",
        "paper notebook desk",
        "journal closed"
    ],
    "object_concepts/keys": [
        "house keys top view",
        "car keys on table",
        "keys bunch metal"
    ],
    "form_concepts/round": [
        "round objects top view",
        "circular objects isolated",
        "plates cups circles"
    ],
    "form_concepts/rectangular": [
        "rectangular objects top view",
        "books boxes flat lay",
        "rectangular shapes isolated"
    ],
    "visual_concepts/screen_surface": [
        "smartphone black screen",
        "phone screen off reflection",
        "tablet screen off close up"
    ],
    "visual_concepts/metal": [
        "metal texture close up",
        "metal objects shiny surface",
        "steel objects random"
    ],
    "visual_concepts/paper": [
        "paper texture close up",
        "notebook pages texture",
        "paper stack top view"
    ],
    "visual_concepts/white": [
        "white objects minimal",
        "white desk setup",
        "all white objects aesthetic"
    ],
    "visual_concepts/glass": [
        "glass reflection surface",
        "glass objects transparent",
        "window reflection close up"
    ],
    "random_concepts/random_1": [
        "random objects variety",
        "street photography random",
        "nature animals mix"
    ],
    "random_concepts/random_2": [
        "city street random scene",
        "people outdoors random",
        "abstract images random"
    ],
    "random_concepts/random_3": [
        "landscape nature random",
        "animals wildlife random",
        "mixed objects scene"
    ],
}


if __name__ == '__main__':
    for folder, queries in concepts.items():
        concept_folder = os.path.join(BASE_DIR, folder)
        os.makedirs(concept_folder, exist_ok=True)

        if is_folder_filled(concept_folder):
            print(f"Skipping {folder} (already filled)")
            continue

        prefix = folder.split("/")[-1]

        for query in queries:
            print(f"\nDownloading: {folder} -> {query}")

            downloader.download(
                query,
                limit=LIMIT // len(queries),
                output_dir=BASE_DIR,
                adult_filter_off=True,
                force_replace=False,
                timeout=60
            )

            query_folder = os.path.join(BASE_DIR, query)

            if not os.path.exists(query_folder):
                continue

            query_clean = clean_query(query)

            remove_invalid_files(query_folder)

            move_and_rename_images(
                query_folder,
                concept_folder,
                query_clean,
                prefix
            )

            os.rmdir(query_folder)

        print(f"\n Deduplicating: {folder}")
        deduplicate_images(concept_folder)

    print("\n✅ DONE! Clean dataset ready.")