import os
import shutil

from markdown_blocks import markdown_to_html_node
from textnode import extract_title


def main() -> None:
    static_to_public()


def find_files(path: str):
    files: list[str] = []
    for file in os.listdir(path):
        new_path = os.path.join(path, file)
        if not os.path.isfile(new_path):
            files.extend(find_files(new_path))
        else:
            files.append(new_path)
    return files


def static_to_public():
    if os.path.exists("./static"):
        if os.path.exists("./public"):
            shutil.rmtree("./public")
        os.mkdir("./public")
        files = find_files("./static")
        for file in files:
            file_split = file.split("/")
            file_split[1] = "public"
            file_split[-1] = ""
            destination = "/".join(file_split)
            os.makedirs(destination, exist_ok=True)
            _ = shutil.copy(src=file, dst=destination)
    generate_page("./content/index.md", "./template.html", "./public/index.html")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    from_file_content = from_file.read()
    from_file.close()

    template_file = open(from_path, "r")
    template_file_content = template_file.read()
    template_file.close()

    markdown_to_html = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(markdown_to_html)

    dest_file = template_file_content.replace("{{ Title }}", title)
    dest_file_content = dest_file.replace("{{ Content }}", markdown_to_html)

    with open(f"{dest_path}", "w") as file:
        _ = file.write(dest_file_content)


if __name__ == "__main__":
    main()
