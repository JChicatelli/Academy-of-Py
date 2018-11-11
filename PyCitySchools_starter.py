#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[65]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "schools_complete.csv"
student_data_to_load = "students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# In[66]:


school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[67]:


school_data_complete.count()


# In[68]:


school_data_complete["school_name"].value_counts()


# In[69]:


#create array of unique school names
unique_school_names = school_data_complete["school_name"].unique()
unique_school_names


# In[70]:


school_count = len(unique_school_names)
school_count


# In[71]:


# total number of students
total_student_count = school_data["size"].sum()
total_student_count


# In[72]:


student_id_count = school_data_complete["student_name"].count()
student_id_count


# In[73]:


#calculate total budget
total_budget = school_data["budget"].sum()
total_budget


# In[74]:


#calculate avg math scores
avg_math_score = school_data_complete["math_score"].mean()
avg_math_score


# In[75]:


#calculate avg reading scores
avg_reading_score = school_data_complete["reading_score"].mean()
avg_reading_score


# In[76]:


#percent passing math
math_pass = student_data[(student_data['math_score'] >= 70)]
math_pass = len(math_pass)
math_pass


# In[77]:


perct_pass_math = math_pass/student_id_count
perct_pass_math


# In[78]:


#percent pass reading
pass_reading = student_data[(student_data['reading_score'] >= 70)]
pass_reading = len(pass_reading)
pass_reading


# In[79]:


perct_pass_reading = pass_reading/student_id_count
perct_pass_reading


# In[80]:


#overall percentage pass
overall_pass = student_data[(student_data['math_score'] >= 70) & (student_data['reading_score'] >= 70)]['student_name'].count()/total_student_count
overall_pass


# In[ ]:





# ## School Summary

# In[81]:


district_summary = pd.DataFrame({
    
    "School Type": [type],
    "School Name": [unique_school_names],
    "Total Schools": [school_count],
    "Total Students": [student_id_count],
    "Total Budget": [total_budget],
    "Average Reading Score": [avg_reading_score],
    "Average Math Score": [avg_math_score],
    "% Passing Reading":[perct_pass_reading],
    "% Passing Math": [perct_pass_math],
    "Overall Passing Rate": [overall_pass]

})


# In[82]:


dist_sum = district_summary[["Total Schools", 
                             "Total Students", 
                             "Total Budget", 
                             "Average Reading Score", 
                             "Average Math Score", 
                             '% Passing Reading', 
                             '% Passing Math', 
                             'Overall Passing Rate']]

#format cells
dist_sum.style.format({"Total Budget": "${:,.2f}", 
                       "Average Reading Score": "{:.1f}", 
                       "Average Math Score": "{:.1f}", 
                       "% Passing Math": "{:.1%}", 
                       "% Passing Reading": "{:.1%}", 
                       "Overall Passing Rate": "{:.1%}"})


# In[84]:


#groups by school

by_school = school_data_complete.set_index('school_name').groupby(['school_name'])

#school types
sch_types = school_data.set_index('school_name')['type']

# total students by school
stu_per_sch = by_school['Student ID'].count()

# school budget
sch_budget = school_data.set_index('school_name')['budget']

#per student budget
stu_budget = school_data.set_index('school_name')['budget']/school_data.set_index('school_name')['size']

#avg scores by school
avg_math = by_school['math_score'].mean()
avg_read = by_school['reading_score'].mean()

# % passing scores
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count()/stu_per_sch 
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/stu_per_sch 
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('school_name')['Student ID'].count()/stu_per_sch 

sch_summary = pd.DataFrame({
    "School Type": sch_types,
    "Total Students": stu_per_sch,
    "Per Student Budget": stu_budget,
    "Total School Budget": sch_budget,
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
})




#munging
sch_summary = sch_summary[['School Type', 
                          'Total Students', 
                          'Total School Budget', 
                          'Per Student Budget', 
                          'Average Math Score', 
                          'Average Reading Score',
                          '% Passing Math',
                          '% Passing Reading',
                          'Overall Passing Rate']]

#formatting
sch_summary.style.format({'Total Students': '{:,}', 
                          "Total School Budget": "${:,}", 
                          "Per Student Budget": "${:.0f}",
                          'Average Math Score': "{:.1f}", 
                          'Average Reading Score': "{:.1f}", 
                          "% Passing Math": "{:.1%}", 
                          "% Passing Reading": "{:.1%}", 
                          "Overall Passing Rate": "{:.1%}"})


# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[85]:


# sort values by passing rate
top_5 = sch_summary.sort_values("Overall Passing Rate", ascending = False)
top_5.head().style.format({'Total Students': '{:,}',
                           "Total School Budget": "${:,}", 
                           "Per Student Budget": "${:.0f}", 
                           "% Passing Math": "{:.1%}", 
                           "% Passing Reading": "{:.1%}", 
                           "Overall Passing Rate": "{:.1%}"})


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[86]:


#bottom 5 schools from worse to best
#take tail of top5 sort and re-sort from worst to best
bottom_5 = top_5.tail()
bottom_5 = bottom_5.sort_values('Overall Passing Rate')
bottom_5.style.format({'Total Students': '{:,}', 
                       "Total School Budget": "${:,}", 
                       "Per Student Budget": "${:.0f}", 
                       "% Passing Math": "{:.1%}", 
                       "% Passing Reading": "{:.1%}", 
                       "Overall Passing Rate": "{:.1%}"})


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[87]:


#creates grade level average math scores for each school 
ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School"

#show and format
math_scores.style.format({'9th': '{:.1f}', 
                          "10th": '{:.1f}', 
                          "11th": "{:.1f}", 
                          "12th": "{:.1f}"})


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[89]:


#creates grade level average reading scores for each school
ninth_reading = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_reading = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_reading = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_reading = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

#merges the reading score averages by school and grade together
reading_scores = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading
})
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]
reading_scores.index.name = "School"

#format
reading_scores.style.format({'9th': '{:.1f}', 
                             "10th": '{:.1f}', 
                             "11th": "{:.1f}", 
                             "12th": "{:.1f}"})


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[94]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$584.99", "$585-614", "$615-644", "> $644"]
school_data_complete['spending_bins'] = pd.cut(school_data_complete['budget']/school_data_complete['size'], spending_bins, labels = group_names)

#creat by spending
by_spending = school_data_complete.groupby('spending_bins')

#calculations
avg_math = by_spending['math_score'].mean()
avg_read = by_spending['reading_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()

# df build            
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})
            
#reorder columns
scores_by_spend = scores_by_spend[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_spend.index.name = "Per Student Budget"
scores_by_spend = scores_by_spend.reindex(group_names)

#formating
scores_by_spend.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})



# In[ ]:





# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[96]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_name = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
school_data_complete['size_bins'] = pd.cut(school_data_complete['size'], size_bins, labels = group_name)

#group by spending
by_size = school_data_complete.groupby('size_bins')

#calculations 
avg_math = by_size['math_score'].mean()
avg_read = by_size['math_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()

            
# df build            
scores_by_size = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
            
})
            
#reorder columns
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "Overall Passing Rate"
]]

scores_by_size.index.name = "Total Students"
scores_by_size = scores_by_size.reindex(group_name)

#formating
scores_by_size.style.format({'Average Math Score': '{:.1f}', 
                              'Average Reading Score': '{:.1f}', 
                              '% Passing Math': '{:.1%}', 
                              '% Passing Reading':'{:.1%}', 
                              'Overall Passing Rate': '{:.1%}'})


# In[ ]:





# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[100]:


# group by type of school
by_type = school_data_complete.groupby("type")

#calculations 
avg_math = by_type['math_score'].mean()
avg_read = by_type['math_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('type')['Student ID'].count()/by_type['Student ID'].count()

# df build            
scores_by_type = pd.DataFrame({
   "Average Math Score": avg_math,
   "Average Reading Score": avg_read,
   '% Passing Math': pass_math,
   '% Passing Reading': pass_read,
   "Overall Passing Rate": overall})
   
#reorder columns
scores_by_type = scores_by_type[[
   "Average Math Score",
   "Average Reading Score",
   '% Passing Math',
   '% Passing Reading',
   "Overall Passing Rate"
]]
scores_by_type.index.name = "Type of School"


#formating
scores_by_type.style.format({'Average Math Score': '{:.1f}', 
                             'Average Reading Score': '{:.1f}', 
                             '% Passing Math': '{:.1%}', 
                             '% Passing Reading':'{:.1%}', 
                             'Overall Passing Rate': '{:.1%}'})

#calculations 
avg_math = by_type['math_score'].mean()
avg_read = by_type['math_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('type')['Student ID'].count()/by_type['Student ID'].count()
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('type')['Student ID'].count()/by_type['Student ID'].count()

# df build            
scores_by_type = pd.DataFrame({
   "Average Math Score": avg_math,
   "Average Reading Score": avg_read,
   '% Passing Math': pass_math,
   '% Passing Reading': pass_read,
   "Overall Passing Rate": overall})
   
#reorder columns
scores_by_type = scores_by_type[[
   "Average Math Score",
   "Average Reading Score",
   '% Passing Math',
   '% Passing Reading',
   "Overall Passing Rate"
]]
scores_by_type.index.name = "Type of School"


#formating
scores_by_type.style.format({'Average Math Score': '{:.1f}', 
                             'Average Reading Score': '{:.1f}', 
                             '% Passing Math': '{:.1%}', 
                             '% Passing Reading':'{:.1%}', 
                             'Overall Passing Rate': '{:.1%}'})


# In[ ]:




