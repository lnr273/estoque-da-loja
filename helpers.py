from flask import render_template

def validateInt(n):
    try:
        n = int(n)
    except ValueError:
        return 0
    return n
    

def validateFloat(n):
    try:
        n = float(n)
    except ValueError:
        return 0
    return n
    

def error(msg, code):
    return render_template("error.html", message=msg, errorCode=code)