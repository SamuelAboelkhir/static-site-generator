import os
import shutil
import sys

from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main() -> None:
    basePath = "/"
    if len(sys.argv) > 0:
        basePath = sys.argv[1]
    static_to_public(basePath)


def find_files(path: str):
    files: list[str] = []
    for file in os.listdir(path):
        new_path = os.path.join(path, file)
        if not os.path.isfile(new_path):
            files.extend(find_files(new_path))
        else:
            files.append(new_path)
    return files


def static_to_public(basePath: str):
    if os.path.exists(dir_path_static):
        if os.path.exists(dir_path_public):
            shutil.rmtree(dir_path_public)
        os.mkdir(dir_path_public)
        files = find_files(dir_path_static)
        for file in files:
            file_split = file.split("/")
            file_split[1] = "public"
            file_split[-1] = ""
            destination = "/".join(file_split)
            os.makedirs(destination, exist_ok=True)
            _ = shutil.copy(src=file, dst=destination)
        generate_pages_recursive(
            basePath, dir_path_content, template_path, dir_path_public
        )


if __name__ == "__main__":
    main()
