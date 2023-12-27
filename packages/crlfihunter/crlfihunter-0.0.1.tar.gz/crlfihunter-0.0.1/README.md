# CRLFi Hunter

## Overview
This tool parses a text file containing URLs, and it will start testing for Carriage Return Line Feed Injection Vulnerability. 
If it present in the input text file, it will shows us the vulnerable endpoint and it's suitable payload.


## Features
- **Comprehensive CRLFi finder:**
  - Parses URLs from a text file and start testing with different payloads.
  - Generates quick and effective report to the Hunters.

- **File Input:**
  - Accepts a text file as input, allowing batch processing of multiple URLs.
  - Easily customizable for different sets of URLs.

- **Clear Output:**
  - Displays the original URL along with a series of payloads.
  - Provides a concise overview of payload for each entry.

## Screenshots 📸 :
<h1 align="center">
  <h2 align="center">Screen Shot 1</h2>
  <h1 align="center"><img align="center" src="https://ik.imagekit.io/d3kzbpbila/thejashari_OBF3ya4mk" width="700px" alt="screenshot1"></h1>
  <h2 align="center">Screen Shot 2</h2>
 <h1 align="center"> <img align="center" src="https://ik.imagekit.io/d3kzbpbila/thejashari_sscL1Lt9i" width="700px" alt="screenshot2"></h1>


## Installation
### Cloning the repository
1. **Clone the repository:**
    ```bash
    git clone https://github.com/thejas-dev/url-splitter
    cd url-splitter
    ```
    
2. **Install dependencies (if any):**
    ```bash
    pip install -r requirements.txt
    ```

### Making the Tool Global

To make Gazilion Endpoint Splitter globally accessible from any directory, follow these steps:

1. Open your Zsh configuration file (`~/.zshrc`) in a text editor:
    ```bash
    nano ~/.zshrc
    ```
    Replace `nano` with your preferred text editor.

2. Add the following line at the end of the file, replacing `/path/to/tool/directory/gazillionsplitterpython` with the actual path to the tool directory:
    ```bash
    export PATH=$PATH:/path/to/tool/directory/gazillionsplitterpython
    ```

3. Save the file and exit the text editor.

4. Reload your Zsh configuration to apply the changes:
    ```bash
    source ~/.zshrc
    ```

Now, you can run Gazilion Endpoint Splitter from any directory using:
```bash
splitter.py -h
```

### Pip Package Installation
1. **Install the package:**
    ```bash
    pip3 install gazillionsplitterpython
    ```
    
2. **Check if successfully installed:**
    ```bash
    gazillionsplitterpython -h
    ```
    Visit <a href="https://pypi.org/project/gazillionsplitterpython/">Gazillion Splitter Pip Package </a> for more info


### Usage

#### Options
- **-l <url-list>:** Specify the path to the URL list.
- **-o <outputFile>:** Specify the output file name.
- **-h, --help:** Display this help message.

#### Example
Run the tool with the following command for repository clone:
```bash
splitter.py -l urllist.txt -o output.txt
```
Run the tool with the following command for pip installation:
```bash
gazillionsplitterpython -l urllist.txt -o output.txt
```

### Connect with me on
<a href="https://www.linkedin.com/in/thejashari/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="linkedin" height="30" width="40" /></a>
<a href="https://instagram.com/nuthejashari" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="instagram" height="30" width="40" /></a>
