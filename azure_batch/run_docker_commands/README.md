# Run Docker commands directly on an Azure Batch Pool

**NOTE:** Running Docker (`docker run ...`) commands directly on an Azure Batch Pool generally results in an execution on a single node. Running workloads in such a way does not scale as the recommended way, which is described [here](https://docs.microsoft.com/en-us/azure/batch/batch-docker-container-workloads).

## Prerequisites

- Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Create a [Batch Account](https://docs.microsoft.com/en-us/azure/batch/quick-create-cli)
- Create a [Storage Account](https://docs.microsoft.com/en-us/azure/storage/common/storage-quickstart-create-account?tabs=azure-portal)
- Create a [Blob container in the Storage Account and upload the .sh script in this repository](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal)

## Adjust settings in `pool-parameters.json`

You can change the following parameters:

- Name of the Azure Batch Pool: Change the `value` parameter of `poolId`.
- SKU of the Azure Batch Pool: Change the `value` parameter of `poolSku`.
- Number of Nodes of the Azure Batch Pool: Change the `value` parameter of `nodeCount`. Most workloads will not scale accross multiple nodes, which is why scale out is not recommended.
- Name of the Storage Account where the .sh script is saved: Change the `value` parameter of `storageAccountName`.
- Name of the Storage Account Container name where the .sh script is saved: Change the `value` parameter of `storageAccountContainerName`.

## Create a new pool with Azure CLI

You can create a new Batch Pool using the , the `pool-definition.json` and the `pool-parameters.json`. To create a batch pool execute the following commands:

1. Install  the latest version of the Batch extension: `az extension add --name azure-batch-cli-extensions`.
2. Create a new Azure Batch Pool: `az batch pool create --template pool-definition.json --parameters pool-parameters.json --account-name <your-batch-account-name> --account-endpoint <your-batch-endpoint>`

## Run Docker commands on your batch pool

Now you can run `docker` commands on your batch pool and e.g. directly submit docker workloads from Azure Data Factory by running: `sudo docker run hello-world`.
For more details please read the following [link](https://docs.microsoft.com/en-us/azure/data-factory/transform-data-using-dotnet-custom-activity).
