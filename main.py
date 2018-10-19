from app import app

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port = 2000, debug=True) # Debug true for development purpose.
    # app.run(host= '0.0.0.0', debug=True)
