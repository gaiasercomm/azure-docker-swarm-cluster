How-To deploy swarm cluster to azure
===
Reference: azure-docker-swarm-cluster, https://github.com/rcarmo/azure-docker-swarm-cluster

1. Deploy swarm cluster

  * Mome files should be modified for python compatibility.
    - genparams.py

      ```python
      - return b64encode(bytes(buffer, 'utf-8')).decode()

      + return b64encode(bytes(buffer).encode('utf-8')).decode()
      ```


  * Modify Makefile to specify location.
    - Makefile

      ```
      export LOCATION?=southeastasia
      ```

  * Modify deployment template.

    If the region where your `availability set is` located has only 2 managed fault domains but the number of unmanaged fault domains is 3, this command shows an error similar to "The specified fault domain count 3 must fall in the range 1 to 2." To resolve the error, update the fault domain to 2.

    reference: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/convert-unmanaged-to-managed-disks

      ```
      # Error Activity Log
      Operation name
      Create or Update Availability Set

      Time stamp
      Fri Mar 15 2019 13:25:36 GMT+0800 (Taipei Standard Time)

      Event initiated by
      xxx@sercommgaia.onmicrosoft.com

      Error code
      InvalidParameter

      Message
      The specified fault domain count 3 must fall in the range 1 to 2.
      ```

    - cluster.json

      ```json
      "asFDCount": {
        "type": "int",
      -  "defaultValue": 3,
      +  "defaultValue": 2,
      ```

  * Modify autoscale setting rule

    - cluster.json

      ```json
      "comments": "Autoscale Settings",
      "type": "microsoft.insights/autoscalesettings",
      "properties": {
        "profiles": [
          {
            "name": "DefaultProfile",
            "capacity": {
      -       "minimum": "1",
              "maximum": "10",
      -       "default": "2"
      +       "minimum": "3",
              "maximum": "10",
      +       "default": "3"
            },
      ```

  * Deploy cluster

    ```sh
    # Generate keys
    $ make keys
    $ make params

    # Deploy SWARM cluster
    $ make deploy-cluster
    ```

  * Deploy visualizer

    ```sh
    $ make deploy-monitor
    ```
    browse visualizer at http://swarm-cluster-master0.southeastasia.cloudapp.azure.com:8080/

  * Deploy global service

    ```sh
    $ make deploy-global-service
    ```
    browse global service at http://swarm-cluster-master0.southeastasia.cloudapp.azure.com:81/

  * Deploy replicated service

    ```sh
    $ make deploy-replicated-service
    ```
    browse replicated service at http://swarm-cluster-master0.southeastasia.cloudapp.azure.com:80/

  * Scale replicated service

    ```sh
    # specify the total number of replicated containers to placehold '%'.
    $ make scale-service-%
    ```

  * List & Scale VMSS instances
    ```sh
    $ make list-agents
    # specify the total number of vmss to placehold '%'.
    $ make scale-agents-%
    ```
