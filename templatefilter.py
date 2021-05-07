from app import app


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b"):
    if value is None:
        return ""
    return value.strftime(format)


@app.template_filter('ru_pluralize')
def ru_pluralize(value, arg="блюдо,блюда,блюд"):
    args = arg.split(",")
    number = abs(int(value))
    arg1 = number % 10
    arg2 = number % 100

    if (arg1 == 1) and (arg2 != 11):
        return args[0]
    elif (arg1 >= 2) and (arg1 <= 4) and ((arg2 < 10) or (arg2 >= 20)):
        return args[1]
    else:
        return args[2]