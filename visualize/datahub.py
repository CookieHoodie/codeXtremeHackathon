import csv

def load_data(filename):

    data = []

    with open(filename, newline='', encoding="utf-8", errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append([row['title'],row['content']])

    return data

def main():
    load_data(r"C:\Users\Kewen\Desktop\articles1.csv")

if __name__ == '__main__':
    main()
