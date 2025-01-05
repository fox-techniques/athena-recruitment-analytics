# ATHENA - Recruitment Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-darkcyan)](https://pypi.org/project/athena-recruitment-analytics/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/fox-techniques/athena-recruitment-analytics/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-athena--recruitment--analytics-181717?logo=github)](https://github.com/fox-techniques/athena-recruitment-analytics)

ATHENA is a cutting-edge Plotly dashboard solution designed to streamline the recruitment process by providing comprehensive analytics and insights into job applications. With interactive visualizations, dynamic data filtering, and key performance metrics, ATHENA empowers users to track, analyze, and optimize their recruitment strategies. From identifying top industries and fields to visualizing application trends across countries, ATHENA delivers actionable insights to enhance decision-making and drive recruitment success.


## Table of Contents

- [ATHENA - Recruitment Analytics](#athena---recruitment-analytics)
  - [Table of Contents](#table-of-contents)
  - [Documentation](#documentation)
  - [Features](#features)
  - [Instructions](#instructions)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
  - [Contribution](#contribution)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
    - [Icons and Graphics](#icons-and-graphics)
    - [Open-Source Libraries](#open-source-libraries)

## Documentation

The full documentation is available on **[GitHub Pages](https://fox-techniques.github.io/athena-recruitment-analytics/)**.


## Features

- **Interactive Visualizations**: Treemaps, bar charts, choropleth maps, and Irene-Sankey diagram.
- **Key Metrics at a Glance**: Track essential statistics such as the number of applications, countries, industries, active applications, and interviews.
- **Dynamic Filtering**: Adjust visualizations using filters for industries, countries, fields, and projections.
- **Comprehensive Visual Insights**: Explore Irene-Sankey flow diargam, top industries, application fields, and geographical trends.
- **Customizable Projections**: Switch between different map projections for geographical analysis.
- **Modular and Extensible Design**: Easily adaptable for additional features and data inputs.
- **User-Friendly Design**: Easy setup and seamless integration with your data.

## Instructions

> **Note**: Requires Python 3.10 or above.


## Quick Start

Here’s a quick example to create a recruitment analytics dashboard with **ATHENA**.

1. Clone the Repository

```bash
git clone https://github.com/your-repo/athena-recruitment-analytics.git
cd athena-recruitment-analytics
```

1. Set Up a Virtual Environment and Activate

```bash
python -m venv .venv
```
```bash
# On Windows
.venv\Scripts\activate
```
```bash
# On macOS/Linux
source .venv/bin/activate
```

2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the Dashboard

```bash
python app.py
```

Open your browser and go to `http://127.0.0.1:8050/`.


## Usage

ATHENA expects job applications to follow a specific folder structure and naming convention:
```
<position> - <company> [<country_code>] (<status>)
```

Example of the folder structure: 

![ATHENA Application folder structure](/docs/assets/data-directories-prep.png)


## Contribution

We welcome contributions! Visit our [Github](https://github.com/fox-techniques/athena-recuitment-analytics) repository, and to contribute:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fox-techniques/athena-recuitment-analytics/blob/main/LICENSE) file for details.


## Acknowledgments

We would like to acknowledge and thank the following individuals and resources for their contributions to the development of ATHENA: Application Tracking & Recruitment Analytics:

### Icons and Graphics

Icons used in this project are sourced from [Flaticon](https://www.flaticon.com):

- [Application](https://www.flaticon.com/free-icons/curriculum-vitae) icon by Awicon
- [Countries](https://www.flaticon.com/free-icons/globe) icon by Freepik 
- [Industries](https://www.flaticon.com/free-icons/partner) icon by Nuricon
- [Backgrounds](https://www.flaticon.com/free-icons/work) icon by Freepik
- [Active](https://www.flaticon.com/free-icons/progress) icon by HideMaru
- [Interview](https://www.flaticon.com/free-icons/interview) icon created by Freepik


### Open-Source Libraries

- Dash by Plotly: For providing a robust framework for building interactive dashboards.
- Pandas: For powerful data manipulation and analysis.
- Plotly: For creating dynamic and customizable visualizations.
- Dash Bootstrap Components: For beautiful UI components.

Special Thanks to:

- [Mahmoud Salah](https://github.com/Mahmoud2227) for his inspiring [IMDB Dashboard](https://github.com/Mahmoud2227/IMDB-Dashboard) 
- The open-source community for continuous innovation and support.
