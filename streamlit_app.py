# streamlit_app.py

# This file serves as the main entry point for the Streamlit app.
# It allows us to run the app from the root directory, which solves
# the Python module import paths.

from app.main import main

if __name__ == "__main__":
    main()
