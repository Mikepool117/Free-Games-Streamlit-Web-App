
# A Streamlit Webapp

A Streamlit Webapp that displays all the free games currently available on the internet and generates a QR Code for each game.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://free-games.streamlit.app)

Use the above button to access the app deployed using streamlit cloud.
## Run Locally

Clone the project

```bash
  git clone https://github.com/Mikepool117/Free-Games-Streamlit-Web-App.git
```

Go to the project directory

```bash
  cd my-project
```

### Project Requirements

To run this project locally, you will need to install the following modules to your python environment. The recommended python version is `3.10`.

Create a conda virtual environment by the inputting the  following command :

`conda create -n freegameapp python=3.10`

Activate the environment to install the dependencies

`conda activate freegameapp`

Then install the required modules from requirements.txt

`pip install -r requirements.txt`

Start the server to run the app

```bash
  streamlit run main.py
```

