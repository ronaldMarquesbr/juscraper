def get_dataset_items(client, dataset_id):
    dataset = client.dataset(dataset_id)
    return list(dataset.iterate_items())
