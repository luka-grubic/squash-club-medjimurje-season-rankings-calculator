import tomllib



MAX_POINTS = 500



def main():
    season = "Unknown"
    files = []
    save_to_csv = False
    print_to_console = True

    with open('config.toml', 'rb') as config_file:
        config_data = tomllib.load(config_file)

        season = config_data['season']
        files = config_data['files']
        save_to_csv = config_data['save_to_csv']
        print_to_console = config_data['print_to_console']

    table = {}

    current_file_idx = 0
    for file_path in files:
        points = MAX_POINTS

        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                if not "GROUP_" in line:
                    # Remove end-line.
                    line.rstrip()

                    # Split by tabs.
                    elems = line.split('\t')        

                    # Extract name and remove extra space.
                    name = elems[0].rstrip(' ')     

                    if not name in table:
                        table[name] = [0] * len(files)

                    table[name][current_file_idx] = points
                    points -= 5

        current_file_idx += 1
    # !for file_path in files

    # Sort dict in descending order by total points.
    final_table = sorted(table.items(), key=lambda item: sum(item[1]), reverse=True)

    if print_to_console:
        pos = 1
        for name, points in final_table:
            pos_str = f"{pos}."

            print(f"{pos_str:<5} {name:20}", end='')
            for p in points:
                print(f"{p:5d}", end='')
            print(f"{sum(points):>10}")

            pos += 1
    # !if print_to_console

    if save_to_csv:
        pos = 1
        lines = []
        for name, points in final_table:
            line = f"{pos}.;{name};"
            for p in points:
                line += f"{p};"
            line += f"{sum(points)}\n"

            lines.append(line)

            pos += 1

        with open(f"standings_{season}.csv", 'w', encoding="utf-8") as csv_file:
            for line in lines:
                csv_file.write(line)
    # !if save_to_csv
# !def main



if __name__ == '__main__':
    main()