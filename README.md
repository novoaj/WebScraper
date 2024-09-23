# Find the Path!
School project from Data Science Programming II course (CS320 @UWMadison).
## Project overview
Find the Path is a Python project that combines graph search algorithms, web scraping, and automation using Selenium. This project provides a practice application of DFS/BFS algorithms to search through web pages using selenium.

This project is structured into multiple classes to perform searches across various data types. It includes a web scraper that navigates through a mock website, collects data, and compiles it into a consolidated format using the pandas library.

### Technologies used
- Python: core prorgamming logic for implementing graph algorithms and web scraping logic 
- Selenium: For automating browser interactions and web scraping in headless mode
- Pandas: To handle and manipulate tabular data collected from web pages

### Project Structure
GraphSearcher (Base Class):
- Implements the core DFS/BFS algorithms
- Provides a foundation for specialized
MatrixSearcher (Subclass of GraphSearcher):
- specialized class for performing searches on matric structures
FileSearcher(Subclass of GraphSearcher):
- Designed to navigate through a directory of files, each representing a node in the graph.
WebSearcher (Subclass of GraphSearcher):
- Uses Selenium to automate web scraping of a dynamic Flask-based web application.
- Visits web pages, extracts data tables, and follows hyperlinks to other pages.
- Compiles extracted data into panda Dataframe
