# Roman Wing Frontend

## General Info

This folder contains all front-end resources: the html, css, js, and flask that renders templates and interacts with the api.

The static folder will contain the files that always stay the same, i.e. styling and javascript for user interaction.

The templates folder contains html templates for each page on the site. These templates are dynamic depending on the information received from the api. layout.html contains that base html that extends to all other pages. The includes folder contains elements that have enough complexity for their own file.

routes.py is the front-end flask app that contains the routes and functions to get information from the api and render it into into the html templates.
