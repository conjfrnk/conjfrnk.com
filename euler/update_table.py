import csv
from bs4 import BeautifulSoup


def read_csv(file_path):
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        problems = list(reader)
    return problems


def create_table_content(problems):
    content = []
    current_table = []
    row = []
    count = 0
    for problem in problems:
        if len(row) == 25:
            current_table.append(row.copy())
            row = []
        if count == 100:  # Start a new table after every 100 problems
            content.append(current_table.copy())
            current_table = []
            count = 0
        status_class = "completed" if problem["Solve Status"] == "1" else "open"
        desc = problem["Description"]
        id = problem["ID"]
        row.append(
            f'<td class="{status_class}"><a href="https://projecteuler.net/problem={id}" title="{desc}">{id}</a></td>'
        )
        count += 1
    if row:
        current_table.append(row)
    if current_table:
        content.append(current_table)
    return content


def update_html(file_path, tables_content):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Remove old progress tables
    container = soup.find("div", class_="container")
    if container:
        for table in container.find_all("table", class_="progress"):
            table.decompose()
    else:
        container = soup.new_tag("div", **{"class": "container"})
        soup.body.append(container)  # Append container to body if it does not exist

    # Append new tables to the container
    for table_content in tables_content:
        new_table = soup.new_tag("table", **{"class": "progress"})
        for row in table_content:
            tr = soup.new_tag("tr")
            for td in row:
                tr.append(
                    BeautifulSoup(td + "\n", "html.parser")
                )  # Adding newline for better formatting
            new_table.append(tr)
        container.append(new_table)

    # Write the updated HTML back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


# Usage
problems = read_csv("pe_minimal_problems.csv")
tables_content = create_table_content(problems)
update_html("stats.html", tables_content)
