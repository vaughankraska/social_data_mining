# Datasheet for: twitter/text/image dataset[^1]

## Authors: Anand Mathew M S, Finn Vaughankraska
### Related Files:
./data/media_lists.txt
./data/media/*
./data/tweets.dat

Version 1.0 2024-11-05

## Motivation

__For what purpose was the dataset created?__
This Dataset was created for the social data mining course. While its main purpose is to serve as a practice dataset for the sake of the authors' learning within the scope of the course, it also serves as a source of information to analyze visual persuasion on Twitter.

__Was there a specific task in mind?__
More explicitly, the listed directives of this dataset is as follows:
- Refresh basic skills for text and data file processing and summarization
- Familiarize the authors with a typical data format.
- Reflect on and/or identify possible data quality and validity issues.
- Generate datasets to be used during the course.
- Practice documenting social data.

__Was there a specific gap that needed to be filled? Please provide a description.__
N/A

__Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?__
The dataset was created by Anand Mathew and Finn Vaughankraska as students in course _1DL465 11012_ (Mining of Social Data) at Uppsala University. More specifically the instruction set was presumed to be created by Matteo Magnani.


__Who funded the creation of the dataset?__ If there is an associated grant, please provide the name of the grantor and the grant name and number.
The funding for the original data came from PolarVis. The supporters for the project are listed as:
> Project PolarVis is supported by FORTE, the Swedish Research Council for Health, Working Life and Welfare; Uddannelses - og Forskningsstyrelsen, the Danish Agency for Higher Education and Science; the National Research, Development and Innovation Office Hungary; and FWF, the Austrian Science Fund under CHANSE ERA-NET Co-fund programme, which has received funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement

However both authors of this dataset are fee paying students and an argument could be made that they are funding the creation of this dataset on some level.


__Any other comments?__
[Link to the source for the data project](https://polarvis.github.io/)


## Composition

__What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)?__ Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? Please provide a description.

The JSON data provided represents tweet objects with various fields:
1. **text**: The main content of the tweet, including any retweeted message, hashtags, URLs, and other text content.

2. **entities**: Contains various subfields to identify special elements within the tweet text:
   - **mentions**: Lists users mentioned in the tweet
   - **hashtags**: Hashtags within the tweet
   - **annotations**: Contextual metadata on keywords, including a **probability** score, **type** (e.g., "Place", "Other"), and **normalized_text**.
   - **urls**: Includes URLs within the tweet, with **start** and **end** positions, **url**, **expanded_url** (the full URL), and **display_url**.

3. **possibly_sensitive**: Boolean flag indicating whether the tweet content might be sensitive.

4. **edit_history_tweet_ids**: List of IDs representing historical edits of the tweet, with the current tweet's ID.

5. **lang**: The language code of the tweet (e.g., "en" for English, "es" for Spanish).

6. **created_at**: Timestamp of when the tweet was posted in ISO 8601 format.

7. **referenced_tweets**: Contains data on other tweets referenced within the tweet, including **type** (e.g., "retweeted") and **id** of the referenced tweet.

8. **author_id**: ID of the user who posted the tweet.

9. **conversation_id**: ID of the conversation thread this tweet belongs to, usually the same as **id** for the root tweet.

10. **id**: Unique identifier for the tweet.

11. **attachments**: Stores information about any media attached to the tweet, such as images or videos, referenced by **media_keys**.
    - **media_keys**: The key matching the media_lists.txt entries with the full image extension (file name pointer).

12. **public_metrics**: Contains engagement metrics for the tweet:
    - **retweet_count**: Number of retweets.
    - **reply_count**: Number of replies.
    - **like_count**: Number of likes.
    - **quote_count**: Number of times the tweet was quoted.

13. **context_annotations**: Metadata that categorizes the tweet within broader domains and entities (e.g., "Extreme Weather + Climate Change"), including:
    - **domain**: Category of context (e.g., "Events") and an **id**.
    - **entity**: Specific entity name and **id**.


__How many instances are there in total (of each type, if appropriate)?__
2,260,916 entries of tweets as outlined above with 44,482 images in the media_list.txt file.

__Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set?__
- If the dataset is a sample, then what is the larger set?
It is technically a subsample of the data that is available on Twitter during that period.
- Is the sample representative of the larger set (e.g., geographic coverage)? If so, please describe how this representativeness was validated/verified. If it is not representative of the larger set, please describe why not (e.g., to cover a more diverse range of instances, because instances were withheld or unavailable).
The dataset contains tweets and images from the time period 30/11 to 12/12 2015 with the hashtag "cop21". The subsample is not representative of the population ("population" being all the tweets on twitter) since collection was focused around a single hashtag which is not a random sample of the possible Tweets on the platform. The authors did not collect the original data, but downloaded it in 2024.

__What data does each instance consist of?__ Raw data (e.g., unprocessed text or images) or features? In either case, please provide a description.
Both _raw data_ (text and images) and semi-structured features representing the interactions and meta-data surrounding the tweet.

__Is there a label or target associated with each instance?__ If so, please provide a description.
No, there is not a target feature defined (yet).

__Is any information missing from individual instances?__ If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include, e.g., redacted text.
No, we have not omitted any features from the original data.

__Are relationships between individual instances made explicit (e.g., users, movie ratings, social network links)?__ If so, please describe how these relationships are made explicit.
Yes, users are referenced by both their Twitter handles (usernames) and by **author_id**. Additionally links are made between tweets and media via the attachments object.

__Are there recommended data splits (e.g., training, development/validation, testing)?__ If so, please provide a description of these splits, explaining the rationale behind them.
No.

__Are there any errors, sources of noise, or redundancies in the dataset?__ If so, please provide a description.
Not that the authors are aware of.

__Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)?__
No, the dataset is not self-contained since there are urls listed in the tweets entries.
- If it links to or relies on external resources
    a) are there guarantees that they will exist, and remain constant, over time;
    No the users who made tweets could delete or edit the source and the entry could cease to exist on the internet or be changed.
    b) are there official archival versions of the complete dataset (i.e., including the external resources as they existed at the time the dataset was created);
    NA
    c) are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a future user? Please provide descriptions of all external resources and any restrictions associated with them, as well as links or other access points, as appropriate.
    The dataset download was protected by a password access granted by the course instructor.

__Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals non-public communications)?__ If so, please provide a description.
The data contains images and Tweets that could be classified as personal identifiable information.

__Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?__ If so, please describe why.
Yes, social media and Twitter are known for having offensive, insulting, threatening, and anxiety-causing content since they allow a vast range of unfiltered opinions and reactions from users across the world.

__Does the dataset relate to people?__ If not, you may skip the remaining questions in this section.
Yes.

__Does the dataset identify any subpopulations (e.g., by age, gender)?__ If so, please describe how these subpopulations are identified and provide a description of their respective distributions within the dataset.
If you consider people on social media who post and interact with content under the "cop21" hashtag, then yes the dataset identiefies subpopulations who interact with the hashtag.

__Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset?__ If so, please describe how.
Yes, the data are Tweets made by real people on Twitter. You can identify users by their username, name, author id, images, and by the content they post.

__Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)?__ If so, please provide a description.
Yes, images and urls in the dataset show individuals' faces and therefore their ethnic origins (and if neural networks can identify peoples' sexual orientations by only their face, then the dataset also reveals that).

__Any other comments?__


## Collection Process

__How was the data associated with each instance acquired?__ Was the data directly observable (e.g., raw text, movie ratings), reported by subjects (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part-of-speech tags, model-based guesses for age or language)? If data was reported by subjects or indirectly inferred/derived from other data, was the data validated/verified? If so, please describe how.
The original data was collected via the Twitter Academic API but the authors collected it via https://uppsala.box.com

__What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)?__ How were these mechanisms or procedures validated?
The original collection mechanism (Academic API) cannot be validated but the download link was verfied via seeing the same data downloaded by two seperate devices.

__If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?__
By choosing the "cop21" hashtag and collecting tweets under that search key. The authors of this data card have not subsampled anything more.

__Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?__
Students Anand Mathew and Finn Vaughankraska who are both unpaid. PolarVis (who studies visual persuasion) is "FORTE, the Swedish Research Council for Health, Working Life and Welfare; Uddannelses - og Forskningsstyrelsen, the Danish Agency for Higher Education and Science; the National Research, Development and Innovation Office Hungary; and FWF, the Austrian Science Fund under CHANSE ERA-NET Co-fund programme, which has received funding from the European Union’s Horizon 2020 Research and Innovation Programme". Matteo Magnani (who granted the students access) is assumed to be paid by Uppsala Univesity.

__Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)?__ If not, please describe the time-frame in which the data associated with the instances was created.
Tweets were collected in 2023 of the period 30/11 to 12/12 2015. The authors created/downloaded this dataset in 2024.

__Were any ethical review processes conducted (e.g., by an institutional review board)?__ If so, please provide a description of these review processes, including the outcomes, as well as a link or other access point to any supporting documentation.
No.

__Does the dataset relate to people?__ If not, you may skip the remainder of the questions in this section.
Yes.

__Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?__
Third parties: [Uppsala Box](https://uppsala.app.box.com/s/ueb0dmz0c3yjhnt3kd95o34e1qg2zgi6)

__Were the individuals in question notified about the data collection?__ If so, please describe (or show with screenshots or other information) how notice was provided, and provide a link or other access point to, or otherwise reproduce, the exact language of the notification itself.
No.

__Did the individuals in question consent to the collection and use of their data?__ If so, please describe (or show with screenshots or other information) how consent was requested and provided, and provide a link or other access point to, or otherwise reproduce, the exact language to which the individuals consented.
No but the students as researchers have legitimate interest and are operating under instructions of their professor.

__If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?__ If so, please provide a description, as well as a link or other access point to the mechanism (if appropriate).
NA.

__Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis) been conducted?__ If so, please provide a description of this analysis, including the outcomes, as well as a link or other access point to any supporting documentation.
No.

__Any other comments?__


## Preprocessing/cleaning/labeling

__Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?__ If so, please provide a description. If not, you may skip the remainder of the questions in this section.
No.

__Was the _raw data_ saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?__ If so, please provide a link or other access point to the _raw data_.
No.

__Is the software used to preprocess/clean/label the instances available?__ If so, please provide a link or other access point.
NA

__Any other comments?__


## Uses

__Has the dataset been used for any tasks already?__ If so, please provide a description.
Not by the authors.

__Is there a repository that links to any or all papers or systems that use the dataset?__ If so, please provide a link or other access point.
No.

__What (other) tasks could the dataset be used for?__
Studying language, social interactions, climate change persuasion, training LLMs and identifying popular Twitter users within the subset.

__Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?__ For example, is there anything that a future user might need to know to avoid uses that could result in unfair treatment of individuals or groups (e.g., stereotyping, quality of service issues) or other undesirable harms (e.g., financial harms, legal risks) If so, please provide a description. Is there anything a future user could do to mitigate these undesirable harms?
No.

__Are there tasks for which the dataset should not be used?__ If so, please provide a description.
Training LLMs and identifying individuals.

__Any other comments?__


## Distribution

__Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created?__ If so, please provide a description.
No.

__How will the dataset will be distributed (e.g., tarball on website, API, GitHub)?__ Does the dataset have a digital object identifier (DOI)?
NA.

__When will the dataset be distributed?__
NA.

__Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?__ If so, please describe this license and/or ToU, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms or ToU, as well as any fees associated with these restrictions.
NA.

__Have any third parties imposed IP-based or other restrictions on the data associated with the instances?__ If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms, as well as any fees associated with these restrictions.
No.

__Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?__ If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any supporting documentation.
No.

__Any other comments?__


## Maintenance

__Who is supporting/hosting/maintaining the dataset?__
There is no support for this dataset.

__How can the owner/curator/manager of the dataset be contacted (e.g., email address)?__
Finn Vaughankraska: vaughankraska@gmail.com
Anand Mathew: anandmathewms@gmail.com

__Is there an erratum?__ If so, please provide a link or other access point.
No.

__Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?__ If so, please describe how often, by whom, and how updates will be communicated to users (e.g., mailing list, GitHub)?
Possibly. The users of this dataset should only be the authors so they will notify eachother of updates via Github. They authors may add the data to a database in order to more easily and performantly process it.

__If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)?__ If so, please describe these limits and explain how they will be enforced.
No, there are no limits on how long the data will be retained for. However, the authors do not intend to keep it longer than the 2024/2025 Uppsala University Fall Term.

__Will older versions of the dataset continue to be supported/hosted/maintained?__ If so, please describe how. If not, please describe how its obsolescence will be communicated to users.
No. The only backup version will be maintained and hosted as it was originally downloaed on upppsala.box.com. This is stated here and now.

__If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?__ If so, please provide a description. Will these contributions be validated/verified? If so, please describe how. If not, why not? Is there a process for communicating/distributing these contributions to other users? If so, please provide a description.
No.

__Any other comments?__

[^1]: From: Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., III, H. D., & Crawford, K. (2021). Datasheets for datasets. Commun. ACM, 64(12), 86�92. https://doi.org/10.1145/3458723
