import requests
import json

#sucscriptionId and bearer are left blank for security
subscriptionId = ""
bearer = ""

defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "lab5"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
apiVersion = "2021-04-01"

def sendHttpRequest(url, json_data, headers):
    # Sending the POST request with the JSON payload
    response = requests.put(url, data=json_data, headers=headers)

    # Checks for answer
    if response.status_code == 200:
        print("Successful request")
        response_data = response.json()
        print("Response Data:", response_data)
    else:
        print(f"Error Request. Statuscode: {response.status_code}")

def createResourceGroup():
    global json_data, headers
    # create Resourcegroup
    urlCreateResourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"
    # JSON-Data, that you want to send
    createResourceGroupPayloadData = {
        "location": "westeurope"
    }
    # converts Python data to JSON
    json_data = json.dumps(createResourceGroupPayloadData)
    # Set the HTTP headers to set the content type to JSON
    headers = {"Authorization": f"Bearer {bearer}",
               'Content-Type': 'application/json'}
    sendHttpRequest(urlCreateResourceGroup, json_data, headers)

def createVirtualNetwork():
    global json_data
    # create virtual network
    urlCreateVirtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    payloadDataCreateVirtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVirtualNetwork)
    sendHttpRequest(urlCreateVirtualNetwork, json_data, headers)

def createSubnet():
    global json_data
    # create subnet
    urlCreateSubnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version=2023-05-01"
    payloadDataCreateSubnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }
    json_data = json.dumps(payloadDataCreateSubnet)
    sendHttpRequest(urlCreateSubnet, json_data, headers)

def createPublicIpAdress():
    global json_data
    # create public ip adress
    urlCreatePublicIPAdress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version=2023-05-01"
    payloadDataCreatePublicIpAdress = {
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreatePublicIpAdress)
    sendHttpRequest(urlCreatePublicIPAdress, json_data, headers)

def createNetworkInterface():
    global networkInterfaceName, json_data
    # create network interface
    networkInterfaceName = "nic4"
    urlCreateNetworkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version=2023-05-01"
    payloadDataCreateNetworkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateNetworkInterface)
    sendHttpRequest(urlCreateNetworkInterface, json_data, headers)

def createVm():
    global json_data
    # create VM
    urlCreateVM = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2023-07-01"
    payloadDataCreateVM = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "hell2",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/hell2/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC79rNjAkGJMczzkJGkaU/Qv+yKFUl3F0TdJQ/qDFs6g5XpUiyKsnyma2IdhwXRMP00bLpNi6H8ZDby30n4Dx5dEmGgpNs+qzg1Rti2l257KPuepouZ+qkgb9VPo9K2UY3vX7saslMAYxMHsLnqEkn5NxEGJ3yQ6qzUFHG2gczMVIdwUing7/+ve/nSjsNPrrWHkhh1+VAepYMxpQoEVpcjf3yIABngjve5E8URfTPLj8QEnXnqkwqqVv/RWb/bvvhRx9ZDhXzaK3xaVegw4fYWImI5vEvThVrMlw/xfrXoCD8e87fARv0FpDeIdfW04cXQ0dYBYQ1vFydOBH+WICDqnMkHUgS99wuHFd5H2ihIQv4H5lCMGO8dg0by2ASL1mDzZrYmw9FRGWKIs2weeiYbZcjMFz/+WAoX8zkvYoRTPX3XjXh0yCZyC/eB/G5c//hrS4hn1Kzr2xocOcuwRX2FJmjACuD6gbVcfqJWyw4SDrXPVKA66ZTE+/ApWRD76OE= hell2@DESKTOP-U75MR1T"
                            }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVM)
    sendHttpRequest(urlCreateVM, json_data, headers)

createResourceGroup()
createVirtualNetwork()
createSubnet()
createPublicIpAdress()
createNetworkInterface()
createVm()

