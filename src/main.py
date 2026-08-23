import os
import shutil

from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


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
        generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
