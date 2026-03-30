import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "lucas-leme/FinBERT-PT-BR"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


def processar_atas_individual(texto):

    # tokenização com janelamento para lidar com o textos grandes das atas
    inputs = tokenizer(
        texto,
        return_tensors="pt",
        truncation=True,
        max_length=512,  # limite do modelo
        stride=128,  # carrega os últimos 128 para o proximo batch
        return_overflowing_tokens=True,
        padding=True,
    )

    input_ids = inputs["input_ids"]

    scores_janela = []

    # inferencia para cada janela de texto
    model.eval()
    with torch.no_grad():
        for i in range(input_ids.shape[0]):
            outputs = model(input_ids[i].unsqueeze(0))

            probs = F.softmax(outputs.logits, dim=-1)
            scores_janela.append(probs)

    if not scores_janela:
        return None

    media_final = torch.mean(torch.stack(scores_janela), dim=0).squeeze()

    return {
        "positivo": media_final[0].item(),
        "negativo": media_final[1].item(),
        "neutro": media_final[2].item(),
    }
