 **\- Web for AI \+ Machine Learning \-**

***Combined Project Assignment***

| *Sam Van Rijn sam.vanrijn@pxl.be* | *Arno Barzan arno.barzan@pxl.be* | *Sam Vanderstraeten sam.vanderstraeten@pxl.be* |
| :---- | :---- | :---- |

***March 2026***

# **Introduction**

Welcome to New York City \- the city that never sleeps, and apparently never stops cycling either. Citi Bike, NYC's public bike share system, has grown into one of the largest and most active urban bike networks in the world, with millions of trips logged every single year.

As a team, you've been contracted by a fictional bike rental company, PXL Pedals, to build a data-driven web platform. Your mission: analyze the Citi Bike historical trip data, train a machine learning model to predict ride demand, and deliver a fully functional web platform that serves both the operations team and everyday riders.

 Put your data science hats on. The bikes won't ride themselves (yet).

**Assignment**

As a team, you'll build a full-stack web platform for PXL Pedals that:

* Provides a Gradio interface for data exploration  
* Analyzes historical Citi Bike trip data to extract meaningful insights  
* Trains a machine learning model to predict bike rental demand  
* Exposes the model and data through a FastAPI REST backend  
* Provides an interactive, role-aware Vue.js frontend for both admins and riders

**Dataset**

|  | Citi bike dataset | NYC Weather |
| :---: | :---: | :---: |
| **Date range** | 2013 \- 2025 | 2016 \- 2022 |
| **\#Records** | A lot | \~60 000 |
| **Size (MB)** | A lot | \~3 MB |
| **Type** | csv | csv |
| **Link** | [https://s3.amazonaws.com/tripdata/index.html](https://s3.amazonaws.com/tripdata/index.html) | [Data](https://drive.google.com/drive/folders/1T9uZZG85VWaHZe6uJkHSa_11fhvC4qsg?usp=sharing) |

**Citi bike dataset**

The dataset used in this project is the official Citi Bike Trip History data, published by Lyft/Citi Bike and available at: 

	[https://citibikenyc.com/system-data](https://citibikenyc.com/system-data)

You don’t have to use **ALL OF THE** Citi Bike data, because it’s a lot of gigabytes. Make sure the available weather data you use overlaps with the available Citi Bike data you use.

# **Machine Learning**

## **Deadline 1**

### **1\. Data Cleaning & Processing**

This is the first and most critical step in any Machine Learning project. You will be confronted with real-world data: messy timestamps, missing station names, outliers in trip duration and coordinates. Use all the tools in your arsenal to get a thorough understanding of your data.

At a minimum, you must:

* Load the CSV data into Pandas DataFrame(s).  
* Parse and clean the data  
* Derive new features such as trip duration (in minutes), hour of day, day of week, month, and season. Determine which other features would be useful.  
* Handle missing values and outliers (e.g. trips with negative or extreme durations, null station IDs).

### **2\. Data Exploration & Visualization**

Understanding data is inseparable from visualizing it. You are expected to generate meaningful charts and visualizations that reveal real insights. Use techniques from the AI Essentials and Machine Learning courses.

Suggested visualizations (not limited to):

* Hourly and weekly trip volume heatmaps  
* Top 10 most popular start and end stations  
* Trip duration distribution (with outlier filtering)  
* Member vs. casual rider breakdown over time  
* Geographic density map of start/end station usage  
* Electric vs. classic bike usage trends  
* …

## **Deadline 2**

### **3\. Prediction and Model Interpretation**

Generate predictions & insights for the following year. I.e.: if you’re using data from 2018 \- 2021 to train your model(s), you will want to predict for the next year.

* Train various supervised models and compare them  
* Evaluate using appropriate metrics (MAE, RMSE, R², MAPE, Precision, Recall, Accuracy, F1, …)  
* Interpret your model: which features matter most? When does demand peak? What differences exist between member and casual riders?

**Tools**

You are encouraged (and expected) to use the following libraries, among others:

* pandas, numpy \- data manipulation  
* matplotlib, seaborn, plotly \- visualization  
* scikit-learn \- preprocessing, regression, evaluation  
* statsmodels, prophet \- time series analysis  
* Joblib / pickle \- model serialization for deployment

**Web for AI**

The Web for AI part of this project is split into two distinct phases. In Part I, you use Gradio to build an interactive data exploration tool \- directly supporting the data exploration work. In Part II, you build the full-stack Vue.js platform that end users actually interact with.

 **Part I \- Gradio: Interactive EDA Interface (Deadline 1\)**

### **Introduction**

Gradio is a Python library that lets you build interactive web interfaces for data exploration, visualization, and machine learning models with very little code. In this phase, you'll use Gradio as a companion tool to your ML notebooks \- turning static analyses into explorable, shareable interfaces. 

The goal is not just to re-display your notebook charts, but to make them interactive: let the user filter, query, and explore the data themselves. Think of this as a tool that a data analyst at PXL Pedals would use daily for quick consultation of known data. 

### **Assignment**

Build a multi-tab Gradio application that covers data exploration and insight generation. The app should run standalone and be launchable with a single command.

 **Minimum Requirements**

* Provide multiple tabs that show a specific part of the dataset. As a group, determine which views or perspectives on the data would be the most useful to gather insights. (e.g. trips, bike demand, stations, …)   
* The Gradio app must be runnable with a single command (e.g. python [app.py](http://app.py))  
* Include a short README in the Gradio subfolder explaining how to run the app and what each tab does

## **Part II \- Vue.js: Full-Stack Web Platform (Deadline 2\)**

### **A \- Frontend**

Build the frontend of the PXL Pedals platform using Vue.js. The application must serve two distinct user roles: an Admin (the rental company operator) and a Rider (a registered or casual biker).

 **Minimum Requirements \- Frontend**

*  **Vue.js Single Page Application**  
  * Use the Composition API throughout  
  * Use Vue Router with at least 5 distinct routes  
  * Use Pinia for state management (auth state, user role, active filters)  
  * Use a CSS framework or UI component library (e.g. Vuetify, PrimeVue, or Tailwind CSS)  
  * Provide at least 5 useful unit or e2e tests


  

* **Authentication & route guarding**  
  * A login page that simulates authentication with two roles: admin and rider  
  * Role-based navigation: admins and riders see different menu items and pages  
  * Implement guarded routes \- unauthenticated users cannot access protected pages

* **Admin views**  
  * Provide one or more admin views that allow employees of PXL Pedals to view key metrics, like demand and availabilities  
  * Integrate the model you created in the ML part

* **Rider views**   
  * Provide one or more rider views that allow customers to view useful information

* **General**  
  * It is your responsibility to develop a useful application. Be creative and create a web app that shows the correct insights for both admins and riders. The level of creativeness is one of the evaluation criteria, so be critical about your solution\!  
  * The application must be visually appealing, user-friendly, and responsive  
  * Use Docker and docker-compose for deployment  
  * Use git for version control with clean commits, a good README, and no clutter

 **B \- Backend**

Connect your frontend to a real FastAPI backend. Make data and action accessible via API calls, implement proper JWT authentication, and serve your trained ML model through a prediction endpoint.

* In short: Build a REST API with FastAPI serving all frontend data needs  
* Protect endpoints with JWT-based authentication and role-based access control (admin vs. rider)  
* Implement all endpoints that are needed to power your frontend admin and rider views:  
  * Auth: login, token retrieval and refresh  
  * Data & analytics: depending on what you want to build, provide all necessary data endpoints  
  * Predictions: invoke the trained ML model and return demand forecasts for a given time window  
* Store data in a relational database (e.g. PostgreSQL) connected via an ORM (e.g. SQLAlchemy)  
* Provide at least 5 meaningful backend tests using pytest  
* Use git for version control with clean commits, a good README, and no clutter  
* The full stack (frontend, backend, and database) must be orchestrated with docker-compose\! 

**Deliverables**

Submit a single GitHub repository containing:

•  	Machine Learning notebooks (data cleaning, visualization, model training and evaluation)

•  	Written report in the form of markdown and notebook documentation

•  	Serialized trained model (e.g. model.pkl or model.joblib)

•  	Gradio application (Part I) \- multi-tab EDA interface

•  	Vue.js frontend application (Part II-A)

•  	FastAPI backend with all required endpoints and database integration (Part II-B)

•  	docker-compose.yml that fires up the entire stack

•  	README.md with clear setup instructions, architecture overview, screenshots, …

•        Contribution overview (see below)

Create your team repo here: [https://classroom.github.com/a/3j-c5SRK](https://classroom.github.com/a/3j-c5SRK)

 **Contribution Overview**

Each team member must log their contributions weekly throughout the project. Fabricated logs submitted at the end will not be accepted. Insufficient contributions will result in a lower individual grade. Use the following format: 

| Week | Name | Course | Hours | Description |
| :---- | :---- | :---- | :---- | :---- |
| Week of 17/03/2026 | Jane Doe | ML | 5h | Data cleaning and outlier analysis (trip duration) |
| Week of 17/03/2026 | Jane Doe | Web | 3h | Created Vue project structure and routing |
| Week of 24/03/2026 | Jane Doe | ML | 4h | Demand aggregation and feature engineering |
| Week of 24/03/2026 | Jane Doe | Web | 4h | Built admin dashboard with Pinia store |

**Deadlines**

 

|   | Day | Date | Time | Milestone |
| :---- | :---- | :---- | :---- | :---- |
| **D1** | Thursday | 02/04 | 08:30 | ML D1 \+ Web Part I (Gradio) |
| **D2** | Wednesday | 27/05 | 08:30 | ML D2 \+ Web Part II \> Working web application and prediction model |

 

**Presentation**

Both deadlines will involve the team presenting their end result for that part (ML \+ Web) and providing answers to the technical questions that are posed by the lecturers. Details and exact planning will be provided when we approach the deadline.

 **Evaluation**

The Web and ML parts will be evaluated separately. Rubrics for both parts will be shared in their respective Blackboard courses.

Make sure your work is clearly documented, your code is clean and your repository is easy to navigate.

**\!\!\! Good luck \!\!\!**

