# Python Data Viewer Application

## Overview

The **Data Viewer** is a Qt Python application to view, edit, plot,
and filter data from various file types.  

The Data Viewer utilizes the `pandas` module along with the 
`Qt for Python` module to provide a familiar spreadsheet-like GUI for
any type of data that can be stored in a pandas `DataFrame`.  

The intention of this application is to provide a high-performance,
cross-platform application to review and analyze data. The Data
Viewer provides a faster and more optimized alternative for viewing and
plotting data files in a table format as opposed to other
applications such as Microsoft Excel or OpenOffice.

### Supported Input Formats

> Note: Input formats are automatically recognized based on the filename.  

The Data Viewer currently supports the following input formats:  

-   CSV (comma-delimited, tab-delimited)  

-   TXT (plain-text files)  

-   JSON (Javascript Object Notation)  

-   PICKLE (Python Pickle Format)  

-   XLSX (Microsoft Excel or OpenOffice files)  

### Supported Operating Systems

The following operating systems have been tested and confirmed to operate
the application nominally:  

-   Windows 10
-   MacOS Version 11.2 (Big Sur) using Apple M1
-   Linux (CentOS, Ubuntu)

Other operating systems are untested but will likely function if they are
supported by the Qt for Python version documented in requirements.txt

## Setup Instructions

### Dependencies

The following dependencies are required to run the data viewer application.

> Note: See [requirements.txt](requirements.txt) for the full dependency list including module versions.

-   `Python` (Version 3.6 or greater)
-   `pandas`
-   `numpy`  
-   `PyQt5`  
-   `openpyxl`  
-   `matplotlib`  
-   `QDarkStyle`  

### Application Setup / Installation

The Data Viewer uses `pip` to manage it's dependencies and can be setup using the commands below from the base directory of this repository.

> **Note: If you are using an Anaconda installation, you can skip these setup steps and proceed directly to the the [Running the Application](#running-the-application) section.**
  


#### Using a Python Virtual Environment (Recommended setup method)

> Windows (Git Bash)

```bash
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
```  

> MacOS / Linux

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```  

#### Installing dependencies locally

> Note: The commands below can be used in Linux, MacOS, or Windows (Powershell, Git Bash, Cygwin, or WSL)

```bash
pip install -r requirements.txt
```  

After downloading the dependencies, you can either clone and run the application directly from the source code,  
or you can install the PyPi package using the instructions below (this is the recommended method).

> PyPi Package Installation Instructions:  
> Note, this requires that you have a [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with the scope set to `api`.  
```bash
pip install --index-url https://<personal_access_token_name>:<personal_access_token>@gitlab.com//api/v4/projects/30493184/packages/pypi/simple --no-deps dataviewer
```

> If you have have your gitlab access token stored in file, you can also do something like this:  
```bash
pip install --index-url https://${LOGNAME}-gitlab-api-token:$(cat ~/${LOGNAME}-gitlab-api-token)@gitlab.com//api/v4/projects/30493184/packages/pypi/simple --no-deps dataviewer
```

## Running the Application

> **Recommended Method**: Run as a module

```bash
python -m dataviewer
```

> Run from source: Linux, MacOS, or Windows (Git Bash)

```bash
python dataviewer/dataviewer.py
```

> Run from source: Windows (Powershell or CMD)

```sh
python dataviewer\dataviewer.py
```

> If using Anaconda 3 on windows with Git Bash installed, you can use the [run.sh](run.sh) script.

```bash
./run.sh
```