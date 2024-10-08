# E-Commerce Data Analysis Dashboard ✨

## Introduction
The E-Commerce Data Analysis Dashboard is an interactive data analysis project focused on uncovering insights within an e-commerce dataset. This project aims to answer critical business questions such as identifying high-demand product categories, analyzing geographic purchase patterns, and understanding payment method preferences across different customer demographics.

Leveraging a combination of data science techniques and an interactive Streamlit dashboard, this project demonstrates the impact of data-driven decisions in the e-commerce domain.

## Features
- **Product Demand Analysis**: Identifies product categories with the highest demand and explores purchasing patterns based on geography.
- **Payment Preference Insights**: Analyzes customer payment preferences and explores variations based on demographics.
- **Interactive Dashboard**: Built with Streamlit, providing a user-friendly interface for real-time filtering and visualization of key metrics.

## Installation & Setup
To set up the environment, please follow these instructions. This project requires Python 3.9+ and several dependencies listed in `requirements.txt`.

### Using Anaconda:
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Using Pipenv
```
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Running the Dashboard:
Once the environment is set up, launch the Streamlit app using:
streamlit run app.py

Usage
Data Analysis Notebook: Open and run notebook.ipynb to perform exploratory data analysis (EDA) and answer key business questions.
Streamlit Dashboard: Access dashboard/app.py to view the interactive dashboard with various data visualizations and insights.
The notebook includes a step-by-step breakdown of data wrangling, exploration, and visualization processes, while the dashboard provides an easy-to-use interface for further exploration.

Project Structure
notebook.ipynb: Main Jupyter notebook containing data analysis and insights.
dashboard/app.py: Streamlit application for the interactive dashboard.
data/: Folder containing datasets, including customer, order, product, and seller information.
requirements.txt: List of dependencies required to run the project.
Examples
Below are some key insights and visualizations provided by the project:

High-demand Products: Bar charts displaying top-selling product categories.
Geographic Insights: Maps showcasing purchasing patterns by region.
Payment Preferences: Pie charts or bar graphs illustrating customer payment choices.
(Include screenshots here if available)

Future Work
Possible future enhancements include:

Adding predictive analysis on customer purchasing behavior.
Expanding the dashboard with more detailed filtering options.
Incorporating more complex visualizations, such as time-series analysis of order patterns.
