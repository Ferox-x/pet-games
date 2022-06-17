
with open('Слова.txt', 'r', encoding='utf-8') as file:
    with open('clean.txt', 'w', encoding='utf-8') as clean_file:
        for line in file:
            string = f"'{line.split()[1]}'," + " "
            clean_file.write(string)
