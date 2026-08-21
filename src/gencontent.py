import os

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


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_file_content = f.read()

    with open(template_path, "r") as t:
        template_file_content = t.read()

    markdown_to_html = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(from_file_content)

    dest_file = template_file_content.replace("{{ Title }}", title)
    dest_file_content = dest_file.replace("{{ Content }}", markdown_to_html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(f"{dest_path}", "w") as file:
        _ = file.write(dest_file_content)
