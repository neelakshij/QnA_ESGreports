# QnA_ESGreports
Question-and-Answer app to explore ESG reports using RAG-LLM

<img src="https://user-images.githubusercontent.com/neelakshij/QnA_ESGreports/images/kx-image.png" width="200" />

This project is developed as a part of KaagleX BIPOC mentorship program.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/images/kx-image.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/images/kx-image.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/images/kx-image.png">
</picture>


The project titled "Q-n-A with ESG report using LLM" is an end-to-end project based on Retrieval Augmentation Generation (RAG) concept where external information, in this case, ESG, i.e., Environmental-Social-Governance reports, are provided to large language models (LLM). 


Every company should produce a report informing how it accomplishes the responsibilities towards ESG complying with regulations. I have chosen reports of first 50 companies listed in S&P 500. ESG report is very important to gain trust of investors and stakeholders. Reports may be large with complex and cleverly written text. Manually finding all required information from the report can be tedious and time consuming. This is the motivation behind this project where user can get concise response along with referred page numbers from the report against their query. 


Front end of the app collects year, company name and query from the user, and then displays response with source page numbers. In the backend, report is fetched from bucket/repository. It gets processed to obtain embeddings.Then LLM retrieves related text chunks and creates concise response. Also returns the corresponding page numbers from metadata associated to text-chunks. 


This project is created on Google Cloud Platform (GCP). Reports are collected by web scrapping and stored in GCP Bucket. To render Streamlit app from GCP, the project use local tunnel and ipv4 utilities.
