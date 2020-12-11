===============
cso_energy
===============

The aim of this repository is to simplify working work with CSO (Ireland's Central Statistics Office) energy-related statistics data

... with the help of the open source `Python` software :code:`prefect` and :code:`pandas`

... via:

- A `Jupyter Notebook` sandbox environment
- A `cso_energy` `Python` library 

------------

Benefits 
--------

Sandbox:

- It's free
- It's fast ... can be run on the cloud via `Google Collab` 
- It downloads the dataset directly

`cso_energy` library:

- It can be imported by other projects to automate the wrangling of CSO data

------------

This repository was setup by the `codema-dev` team as part of the SEAI RD&D funded `Dublin Region Energy Masterplan Project`__

__ https://www.codema.ie/projects/local-projects/dublin-region-energy-master-plan/

.. raw:: html

    <a href="https://www.codema.ie">
        <img src="images/codema.png" height="100px"> 
    </a> &emsp;

.. raw:: html

    <a href="https://www.seai.ie">
        <img src="images/seai.png" height="50px"> 
    </a> &emsp;

------------

Installation
------------

To setup the `cso_energy` sandbox:

- Google Collab:

    - Click the Google Collab badge & open `sandbox.ipynb`:
    
        .. image:: https://colab.research.google.com/assets/colab-badge.svg
                :target: https://colab.research.google.com/github/codema-dev/cso_energy
                
    - Mount your Google Drive to your Google Collab instance & refresh your filetree

        .. image:: images/mount-gdrive.jpg
    
    - Copy the path to your Google Drive data folder and paste it into the appropriate string

        .. image:: images/copy-path.png

    - For more information see `External data: Local Files, Drive, Sheets, and Cloud Storage`__
    
    __ https://colab.research.google.com/notebooks/io.ipynb

- Local:
    - Unzip the dataset
    - Clone this repository locally via :code:`git clone https://github.com/codema-dev/cso_energy` 
    - Launch `Jupyter Notebook` and open the relevant sandbox file in the `notebooks` folder 

