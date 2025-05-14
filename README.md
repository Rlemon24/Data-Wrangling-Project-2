# Data-Wrangling-Project-2
# United States Economic Dashboard

# Overview
The U.S. Economic Dashboard is an interactive web application designed to visualize and analyze various U.S. economic indicators. Built with Dash, the application enables users to explore economic trends in real time, with interactive charts and filters that focus on key economic areas such as:

Economic Growth: Gross Domestic Product (GDP), industrial production, and real disposable income.

Government Spending: Federal government debt, expenditures, and social programs.

Wages & Income: Trends in median household income, weekly earnings, and personal savings rate.

Interest Rates & Inflation: Federal Funds Rate, Treasury Yields, and inflation rates.

Users can interact with the data using dynamic range sliders, dropdown filters, and various visualization types, including scatter plots, box plots, and bar charts.

# Key Features
Interactive Data Overview: Filter data by year and columns of interest. The data is presented in an interactive table.

Charts and Visualizations: Create scatter plots, box plots, and bar charts with customized variables on the X and Y axes.

Recession and Event Overlays: Visualize recessions and major historical events (e.g., 9/11, the 2008 financial crisis, COVID-19) on charts for added context.

Correlation Analysis: Calculate and display Pearson correlation coefficients between selected variables, highlighting relationships between economic indicators.

Customizable Sliders and Filters: Use range sliders to filter data based on years and value thresholds.

# Technologies Used
Dash: Framework for building interactive web applications.

Dash Bootstrap Components: For responsive UI design.

Plotly: For dynamic data visualizations (scatter plots, box plots, line charts).

Pandas: For data manipulation and processing.

Scipy: For Pearson correlation calculation.

# Data Sources
The data used in this U.S. Economic Dashboard project was sourced from the following major U.S. government agencies and databases, which were used to create the Project2Data.csv file for the app:

- U.S. Bureau of Economic Analysis (BEA)
The BEA provides data on U.S. economic accounts, including national income and product accounts (NIPA), GDP, personal income, and other economic indicators.

- U.S. Federal Reserve Economic Data (FRED)
Managed by the Federal Reserve Bank of St. Louis, FRED offers a wealth of economic data, including historical economic indicators such as inflation, interest rates, and employment statistics.

- U.S. Bureau of Labor Statistics (BLS)
The BLS provides data on U.S. labor market conditions, including unemployment rates, wage levels, and other related statistics.

These sources are publicly available and regularly updated to reflect the latest economic data. The data from these agencies has been processed and integrated into a CSV file (Project2Data.csv) used for the dashboard's analysis and visualizations.
