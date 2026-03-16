
from extract_data import *
import time
from store_data_database import *

url = "https://locations.wendys.com/united-states/ne/mccook/226-westview-plz"

def main():
    create_table()
    print("table and db create")
    html_content = read_html_content(url)
    burger_list = extract_data_from_html(html_content)
    insert_data_in_table(list_data=burger_list)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("time different  : ", end - start)





