---
title: Student school attendance analysis
summary: Built a pipeline that loads PK-12 attendance data into a normalized PostgreSQL schema and explores it through interactive Python dashboards by district and student group.
problem: Attendance rates for high-needs groups (students experiencing homelessness, students with disabilities, English learners) were hidden in one flat state file, which made district-by-group comparisons across three school years slow to answer.
timeline: 2024-01 to 2024-04
skills: [Python, Pandas, SQL, PostgreSQL, Data Modeling, Data Visualization, Matplotlib, Seaborn, Jupyter]

venue: DCS535 Advanced Data Analytics, Judson University
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: normalize-before-plotting
    question: Should the analysis run straight off the CSV or through a database?
    options: [Plot directly from the flat CSV, Normalize into a relational schema first]
    chose: Normalize into a relational schema first
    why: Splitting the file into Districts, Student_Groups, Attendance and Attendance_Records tables with composite keys made each district-by-group-by-year question a simple join, and kept suppressed cells from being misread as zeros.
    bubble: Designed an E-R model before drawing a single chart.

outcomes:
  - metric: School years compared
    value: "3 (2019–2022)"
  - metric: Relational tables
    value: 4
---

## Data

The Kaggle "Student School Attendance" dataset: attendance rates for public school students by district and student group for 2019–20, 2020–21 and 2021–22. Groups include students experiencing homelessness, students with disabilities, free or reduced lunch, English learners, high-needs versus non-high-needs, and race and ethnicity. Cells are suppressed where counts are too small to publish.

## What I built

1. **Profiling** in pandas: shape, head and tail, types, summary statistics and null counts.
2. **E-R model** with four tables, primary and composite keys, and foreign keys back to districts and student groups.
3. **Loading** into PostgreSQL, verified in pgAdmin.
4. **Exploration** with Matplotlib, Seaborn and ipywidgets dropdowns, so a reader can pick a district and a student group and see the trend.
