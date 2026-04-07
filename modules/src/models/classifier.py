import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AdamW
import logging

class LightweightClassifier:
    def __init__(self, model_name="ai4bharat/IndicBERT-v2", num_labels=7):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not torch.cuda.is_available():
            logging.warning("CUDA unavailable! Training will be exceedingly slow.")
            
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # We must add our custom boundary marker so the model embeds it or ignores it safely
        self.tokenizer.add_special_tokens({'additional_special_tokens': ['▁']})
        
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.to(self.device)

        # Learning rate fixed at 2e-5 as per methodology [cite: 157]
        self.optimizer = AdamW(self.model.parameters(), lr=2e-5)

    def train_epoch(self, dataloader: DataLoader, accumulation_steps=4):
        """
        Implements gradient accumulation to handle 4GB VRAM constraints.
        Simulates a larger batch size by accumulating gradients over several mini-batches.
        """
        self.model.train()
        total_loss = 0
        
        for step, batch in enumerate(dataloader):
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)

            outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss / accumulation_steps # Normalize loss
            loss.backward()

            if (step + 1) % accumulation_steps == 0:
                self.optimizer.step()
                self.optimizer.zero_grad()

            total_loss += loss.item() * accumulation_steps
            
        return total_loss / len(dataloader)