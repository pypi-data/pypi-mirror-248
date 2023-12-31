from .utils import *


def elements_to_pages(
    elements: list,
    all_data: bool = False,
    data_keys: list[str] = [
        "type",
        "text",
        "page_number",
        "file_directory",
        "filename",
    ],
) -> list[dict]:
    pages = []
    page = []
    for element in elements:
        element.apply(clean_text)
        element = element.to_dict()
        if element["type"] == "PageBreak":
            pages.append(page)
            page = []
        elif all_data:
            page.append(element)
        else:
            page_data = {}
            for key in data_keys:
                if key in element:
                    key = [key]
                elif key in element["metadata"]:
                    key = ["metadata", key]
                else:
                    continue
                page_data[key[-1]] = nested_idx(element, *key)
            page.append(page_data)
    return pages if pages else [page]


def pdf_to_pages(
    pdf_file: str | Path,
    infer_table_structure: bool = True,
    all_data: bool = False,
    data_keys: list = [
        "type",
        "text",
        "page_number",
        "file_directory",
        "filename",
    ],
) -> list[dict]:
    pdf_elements = partition_pdf(
        filename=pdf_file,
        include_page_breaks=True,
        infer_table_structure=infer_table_structure,
    )
    return elements_to_pages(pdf_elements, all_data=all_data, data_keys=data_keys)


def pdf_to_chunks(
    pdf_file: str | Path,
    max_characters: int = 5000,
    all_data: bool = False,
    data_keys: list = [
        "text",
        "page_number",
        "file_directory",
        "filename",
    ],
) -> list[dict]:
    pdf_elements = partition_pdf(pdf_file)
    pdf_chunks = chunk_by_title(pdf_elements, max_characters=max_characters)
    return elements_to_pages(pdf_chunks, all_data=all_data, data_keys=data_keys)[0]



