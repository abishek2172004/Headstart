from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ensures the app runs and directs to 'index1.html' as the main page
    app.run(debug=True)
