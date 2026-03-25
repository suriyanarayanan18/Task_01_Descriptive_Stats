# Findings: 2024 Facebook Political Ads Dataset

## Introduction

This analysis examines 246,745 Facebook ad records from the 2024 U.S. Presidential election cycle. Each row represents a single ad purchase where at least one presidential candidate was mentioned. The data spans from mid-2021 through November 2024, though the vast majority of activity is concentrated in the final months before Election Day. The goal of this analysis was to understand who was spending, how much, when, and on what topics.

## Spending is Heavily Concentrated

Political ad spending on Facebook is not evenly distributed. The top two organizations by ad volume, HARRIS FOR PRESIDENT (49,788 ads) and HARRIS VICTORY FUND (32,612 ads), together account for roughly one-third of all ads in the dataset. On the Trump side, spending was spread across more entities: DONALD J. TRUMP FOR PRESIDENT 2024, INC. (15,112), Trump National Committee JFC (7,279), and TRUMP 47 COMMITTEE, INC. (5,027).

The Harris campaign's consolidated approach meant that a single byline dominated the dataset, while the Trump campaign's spending was fragmented across multiple fundraising committees and PACs. Whether this reflects a strategic difference in campaign structure or just how the organizations were registered is worth further investigation.

The spend distribution itself is dramatically right-skewed. The median ad spend was just $49.50, while the mean was $1,062. This tells us that the vast majority of ads were low-budget purchases under $100, but a small number of high-spend ads (up to $475,000) pulled the average up significantly. Over 135,000 ads (55% of the dataset) fell in the $0-$99 range.

## Ad Volume Ramped Up Sharply Before Election Day

The timeline of ad creation shows near-zero activity through most of 2021-2023, with a gradual increase starting in early 2024 and an explosive ramp-up in October 2024. The highest single day for ad creation was October 27, 2024, with 8,619 ads created just nine days before the election.

The most common ad delivery stop date was November 5, 2024 (Election Day itself), with 14,222 ads ending that day. This makes sense as campaigns would have no reason to continue running political ads after votes were cast. The 2,159 ads with no stop date may have still been running when the data was collected, or the stop date may not have been recorded for other reasons.

## Platform Strategy is Uniform

An overwhelming 86.9% of ads were deployed to both Facebook and Instagram simultaneously. Only 9.4% targeted Facebook alone, and 3.4% targeted Instagram alone. Less than 1% used other placements like Audience Network or Messenger.

This suggests that cross-platform deployment is the default strategy for political advertisers on Meta's platforms. There is very little evidence of campaigns tailoring their platform choice on a per-ad basis.

## Advocacy and Fundraising Dominated Messaging

Looking at the message type flags, 54.9% of ads were classified as advocacy and 57.3% included a call to action. Fundraising was the purpose of 22.9% of ads, while 14.4% were focused on voting. Attack ads made up 27.2% of the dataset, meaning roughly one in four political ads was designed to criticize an opponent rather than promote a candidate.

Among topics, the economy (12.2%) and health (10.9%) were the most common issues referenced. Social and cultural topics appeared in 10.6% of ads. Immigration (3.4%), safety (3.4%), and women's issues (8.1%) also had notable presence. Foreign policy (0.5%), LGBTQ issues (0.3%), and military topics (0.2%) were rarely addressed in Facebook political ads.

## What Surprised Me

A few things stood out:

The dataset contains 18 different currencies, even though these are U.S. presidential election ads. While 246,599 out of 246,745 ads used USD, there were 63 ads in Indian Rupees, 17 in British Pounds, and smaller numbers in Euros, Pakistani Rupees, and Egyptian Pounds. This raises questions about foreign ad purchases targeting American elections.

The `illuminating_scored_message` column contains anonymized ad content. Interestingly, the two most frequent values appear to be identical except for letter casing (one lowercase, one uppercase), each appearing around 3,000 times. This is likely a data quality issue where the same ad was recorded inconsistently.

Despite the Harris campaign running significantly more ads (over 82,000 across HARRIS FOR PRESIDENT and HARRIS VICTORY FUND combined), Donald Trump was the most mentioned candidate in the dataset with 78,324 mentions compared to Kamala Harris at 53,239. This suggests that a large portion of Harris-aligned ads were focused on Trump rather than promoting Harris herself. The 27.2% attack ad rate across the dataset supports this interpretation. In political advertising, the opponent's name can appear as often as, or more than, the candidate being promoted.

Finally, 73,205 ads (29.7%) had no candidate mentions at all. These were ads that appeared in the political advertising dataset but did not specifically name any candidate. This could include issue-based ads from advocacy organizations that were flagged as political without directly referencing a candidate.