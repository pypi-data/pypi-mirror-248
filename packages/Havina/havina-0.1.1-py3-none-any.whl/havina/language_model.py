import torch
import transformers


class LanguageModel:
    def __init__(self, device):
        self.device = device

    def init_token_idx_2_word_doc_idx(self) -> list[tuple[str, int]]:
        pass

    def num_start_tokens(self) -> int:
        pass

    def append_last_token(self, listing: list[tuple[str, int]]):
        pass

    def model_input(self, tokenized_sequence: list[int]) -> dict[str, torch.Tensor]:
        pass

    def tokenize(self, word: str):
        pass

    def inference_attention(self, model_input: dict[str, torch.Tensor]):
        pass


class BertModel(LanguageModel):
    def __init__(self, device):
        super().__init__(device)
        self.tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = transformers.BertModel.from_pretrained('bert-base-uncased').to(self.device)

    def init_token_idx_2_word_doc_idx(self) -> list[tuple[str, int]]:
        return [('CLS', -1)]

    def num_start_tokens(self) -> int:
        return 1

    def append_last_token(self, listing: list[tuple[str, int]]):
        listing.append(('SEP', len(listing)))

    def model_input(self, tokenized_sentence: list[int]) -> dict[str, torch.Tensor]:
        tokenized_sentence = [self.tokenizer.cls_token_id] + tokenized_sentence + [self.tokenizer.sep_token_id]
        input_dict = {
            'input_ids': torch.tensor(tokenized_sentence, device=self.device).long().unsqueeze(0),
            'token_type_ids': torch.zeros(len(tokenized_sentence), device=self.device).long().unsqueeze(0),
            'attention_mask': torch.ones(len(tokenized_sentence), device=self.device).long().unsqueeze(0),
        }
        return input_dict

    def tokenize(self, word):
        return self.tokenizer(str(word), add_special_tokens=False)['input_ids']

    def inference_attention(self, model_input: dict[str, torch.Tensor]) -> torch.Tensor:
        output = self.model(**model_input, output_attentions=True)
        last_att_layer = output.attentions[-1]
        mean = torch.mean(last_att_layer, dim=1)
        return mean[0]


def get_model(model: str, device) -> LanguageModel:
    if model == 'bert':
        return BertModel(device)

    raise Exception("Model not found")
