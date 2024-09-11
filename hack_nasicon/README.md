# NASICON Materials Project (Hackathon)

## Project Overview
This project focuses on analyzing 12 NASICON (Na Super Ionic Conductor) materials. The project includes:
- Built an ontology using discomat and rdflib package to represent the data.
- The ontology is stored in a .ttl file and visualized using ggraph in an .html format.
- Add ontology to dome 4.0 if you want

## Files
- nasicon.csv: Contains some data about nasicon materials (both experimental and simulation)
- nasicon.ttl: The generated ontology in Turtle format.
- nasicon.html: Visualization of the ontology
- nasicon.py: Python script for building the nasicon material ontology and generating the visualization.
- Chemical_formula_Parser.py: Script for parsing chemical formulas.

## Requirements
To run this project, the following dependencies are required:
- pandas
- rdflib
