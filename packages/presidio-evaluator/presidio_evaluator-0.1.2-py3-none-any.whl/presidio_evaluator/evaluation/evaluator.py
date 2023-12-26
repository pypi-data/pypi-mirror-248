from collections import Counter
from typing import List, Optional, Dict
from pathlib import Path

import numpy as np
from tqdm import tqdm

import plotly.express as px
import pandas as pd

from presidio_evaluator import InputSample
from presidio_evaluator.evaluation import EvaluationResult, ModelError
from presidio_evaluator.models import BaseModel


class Evaluator:
    def __init__(
        self,
        model: BaseModel,
        verbose: bool = False,
        compare_by_io=True,
        entities_to_keep: Optional[List[str]] = None,
    ):
        """
        Evaluate a PII detection model or a Presidio analyzer / recognizer

        :param model: Instance of a fitted model (of base type BaseModel)
        :param compare_by_io: True if comparison should be done on the entity
        level and not the sub-entity level
        :param entities_to_keep: List of entity names to focus the evaluator on (and ignore the rest).
        Default is None = all entities. If the provided model has a list of entities to keep,
        this list would be used for evaluation.
        """
        self.model = model
        self.verbose = verbose
        self.compare_by_io = compare_by_io
        self.entities_to_keep = entities_to_keep
        if self.entities_to_keep is None and self.model.entities:
            self.entities_to_keep = self.model.entities

    def compare(self, input_sample: InputSample, prediction: List[str]):

        """
        Compares ground truth tags (annotation) and predicted (prediction)
        :param input_sample: input sample containing list of tags with scheme
        :param prediction: predicted value for each token
        self.labeling_scheme

        """
        annotation = input_sample.tags
        tokens = input_sample.tokens

        if len(annotation) != len(prediction):
            print(
                "Annotation and prediction do not have the"
                "same length. Sample={}".format(input_sample)
            )
            return Counter(), []

        results = Counter()
        mistakes = []

        new_annotation = annotation.copy()

        if self.compare_by_io:
            new_annotation = self._to_io(new_annotation)
            prediction = self._to_io(prediction)

        # Ignore annotations that aren't in the list of
        # requested entities.
        if self.entities_to_keep:
            prediction = self._adjust_per_entities(prediction)
            new_annotation = self._adjust_per_entities(new_annotation)
        for i in range(0, len(new_annotation)):
            results[(new_annotation[i], prediction[i])] += 1

            if self.verbose:
                print("Annotation:", new_annotation[i])
                print("Prediction:", prediction[i])
                print(results)

            # check if there was an error
            is_error = new_annotation[i] != prediction[i]
            if is_error:
                if prediction[i] == "O":
                    mistakes.append(
                        ModelError(
                            error_type="FN",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )
                elif new_annotation[i] == "O":
                    mistakes.append(
                        ModelError(
                            error_type="FP",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )
                else:
                    mistakes.append(
                        ModelError(
                            error_type="Wrong entity",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )

        return results, mistakes

    def _adjust_per_entities(self, tags):
        if self.entities_to_keep:
            return [tag if tag in self.entities_to_keep else "O" for tag in tags]
        else:
            return tags

    @staticmethod
    def _to_io(tags):
        """
        Translates BILUO/BIO/IOB to IO - only In or Out of entity.
        ['B-PERSON','I-PERSON','L-PERSON'] is translated into
        ['PERSON','PERSON','PERSON']
        :param tags: the input tags in BILUO/IOB/BIO format
        :return: a new list of IO tags
        """
        return [tag[2:] if "-" in tag else tag for tag in tags]

    def evaluate_sample(
        self, sample: InputSample, prediction: List[str]
    ) -> EvaluationResult:
        if self.verbose:
            print("Input sentence: {}".format(sample.full_text))

        results, mistakes = self.compare(input_sample=sample, prediction=prediction)
        return EvaluationResult(results, mistakes, sample.full_text)

    def evaluate_all(self, dataset: List[InputSample]) -> List[EvaluationResult]:
        evaluation_results = []
        if self.model.entity_mapping:
            print(
                f"Mapping entity values using this dictionary: {self.model.entity_mapping}"
            )
        for sample in tqdm(dataset, desc=f"Evaluating {self.model.__class__}"):

            # Align tag values to the ones expected by the model
            self.model.align_entity_types(sample)

            # Predict
            prediction = self.model.predict(sample)

            # Remove entities not requested
            prediction = self.model.filter_tags_in_supported_entities(prediction)

            # Switch to requested labeling scheme (IO/BIO/BILUO)
            prediction = self.model.to_scheme(prediction)

            evaluation_result = self.evaluate_sample(
                sample=sample, prediction=prediction
            )
            evaluation_results.append(evaluation_result)

        return evaluation_results

    @staticmethod
    def align_entity_types(
        input_samples: List[InputSample],
        entities_mapping: Dict[str, str] = None,
        allow_missing_mappings: bool = False,
    ) -> List[InputSample]:
        """
        Change input samples to conform with Presidio's entities
        :return: new list of InputSample
        """

        new_input_samples = input_samples.copy()

        # A list that will contain updated input samples,
        new_list = []

        for input_sample in new_input_samples:
            contains_field_in_mapping = False
            new_spans = []
            # Update spans to match the entity types in the values of entities_mapping
            for span in input_sample.spans:
                if span.entity_type in entities_mapping.keys():
                    new_name = entities_mapping.get(span.entity_type)
                    span.entity_type = new_name
                    contains_field_in_mapping = True

                    new_spans.append(span)
                else:
                    if not allow_missing_mappings:
                        raise ValueError(
                            f"Key {span.entity_type} cannot be found in the provided entities_mapping"
                        )
            input_sample.spans = new_spans

            # Update tags in case this sample has relevant entities for evaluation
            if contains_field_in_mapping:
                for i, tag in enumerate(input_sample.tags):
                    has_prefix = "-" in tag
                    if has_prefix:
                        prefix = tag[:2]
                        clean = tag[2:]
                    else:
                        prefix = ""
                        clean = tag

                    if clean in entities_mapping.keys():
                        new_name = entities_mapping.get(clean)
                        input_sample.tags[i] = "{}{}".format(prefix, new_name)
                    else:
                        input_sample.tags[i] = "O"

            new_list.append(input_sample)

        return new_list
        # Iterate on all samples

    def calculate_score(
        self,
        evaluation_results: List[EvaluationResult],
        entities: Optional[List[str]] = None,
        beta: float = 2.5,
    ) -> EvaluationResult:
        """
        Returns the pii_precision, pii_recall, f_measure either and number of records for each entity
        or for all entities (ignore_entity_type = True)
        :param evaluation_results: List of EvaluationResult
        :param entities: List of entities to calculate score to. Default is None: all entities
        :param beta: F measure beta value
        between different entity types, or to treat these as misclassifications
        :return: EvaluationResult with precision, recall and f measures
        """

        # aggregate results
        all_results = sum([er.results for er in evaluation_results], Counter())

        # compute pii_recall per entity
        entity_recall = {}
        entity_precision = {}
        n = {}
        if not entities:
            entities = list(set([x[0] for x in all_results.keys() if x[0] != "O"]))

        for entity in entities:
            # all annotation of given type
            annotated = sum([all_results[x] for x in all_results if x[0] == entity])
            predicted = sum([all_results[x] for x in all_results if x[1] == entity])
            n[entity] = annotated
            tp = all_results[(entity, entity)]

            if annotated > 0:
                entity_recall[entity] = tp / annotated
            else:
                entity_recall[entity] = np.NaN

            if predicted > 0:
                per_entity_tp = all_results[(entity, entity)]
                entity_precision[entity] = per_entity_tp / predicted
            else:
                entity_precision[entity] = np.NaN

        # compute pii_precision and pii_recall
        annotated_all = sum([all_results[x] for x in all_results if x[0] != "O"])
        predicted_all = sum([all_results[x] for x in all_results if x[1] != "O"])
        if annotated_all > 0:
            pii_recall = (
                sum(
                    [
                        all_results[x]
                        for x in all_results
                        if (x[0] != "O" and x[1] != "O")
                    ]
                )
                / annotated_all
            )
        else:
            pii_recall = np.NaN
        if predicted_all > 0:
            pii_precision = (
                sum(
                    [
                        all_results[x]
                        for x in all_results
                        if (x[0] != "O" and x[1] != "O")
                    ]
                )
                / predicted_all
            )
        else:
            pii_precision = np.NaN
        # compute pii_f_beta-score
        pii_f_beta = self.f_beta(pii_precision, pii_recall, beta)

        # aggregate errors
        errors = []
        for res in evaluation_results:
            if res.model_errors:
                errors.extend(res.model_errors)

        evaluation_result = EvaluationResult(
            results=all_results,
            model_errors=errors,
            pii_precision=pii_precision,
            pii_recall=pii_recall,
            entity_recall_dict=entity_recall,
            entity_precision_dict=entity_precision,
            n_dict=n,
            pii_f=pii_f_beta,
            n=sum(n.values()),
        )

        return evaluation_result

    @staticmethod
    def precision(tp: int, fp: int) -> float:
        return tp / (tp + fp + 1e-100)

    @staticmethod
    def recall(tp: int, fn: int) -> float:
        return tp / (tp + fn + 1e-100)

    @staticmethod
    def f_beta(precision: float, recall: float, beta: float) -> float:
        """
        Returns the F score for precision, recall and a beta parameter
        :param precision: a float with the precision value
        :param recall: a float with the recall value
        :param beta: a float with the beta parameter of the F measure,
        which gives more or less weight to precision
        vs. recall
        :return: a float value of the f(beta) measure.
        """
        if np.isnan(precision) or np.isnan(recall) or (precision == 0 and recall == 0):
            return np.nan

        return ((1 + beta ** 2) * precision * recall) / (
            ((beta ** 2) * precision) + recall
        )

    class Plotter:
        """
        Plot scores (f2, precision, recall) and errors (false-positivies, false-negatives) 
        for a PII detection model evaluated via Evaluator

        :param model: Instance of a fitted model (of base type BaseModel)
        :param results: results given by evaluator.calculate_score(evaluation_results)
        :param output_folder: folder to store plots and errors in
        :param model_name: name of the model to be used in the plot title
        :param beta: a float with the beta parameter of the F measure,
        which gives more or less weight to precision vs. recall
        """

        def __init__(self, model, results, output_folder: Path, model_name: str, beta: float):
            self.model = model
            self.results = results
            self.output_folder = output_folder
            self.model_name = model_name.replace("/", "-")
            self.errors = results.model_errors
            self.beta = beta

        def plot_scores(self) -> None:
            """
            Plots per-entity recall, precision, or F2 score for evaluated model. 
            :param plot_type: which metric to graph (default is F2 score)
            """
            scores = {}
            scores['entity'] = list(self.results.entity_recall_dict.keys())
            scores['recall'] = list(self.results.entity_recall_dict.values())
            scores['precision'] = list(self.results.entity_precision_dict.values())
            scores['count'] = list(self.results.n_dict.values())
            scores[f"f{self.beta}_score"] = [Evaluator.f_beta(precision=precision, recall=recall, beta=self.beta)
                                  for recall, precision in zip(scores['recall'], scores['precision'])]
            df = pd.DataFrame(scores)
            df['model'] = self.model_name
            self._plot(df, plot_type="f2_score")
            self._plot(df, plot_type="precision")
            self._plot(df, plot_type="recall")

        def _plot(self, df, plot_type) -> None:
            fig = px.bar(df, text_auto=".2", y='entity', orientation="h",
                         x=plot_type, color='count', barmode='group', title=f"Per-entity {plot_type} for {self.model_name}")
            fig.update_layout(barmode='group', yaxis={
                'categoryorder': 'total ascending'})
            fig.update_layout(yaxis_title=f"{plot_type}", xaxis_title="PII Entity")
            fig.update_traces(textfont_size=12, textangle=0,
                              textposition="outside", cliponaxis=False)
            fig.update_layout(
                plot_bgcolor="#FFF",
                xaxis=dict(
                    title="PII entity",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
                yaxis=dict(
                    title=f"{plot_type}",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
            )
            fig.show()

        def plot_most_common_tokens(self) -> None:
            """Graph most common false positive and false negative tokens for each entity."""
            ModelError.most_common_fp_tokens(self.errors)
            fps_frames = []
            fns_frames = []
            for entity in self.model.entity_mapping.values():
                fps_df = ModelError.get_fps_dataframe(self.errors, entity=[entity])
                if fps_df is not None:
                    fps_path = self.output_folder / \
                        f"{self.model_name}-{entity}-fps.csv"
                    fps_df.to_csv(fps_path)
                    fps_frames.append(fps_path)
                fns_df = ModelError.get_fns_dataframe(self.errors, entity=[entity])
                if fns_df is not None:
                    fns_path = self.output_folder / \
                        f"{self.model_name}-{entity}-fns.csv"
                    fns_df.to_csv(fns_path)
                    fns_frames.append(fns_path)

            def group_tokens(df):
                return df.groupby(['token', 'annotation']).size().to_frame(
                ).sort_values([0], ascending=False).head(3).reset_index()

            fps_tokens_df = pd.concat(
                [group_tokens(pd.read_csv(df_path)) for df_path in fps_frames])
            fns_tokens_df = pd.concat(
                [group_tokens(pd.read_csv(df_path)) for df_path in fns_frames])

            def generate_graph(title, tokens_df):
                fig = px.histogram(tokens_df, x=0, y="token", orientation='h', color='annotation',
                                   title=f"Most common {title} for {self.model_name}")

                fig.update_layout(yaxis_title=f"count", xaxis_title="PII Entity")
                fig.update_traces(textfont_size=12, textangle=0,
                                  textposition="outside", cliponaxis=False)
                fig.update_layout(
                    plot_bgcolor="#FFF",
                    xaxis=dict(
                        title="Count",
                        linecolor="#BCCCDC",  # Sets color of X-axis line
                        showgrid=False  # Removes X-axis grid lines
                    ),
                    yaxis=dict(
                        title=f"Tokens",
                        linecolor="#BCCCDC",  # Sets color of X-axis line
                        showgrid=False  # Removes X-axis grid lines
                    ),
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                fig.show()
            generate_graph(title="false-negatives", tokens_df=fns_tokens_df)
            generate_graph(title="false-positives", tokens_df=fps_tokens_df)
