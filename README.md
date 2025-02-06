
<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Career Cupid: Optimizing Job Matches Through Data-Driven Insights
 </h1>

<p align='center' style="text-align:center;font-size:1em;">
    <a href="https://www.linkedin.com/in/zakhar-manikhas-306939285/"> Zakhar Manikhas</a>&nbsp;,&nbsp;
    <a href="https://www.linkedin.com/in/noor-shahin-254502344/"> Noor Shahin</a>&nbsp;,&nbsp;
    <a href="https://www.linkedin.com/in/ravid-dimant-48599224a/">Ravid Dimant</a>&nbsp;&nbsp;
    <br/> 
    Technion - Israel Institute of Technology<br/> 
<br>
    <a href="https://career-cupid.streamlit.app/">Survey</a> |
    <a href="https://youtu.be/dMre1jKHiUU?si=0qYKhWtw6YWmRANX">Trailer</a> |
    <a href="https://arxiv.org/abs/2403.02817">BTS</a>

</p>


<br>
<br>

<p align="center">
  <img src="https://raw.githubusercontent.com/RavidDimant/JobMatcher-Aligning-LinkedIn-Profiles-with-Scraped-Job-Listings/main/Survey/logo.png" alt="Logo" >



# Contents
- [Overview](#Overview)
- [Abstract](#Abstract)
- [Install](#Install)
- [Running the code](#Running-the-code)
  - [Data Scraping](#Data-Scraping)
  - [Survey](#Survey)
  - [Job Matching Algorithm](#Job-Matching-Algorithm) 
- [Results](#Results)


  
# Overview

Career Cupid is a job-matching system that goes beyond traditional keyword-based and LinkedIn-centric approaches. By integrating job listings from multiple platforms (Indeed, Dice, SimplyHired) and enriching them with user-specific survey data, Career Cupid provides a holistic job recommendation experience. Unlike existing job-matching models that primarily focus on skills and job titles, our system factors in personal interests, hobbies, and career aspirations, ensuring a deeper alignment between candidates and job opportunities.

To achieve this, we developed a data-driven pipeline that:

1. Collects and integrates over 30,000 job listings from major job platforms while overcoming scraping challenges.
2. Enhances job recommendations by incorporating user survey responses, including skills, hobbies, and career preferences.
3. Leverages AI-driven techniques such as TF-IDF and BERT embeddings to compute job-profile similarity.
4. Refines the matching algorithm by considering factors like job location, past job titles, and project descriptions.
Through this approach, Career Cupid bridges the gap between what users can do and what they love to do, improving job satisfaction and career fulfillment.

# Abstract

Traditional job-matching systems rely heavily on keyword-based searches and LinkedIn profile data, often overlooking the personal interests and aspirations that contribute to job satisfaction. *Career Cupid* introduces a novel job recommendation framework that enhances traditional job-matching techniques with user-centric personalization. By aggregating big data from multiple job platforms, including *Indeed, Dice, and SimplyHired*, and integrating a custom survey-driven approach, our system refines job recommendations beyond technical skills and job titles. To achieve this, we scrape and integrate job data without relying on external APIs, connect job listings to LinkedIn profiles to ensure relevance, and incorporate survey responses to capture users' hobbies, interests, and ideal job preferences. Leveraging AI models such as **TF-IDF, BERT embeddings, and cosine similarity**, *Career Cupid* enhances job-profile matching accuracy. The effectiveness of our approach is evaluated through data visualization and embedding-based similarity analysis. Results demonstrate that integrating **AI-driven recommendations** with **personalized survey data** leads to more meaningful and accurate job matches than traditional methods. Our findings suggest that considering user passions alongside technical skills significantly improves job satisfaction and career alignment.

# Running the code

## Data Scraping
The first step is to gather the data for the project. Navigate to the Scrapers directory and run each of the scraper files. Each scraper has a default maximum run time of 10 hours. You can adjust the amount of time you want to collect job listings from the sites (Dice, Simply Hired, and Indeed) by modifying the following line in each scraper:
```python
# maximum runtime in seconds (10 hours), theoretically, we can scrape for years
max_runtime = 60 * 60 * 10
```
We use a list of company keywords sourced from a dataset provided by the course staff, and its origin is from Brightdata. Instead of relying on the provided CSV file (company_names.csv), we suggest using the pre-defined companies_list (as shown in the comment) for convenience:
```python
# companies_list = ["Amazon", "Meta", "Nvidia", "Google", "Apple", "Microsoft", "YouTube"]
```
**Note**: You can also run the model using our pre-collected dataset, which is available via the link in the Data.md file. We've already scraped over 10,000 job listings from each site for you!

## Survey
The Career Cupid survey is a Streamlit-based web form designed to collect user input for job-matching.

Click on the survey link:  <a href="https://career-cupid.streamlit.app/"> Career Cupid Survey </a>&nbsp;
## Job Matching Algorithm
Career Cupid's job matching algorithm integrates multiple techniques to improve the relevance of job recommendations. 

### Matching Process
1. **Embedding Generation**: We compute BERT-based embeddings for job descriptions, profile 'About' sections, and job titles.
2. **Similarity Scoring**: We calculate cosine similarity between job descriptions and user profiles, incorporating additional signals from job titles and past experience.
3. **Location-Based Weighting**: We assign a location score based on whether the job is in the same city (1.0) or state (0.5) as the candidate.
4. **Survey Personalization**: To further refine recommendations, we introduce personalized scoring based on survey responses:
   - **Projects**: Cosine similarity between past projects and job descriptions.
   - **Skills & Hobbies**: Weighted match percentage between user-provided skills/hobbies and job requirements.
   - **Job Type Preference**: Minor adjustment based on user-indicated job types.

### Scoring Function
```math
Score = 0.33 \cdot similarity_{title} + 0.225 \cdot similarity_{description} + 0.225 \cdot similarity_{project} 
+ 0.05 \cdot score_{location} + 0.01 \cdot score_{hobbies} + 0.15 \cdot score_{skills} + 0.01 \cdot score_{job-type}
```

This multi-faceted approach significantly improves job recommendations, aligning them with user interests and backgrounds. The model successfully avoids misleading matches (e.g., interpreting "hungry to learn" as a food industry preference) and instead prioritizes roles that better fit the candidate's expertise and aspirations.

# Results
Career Cupid significantly improves job matching by incorporating AI-driven personalization beyond traditional keyword-based approaches. For example, Autumn Venson-Roscoe, a B.A. in Communication Studies graduate, was initially matched with Sr. Optical Engineer (Exterior Lighting) and Barista, roles unrelated to her expertise. After applying Career Cupid’s recommendation model, her top matches became Copywriter and Interactive Producer, aligning with her skills in social media management, marketing, and problem-solving, as well as her hobbies in photography, pop culture, and networking.

This transformation demonstrates how Career Cupid refines job recommendations by considering both professional qualifications and personal interests, leading to more relevant and fulfilling career opportunities.

| recommendations before                                                          |  recommendations before                                                                       |
|---------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
|Sr. Optical Engineer Exterior Lighting |Copywriter |
|Barista|  Interactive Producer     |




