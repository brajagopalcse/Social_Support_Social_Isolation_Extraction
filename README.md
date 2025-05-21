# Using Natural Language Processing to Identify  Social Support and Social Isolation from Electronic Health Records of Psychiatric Patients: A Multi-Site Study

This repository maintains the code for identifying social support and social isolation with fine-grained categories (presence or absence of social network, emotional support, instrumental support, general and loneliness) using rule- and large language models (LLM)-based algorithms. 

## 1. For running rule-based algorithm
	python rule_based_classification.py

## 2. For running LLM 

### for fine-tunning the models
	python llm_fine_tune_all.py

### for testing the models
	python llm_sentence_classification_fine_tuned.py

We will update the GPU version of the LLM code soon. 


## Reference

Please cite the following paper if you find this code useful.

_Patra, B. G., Lepow, L. A., Kumar, P. K. R. J., Vekaria, V., Sharma, M. M., Adekkanattu, P., Fennessy, B., Hynes, G., Landi, I., Sanchez-Ruiz, J. A., Ryu, E., Biernacka, J. M., Nadkarni, G. M., Talati, A., Weissman, M., Olfson, M., Mann, J. J., Charney, A. W., & Pathak, J. (2024). Extracting Social Support and Social Isolation Information from Clinical Psychiatry Notes: Comparing a Rule-based Natural Language Processing System and a Large Language Model. Journal of the American Medical Informatics Association, Volume 32, Issue 1, January 2025, Pages 218–226, https://doi.org/10.1093/jamia/ocae260_

Please contact brajagopal[dot]cse[at]gmail[dot]com for further information. 

