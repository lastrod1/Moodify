from moodify_api import create_app 

# calls from moodify_api/__init__.py
app = create_app()

if __name__ == "__main__":
    #app.run(debug = True)
    app.run(debug=True, host='0.0.0.0', port=5001)