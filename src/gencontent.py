import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line
            break
    if title == "":
        raise Exception("No title found")
    return title.removeprefix("#").strip()


def generate_page(
    basePath: str, from_path: str, template_path: str, dest_path: str | Path
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_file_content = f.read()

    with open(template_path, "r") as t:
        template_file_content = t.read()

    markdown_to_html = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(from_file_content)

    dest_file = template_file_content.replace("{{ Title }}", title)
    dest_file_content = dest_file.replace("{{ Content }}", markdown_to_html)
    dest_file_href = dest_file_content.replace('href="/', f'href="{basePath}/')
    dest_file_src = dest_file_href.replace('src="/', f'src="{basePath}/')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(f"{dest_path}", "w") as file:
        _ = file.write(dest_file_src)


def generate_pages_recursive(
    basePath: str, dir_path_content: str, template_path: str, dest_dir_path: str
):
    content_files = os.listdir(dir_path_content)
    print(f"found {content_files} under {dir_path_content}")
    for file in content_files:
        origin = os.path.join(dir_path_content, file)
        dest = os.path.join(dest_dir_path, file)
        if os.path.isfile(origin):
            dest = Path(dest).with_suffix(".html")
            print(f"generating {dest} from {file}")
            generate_page(basePath, origin, template_path, dest)
        else:
            print(f"parsing subdirectory {origin}")
            generate_pages_recursive(basePath, origin, template_path, dest)
