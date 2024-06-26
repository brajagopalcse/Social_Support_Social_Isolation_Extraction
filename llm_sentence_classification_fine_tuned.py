# -*- coding: utf-8 -*-
"""This code performs classification of sentences based on fine_tuned models. """

import os
os.environ["HF_ENDPOINT"] = "https://huggingface.co"
import pandas as pd
from load_documents import LoadDocuments
from transformers import T5Tokenizer, T5ForConditionalGeneration
from llm_utility import LLM_Utility


class LLMSentenceClassification:

    def __init__(self):
        self.llm_utility = LLM_Utility()
        self.load_docs = LoadDocuments()
        # using the base model
        self.tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-xl', cache_dir='google/flan-t5-tokenizer')
        self.model = None

    def load_model(self, category):
        """
        Loading models for different fine-grained categories.
        :param category: (str) fine-grained category name
        :return model: (T5ForConditionalGeneration) model for FLAN with ia3 adapter
        """
        if category == 'social_isolation_loneliness':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/si_l/flan-t5-xl")
        elif category == 'social_isolation_no_social_network':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/si_no_sn/flan-t5-xl")
        elif category == 'social_isolation_no_instrumental_support':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/si_no_is/flan-t5-xl")
        elif category == 'social_isolation_no_emotional_support':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/si_no_es/flan-t5-xl")
        elif category == 'social_isolation_general':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/si_g/flan-t5-xl")
        elif category == 'social_support_social_network':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/su_sn/flan-t5-xl")
        elif category == 'social_support_instrumental_support':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/su_is/flan-t5-xl")
        elif category == 'social_support_general':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/su_g/flan-t5-xl")
        elif category == 'social_support_emotional_support':
            self.model = T5ForConditionalGeneration.from_pretrained("tuned_model/su_es/flan-t5-xl")
        else:
            print('Category is something else: ', category)
            import sys
            sys.exit(1)
        self.model.set_active_adapters("ia3_adapter")

    def process(self):
        # load datasets from BRAT annotation
        annotated_data = self.load_docs.get_annotations(
            './Psych_notes/annotation_sisu_psych_notes_final/support_notes/',
            './Psych_notes/annotation_sisu_psych_notes_final/social_support_files.csv')
        annotated_data.update(self.load_docs.get_annotations(
            './Psych_notes/annotation_sisu_psych_notes_final/isolation_notes/',
            './Psych_notes/annotation_sisu_psych_notes_final/social_isolation_files.csv'))
        print('Total number of annotated files: ', len(annotated_data))
        sentence_categories_df = self.load_docs.convert_entity_to_sentence_category(annotated_data)
        pred_annotation = sentence_categories_df.copy()
        print(pred_annotation.shape)
        for category in self.load_docs.su_classes + self.load_docs.si_classes:
            # not classifying emotional categories for now
            if category == 'social_isolation_no_emotional_support' \
                    or category == 'social_support_emotional_support':
                print('Skipping {} category'.format(category))
                continue
            print('Processing {} category'.format(category))
            import time
            self.load_model(category)
            start_time = time.time()
            pred_annotation[category] = self.llm_utility.find_category(pred_annotation['sent_text'].tolist(), category,
                                                                       self.tokenizer, self.model)
            print('Total time for {} = {}'.format(category, time.time()-start_time))
        pred_annotation.to_csv('system_output_for_sentence_llm_fine_tuned.csv')
        pred_annotation = self.load_docs.convert_sentence_to_document_category(pred_annotation)
        true_annotation = self.load_docs.convert_sentence_to_document_category(sentence_categories_df, False)
        self.load_docs.calculate_iaa(true_annotation, pred_annotation)
        merged_results = pd.concat([true_annotation, pred_annotation], axis=1)
        merged_results.to_csv('annotation_vs_system_output_llm_fine_tuned.csv')


def main():
    LLMSentenceClassification().process()


if __name__ == '__main__':
    main()