[![BuildStatus](https://github.com/mattintech/PyKTL/workflows/CI/badge.svg)](https://github.com/mattintech/PyKTL/actions/workflows/auto-build-publish.yml)
[![PyPI Version](https://img.shields.io/pypi/v/PyKTL.svg)](https://pypi.org/project/PyKTL/)
[![Active branch](https://img.shields.io/badge/branch-master-lightgrey.svg)](https://github.com/mattintech/PyKTL/tree/master/)

<div style="text-align: right"> 
    <a href="https://www.buymeacoffee.com/mattintech" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
</div>


# KnoxTokenLibrary-Python ('PyKTL')

**This is not an offical Samsung library or repository**

pyktl is a python rewrite of the knox-token-library-js library written by Samsung.  The following code was used to build this project. https://www.npmjs.com/package/knox-token-library-js?activeTab=readme

## Usage

Install using: 
```
pip install PyKTL
```

### Assumptions 
 - You have downloaded the Knox Certificate file (certificate.json)
 - You have generated a Client Identifier (api-key) for accessing apis of Knox Cloud Services.

### Intended Use
The workflow for making api calls to Knox Cloud Services is divided into a portal workflow, and a programmatic workflow.

#### Portal flow

 - Download Certificate from Knox Api Portal
 - Generate and Download ClientIdentifier (api-key) for a specific Knox Solution

#### Programmatic flow

 - Call Knox api to generate an Api Access Token. This api call requires a signed ClientIdentifier, and specific contents of your Certificate (Public Key).
 - Call Knox api for your intended workflow (eg: upload device, configure device etc). This api call requires your signed Api Access Token, and specific contents of your Certificate (Public Key).

 - This utility py library helps generate signed clientIdentifiers, and signed accessTokens.

## Examples
Leverage examples from [here](https://github.com/mattintech/KnoxCloudService-Python).

The example leverages a keys.json which is obtained using the SamsungKnox.com portal - view the Samsung tutorial for more details. 
The example also leverages clientId.json which includes the clientIds 

```
{
    "kme": "",
    "kc": "",
    "ke1": "",
    "kai": ""
}
```
You can also reference Samsung's authentication tutorail found here: https://docs.samsungknox.com/dev/knox-cloud-authentication/tutorial/tutorial-for-customers-generate-access-token/. 
I did attempt to keep only required method names, so not all methods found in the nodejs/java/NuGet package will be available in PyKTL.


## Local Build & Install
In order to build and install pyktl locally you can run the following commands:

```
python setup.py sdist
pip install .
```

## KDP API Support
While no testing was done using the PyKTL and the Knox Deployment Program API - it is believed it should still work.  Authentication between the KCS APIs and KCS APIs appears to be the same.
