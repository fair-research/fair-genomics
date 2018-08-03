# 4M.4.FULLSTACKS: Cross-stack Compute

## Table of Contents
1. [Quickstart Tutorial](#quickstart-tutorial)
1. [Introduction](#introduction)
1. [Use of Globus Auth Token](#use-of-globus-auth-token)
1. [User Login to FAIR Research Data Portal](#user-login-to-fair-research-data-portal)
1. [Faceted Search](#faceted-search)
    1. [Male Smokers with 4th Stage Lung Cancer](#male-smokers-with-4th-stage-lung-cancer)
    1. [Female Non-Smokers with 4th Stage Lung Cancer](#female-non-smokers-with-4th-stage-lung-cancer)
1. [Analysis of Input Datasets using Workspace](#analysis-of-input-datasets-using-workspace)
    1. [TOPMed RNA-Seq analysis pipeline](#topmed-rna-seq-analysis-pipeline)
    1. [Analysis using Globus Genomics](#analysis-using-globus-genomics)
    1. [Analysis using JupyterHub](#analysis-using-jupyterhub)
    1. [Results of Analysis](#results-of-analysis)
    
## Quickstart Tutorial
This quickstart tutorial walks through a quick submission of 5 downsampled TOPMed CRAM input files using a TOPMed Alignment workflow in CWL. It uses a portal to index and search the input datasets and submits to a WES (Workflow Execution Service - GA4GH) service deployed as a shim-layer on the Galaxy based Globus Genomics platform.

* Login to the search portal at: https://globus-portal.fair-research.org/search/ using your Globus credentials
* Search for the 5 downsampled input CRAM files using the search tag "downsampled"
* Select the 5 samples by checking the box next to "downsampled" in the left menu
* Click on "Add Minids" button, which creates a Workspace called "Downsampled Topmed" and adds these 5 samples for analysis
* Then click on the "Start" button for each input CRAM file to initiate the alignment workflow using Globus Genomics backend.
* Typically, after 20-25mins, the analysis of the 5 downsampled inputs should be completed and you should see the resulting BDBag-Minid under the "Output files" column of the workspace. 
The picture below shows a screenshot of the workspace used for the analysis of the 5 input CRAM files

![Screenshot](images/downsample-outputs.png)

## Introduction
This README describes the implementation of a fullstacks platform that allows to:
* Analyze open access TOPMed WGS data by sharing the same CWL workflow around with other fullstacks
* Scale up the analysis to 5 downsampled, 7 full size WGS open access TOPMed samples and 25 of the remaining 100 samples
* Demonstrate the use of GA4GH Workflow Execution Service (WES) implementation to standardize the workflow execution across multiple fullstacks 
* Build upon the “Workspaces” implemented in 3M.4 Fullstacks demo and add additional features to submit to the WES interface
* Use of Globus auth tokens for user access and user management in Galaxy within Globus Genomics

Some of the highlights of this month’s deliverable are: 
* We indexed the 5 downsampled and 107 open access TOPMed samples within the data portal at https://globus-portal.fair-research.org/workflows/ 
* We implemented a CWL-Runner tool within Galaxy to support CWL workflow execution within Galaxy based Globus Genomics
* We implemented a GA4GH WES service that provides a standard interface to allow CWL based workflow submission and workflow status tracking hiding the Galaxy specific details
* A major feature is the use of Globus auth tokens for user-management on the Galaxy side, thus eliminating the need for a Galaxy API keys used in the previous month deliverables
* Extended the fair research data portal to act as an workflow orchestrator to submit CWL workflows to Globus Genomics via the new WES interface

## Use of Globus Auth Token:
One of the highlights of this deliverable is the use of Globus Auth tokens instead of the Galaxy API Keys to interact with Galaxy. Within the WES implementation, the Globus auth token is used to map the user to the local Galaxy user. If the user doesn’t exist, from within the WES, we create that user using the Galaxy Bioblend API and generate a Galaxy API Key that is then used internally. If the user already exists, we map the Globus Auth token to the user and retrieve the API key and use it to interact with Galaxy. It significantly simplifies the authentication, authorization and the ease of use of our fullstacks platform.

We demonstrate this feature by using the data portal that uses Globus authentication to login. And the portal submits the CWL workflows to the WES interface with the Globus auth tokens in the headers that have the Globus Genomics application scope for further validation. 

## User Login to FAIR Research Data Portal
The FAIR Research data portal is available at: https://globus-portal.fair-research.org and users can login using their Globus ID.
![Screenshot](images/globus-login.png)

## Analysis of 5 Downsampled CRAM inputs
