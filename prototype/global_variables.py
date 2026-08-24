from datetime import date

curr_year = date.today().year
year_stock = [str(i) for i in range(2000, curr_year + 1)]
year_part1 = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
year_part2 = [str(i - 2010) for i in range(2010, curr_year + 1)]
month = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
check_list = []
