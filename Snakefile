rule setup:
    shell: "python setup.py develop"

rule run:
    shell "python routes/routes.py"
