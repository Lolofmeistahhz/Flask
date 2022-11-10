GROUP = 4
if  GROUP == 1:
    from apppri import app
elif GROUP == 2:
    from apppi import app
elif GROUP == 3:
    from appist import app
elif GROUP == 4:
    from appivt import app

if __name__ == '__main__':
    app.run(debug=True)