import time

class tables():
    def __init__(self, framework):
        self.framework = framework

    def get_table_info(self, element):
        for _ in range(10):
            table_info = self.framework.get_text(element)
            if "Showing" in table_info:
                return table_info
            else:
                time.sleep(1)
        else:
            self.framework.fail("Can't get the table info")

    def get_table_start_number(self, table_info_element):
        table_info = self.get_table_info(table_info_element)
        return int(table_info[(table_info.index('g') + 2):(table_info.index('to') - 1)])

    def get_table_end_number(self, table_info_element):
        table_info = self.get_table_info(table_info_element)
        return int(table_info[(table_info.index('to') + 3):(table_info.index('of') - 1)])

    def get_table_max_number(self, table_info_element):
        table_info = self.get_table_info(table_info_element)
        return int(table_info[(table_info.index('f') + 2):(table_info.index('entries') - 1)])

    def get_previous_next_button(self):
        pagination = self.framework.get_list_items('pagination')
        previous_button = pagination[0].find_element_by_tag_name('a')
        next_button = pagination[(len(pagination) - 1)].find_element_by_tag_name('a')
        return previous_button, next_button

    def get_table_data(self, element):
        # This method will return a table data as a list
        self.framework.assertTrue(self.framework.check_element_is_exist('thead'))
        max_sort_value = 100

        table_max_number = self.get_table_max_number(element)
        self.framework.select('account selector', max_sort_value)
        time.sleep(3)
        page_numbers = (table_max_number / max_sort_value) + 1

        tableData = []
        for page in range(page_numbers):
            table_rows = self.framework.get_table_rows()
            self.framework.assertTrue(table_rows)
            for row in table_rows:
                cells = []
                cells_elements = row.find_elements_by_tag_name('td')
                #try:
                for cell_element in cells_elements:
                    if cell_element.text:
                        cells.append(cell_element.text)
                    else:
                        cells.append('')
                if len(cells) != 6:
                    print(len(cells_elements), len(cells), cells)
                tableData.append(cells)
                # except:
                #     #sielnt skip non english items
                #     continue

            if page_numbers > 1:
                previous_button, next_button = self.get_previous_next_button()
                next_button.click()
                time.sleep(3)

        if page_numbers > 1:
            self.framework.refresh()

        print(len(tableData))
        return tableData