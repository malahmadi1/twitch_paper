import torch

def my_collate(batches):
    # return batches
    return [{key: torch.stack(value) for key, value in batch.items()} for batch in batches]


def prepare_batch_for_model(batch, device='cuda', fine_tune=True):

    # Prepare batch for model 

    ids = [data["ids"] for data in batch]
    mask = [data["mask"] for data in batch]
    token_type_ids = [data["token_type_ids"] for data in batch]

    if fine_tune:
        targets = [data["targets"][0] for data in batch]
        targets = torch.stack(targets)
    else:
        targets = [data["targets"] for data in batch]
        targets = torch.cat(targets)
    lengt = [data['len'] for data in batch]

    ids = torch.cat(ids)
    mask = torch.cat(mask)
    token_type_ids = torch.cat(token_type_ids)
    
    lengt = torch.cat(lengt)
    lengt = [x.item() for x in lengt]

    ids = ids.to(device, dtype=torch.long)
    mask = mask.to(device, dtype=torch.long)
    token_type_ids = token_type_ids.to(device, dtype=torch.long)
    targets = targets.to(device, dtype=torch.long)

    return ids, mask, token_type_ids, targets, lengt