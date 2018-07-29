from setuptools import setup

setup(name="roman_wing_API",
      version="0.1",
      url="https://github.com/In-The-Lab/roman_wing_api",
      author="In The Lab",
      packages=["db"],
      install_requires=[
          "flask",
          "mysql-connector-python",
          "configparser",
          "pytz",
          "bcrypt",
          "PyJWT"
      ]
)
