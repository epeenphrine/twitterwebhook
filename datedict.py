
numbers = ["1", "2", "3", "4"]

months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
]

days = {

}

for i in range(1,32):
    if i < 10: 
        days[str(i)] = f"0{i}"
    else:
        days[str(i)] = f"{i}"

print(days)

for num in numbers:
    print(days[num])


month_key = {
    'Jan' : '01',
    'Feb' : '02',
    'Mar' : '03',
    'Apr' : '04',
    'May' : '05',
    'Jun' : '06',
    'Jul' : '07',
    'Aug' : '08',
    'Sep' : '09',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12'
}
