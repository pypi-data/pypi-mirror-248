import urllib.parse

def read_urls(path, save):
    url_parts = set()

    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            url_string = line.strip()
            parsed_url = urllib.parse.urlparse(url_string)

            if parsed_url.path is not None:
                path_array = parsed_url.path.split('/')
                path_array = [part for part in path_array if part]  
                parts = [
                    f"{parsed_url.scheme}://{parsed_url.hostname}/{'/'.join(path_array[:index + 1])}/"
                    for index in range(len(path_array))
                ]
                url_parts.update(parts)

    urls = sorted(url_parts, key=len)
    print("\n".join(urls))

    if save:
        with open(save, 'a') as save_file:
            for element in urls:
                save_file.write(f"{element}\n")

    return list(url_parts)

if __name__ == "__main__":
    path_input = input("Enter the path: ")
    save_input = input("Enter the save file path (press enter to skip): ")

    loader_instance = read_urls(path_input, save_input)
