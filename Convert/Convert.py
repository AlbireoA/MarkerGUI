from marker.convert import convert_single_pdf
from marker.models import load_all_models
from pathlib import Path
import json
import os


def convert_single(file_folder, filename, start_page, max_pages, batch_multiplier, ocr_all_pages):
    file_folder = Path(file_folder)
    fpath_in = file_folder / filename
    fpath_out = file_folder / "marker_output"
    model_lst = load_all_models()
    max_pages = max_pages
    start_page = start_page
    metadata = None
    langs = None
    batch_multiplier = batch_multiplier
    ocr_all_pages = ocr_all_pages

    full_text, images, out_meta = convert_single_pdf(fpath_in, model_lst, max_pages, start_page, metadata, langs,
                                                     batch_multiplier, ocr_all_pages)

    os.makedirs(fpath_out, exist_ok=True)

    # Save the full text to a file
    with open(fpath_out / "output_text.md", "w", encoding="utf-8") as text_file:
        text_file.write(full_text)

    # Save the images to files
    for img_name, img in images.items():
        img.save(fpath_out / img_name)

    # Save the metadata to a JSON file
    with open(fpath_out / "output_metadata.json", "w", encoding="utf-8") as meta_file:
        json.dump(out_meta, meta_file, ensure_ascii=False, indent=4)

    return True
