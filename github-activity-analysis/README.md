# Github Activity Analysis

## Team members
Kalenga Mumba


## Data Source

What data source did you work with?

I worked with the GitHub Archive API that contains a complete record of public GitHub events for every hour in January 2015, stored as newline-delimited JSON files (json.gz). Each line represents a single event, such as a push to a repository, a pull request, an issue being opened, a repository being starred, or a wiki edit. Key information captured for each event includes the type of event, the user who triggered it, the repository involved, event-specific details in the payload, and the timestamp of when the event occurred. This dataset enables analysis of patterns in GitHub activity, including the frequency of different event types over time, popular repositories, and user engagement.

## Challenges / Obstacles

What challenges did this data choice present in data gathering, processing and analysis, and how did you work through them? What methods and tools did you use to work with this data?

Working with this dataset presented several challenges. First, the data is extensive, covering every hour of a month, which makes downloading, storing, and processing resource-intensive. Second, the JSON files sometimes contain distorted lines, requiring careful error handling during parsing. To address these challenges, I converted the original JSON files to Parquet files, enabling efficient storage and retrieval of data in a compressed columnar format. This approach allowed for faster processing and reduced memory usage. Filtering by specific dates and event types was essential to focus the analysis and manage the large dataset effectively, and I used visualization tools to summarize and display the results.

## Analysis

The bar plot displaying the top 10 repositories by the number of PushEvents from January 5 to January 11, 2015, highlights a significant skew in contributions, where a small number of repositories dominate the push activity on GitHub. For instance, the repository KennaSullivan/heartbeat leads by a wide margin, indicating it was a focal point for developer contributions during this period. This concentration suggests that a few popular or actively maintained projects attract the bulk of development efforts, reflecting either a larger community engagement around these repositories or critical ongoing development work. The presence of repositories like sakl-mirror/mesie and qdnflor/dsml.github.io among the top contributors also suggests diversity in project types and possibly different domains or programming languages that are being actively developed. The line plot of average GitHub events per hour over the same week reveals a clear daily rhythm in user activity. GitHub events peak during typical working hours, with activity rising steadily from the morning, reaching the highest levels in the afternoon and early evening hours, and then gradually declining late at night. This pattern aligns closely with standard global workday cycles, reflecting when developers are most productive and engaged. The midday and early afternoon peaks correspond to active collaboration, code reviews, and pushes before the official deadlines. At the same time, the drop during night hours indicates less activity as developers rest or work on offline tasks. Overall, these visualizations paint a picture of concentrated repository activity influenced by both project popularity and typical human work patterns. They highlight the importance of certain key projects within the GitHub ecosystem and demonstrate how developer activity is strongly tied to conventional work schedules, underscoring the global, yet time-sensitive nature of software development workflows.


## Plot / Visualization

[![Alt text](visualizations/PushEvents_repo_usage.png)
![Alt text](visualizations/average_events.png)

## GitHub Repository

https://github.com/KCM2005/Kalenga-ds3022-dp3/tree/main
