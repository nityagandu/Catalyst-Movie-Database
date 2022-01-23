
# Catalyst-Movie-Database

## Prerequisites

Python version 3.6 or newer is recommended. 

```bash
sudo apt install python3.9
```

Use the package manager [pip](https://pip.pypa.io/en/stable/installation/) to install Flask.

```bash
sudo apt install python3-pip
```

Install Flask.

```bash
pip install Flask
```

## Usage

Clone/Download the repository.
```bash
git clone https://github.com/nityagandu/Catalyst-Movie-Database.git
```

Run main from the downloaded repository.

```bash
python3 main.py
```

Go to the localhost which is located at http://localhost:5000/ to use the website.

## High Level Concept

UML diagram of the project.
![uml of the classes](Docs/uml.drawio.png)

Once the application starts, main calls init which loads the csv files concurrently to be read by the csv readers and parsed into lists of the respective objects (Movies and Person). These lists are arrays of all the movies in the form of Movie classes and lists of the staff and actors.

All calls from the web browser are handled by main.py which loads any relevant searches and analytics.

## Testing

Install Pytest.
```bash 
pip install pytest
```

Run tests.
```bash
python -m pytest
```

The Test Files are located under [Test Location](tests/).
