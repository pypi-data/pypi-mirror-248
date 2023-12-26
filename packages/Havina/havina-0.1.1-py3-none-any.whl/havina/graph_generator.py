import multiprocessing

import havina.entity_finding as ef
import havina.language_model as lm
from multiprocessing import Pool
import havina.filters as fs
import os


class GraphGenerator:
    def __init__(
            self,
            top_k=4,
            threshold=0.015,
            link_entity=False,
            model='bert',
            contiguous_token=True,
            forward_tokens=True,
            frequency=1,
            relation_length=8,
            resolve_reference=True,
            device=None):
        """
        Initialize the graph generator class with the following parameters:
        :param top_k: Number of candidates to select for the next iteration of the beam search
        :param threshold: Discard a relation if its accumulated attention score is below this threshold
        :param link_entity: Link head and tail entities using Wikidata database
        :param model: Language model to extract attention scores from
        :param contiguous_token: When generating relations, consider only those with contiguous tokens
        :param forward_tokens: When filtering relations, remove those whose order of words do not follow that of the
        text. (i.e. if the input is 'I love beautiful cars', a relation like 'beautiful love' would be removed)
        :param frequency: The frequency cutoff. If a relation appears less than 'frequency' in the text corpus, it
        will not be accounted.
        :param relation_length: Maximum quantity of tokens allowed in a relation.
        :param resolve_reference: Resolve cross-references, i.e. replace pronouns (e.g. 'he') by the noun they refer to
        :param device: Pytorch device in which to run the language model

        The word tokens refer not to words but to the items in a tokenized sentence, prepared to be the input of the
        language model.
        """
        self.top_k = top_k
        self.threshold = threshold
        self.link_entity = link_entity
        self.model = model
        self.contiguous_token = contiguous_token
        self.forward_tokens = forward_tokens
        self.frequency = frequency
        self.relation_length = relation_length
        self.device = device
        self.resolve_reference = resolve_reference

    def __call__(self, sentence: str, workers=1) -> list[fs.HeadTailRelations]:
        """
        Processes an input sentence and returns a list of head and tails and their corresponding relations.

        :param sentence: A string to be processed
        :param workers: The number of processes to create for splitting the work
        :return: A list of head and tails entities and their corresponding relations
        """

        model = lm.get_model(self.model, self.device)
        processed_sentence = ef.Sentence(sentence, model, self.link_entity, self.resolve_reference)
        model_input, noun_chunks = processed_sentence.prepare()
        self.attention = model.inference_attention(model_input).to('cpu').detach()

        ht_pairs = ef.create_ht_pairs(noun_chunks, processed_sentence, self.link_entity)
        self.ind_filter = fs.IndividualFilter(processed_sentence, self.forward_tokens, self.threshold)

        relations: list[fs.HeadTailRelations] = []
        if workers <= 0:
            raise Exception('Invalid number of workers')
        elif workers == 1:
            for idx, item in enumerate(ht_pairs):
                relations.append(self.worker(item))
        else:
            os.environ['TOKENIZERS_PARALLELISM'] = 'true'
            try:
                multiprocessing.set_start_method('fork')
            except RuntimeError:
                pass
            with Pool(workers) as p:
                for item in p.imap_unordered(self.worker, ht_pairs):
                    relations.append(item)

        fs.frequency_cutoff(relations, self.frequency)

        # Clean up references
        self.ind_filter = None
        self.attention = None

        return clean_relations(relations)

    def worker(self, pair: ef.HtPair) -> fs.HeadTailRelations:
        candidates = ef.search_pass(self.attention, pair, self.top_k, self.contiguous_token, self.relation_length)
        return self.ind_filter.filter(candidates, pair)


def clean_relations(ht_pairs: list[fs.HeadTailRelations]) -> list[fs.HeadTailRelations]:
    unique_relations = set()
    for ht_pair in ht_pairs:
        filtered_relations = []
        for relation in ht_pair.relations:
            unique_key = ht_pair.head.text + "|" + relation + "|" + ht_pair.tail.text
            reverse_key = ht_pair.tail.text + "|" + relation + "|" + ht_pair.head.text
            if unique_key not in unique_relations and reverse_key not in unique_relations:
                filtered_relations.append(relation)
                unique_relations.add(unique_key)
        ht_pair.relations = filtered_relations

    new_list = [pair for pair in ht_pairs if len(pair.relations) > 0 and
                (pair.head.wikidata_id != pair.tail.wikidata_id
                 or pair.head.text != pair.tail.text)]

    return new_list
