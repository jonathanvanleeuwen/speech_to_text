# Introduction <!-- omit in toc -->
This is a code repo for interfacing with the azure speech to text SDK

**Note**
It requires the user to have an AZURE-COGNITIVE_SERVICES-SPEECH-KEY, if used as a CMD tool, the AZURE-COGNITIVE_SERVICES-SPEECH-KEY needs to be set as an environment variable named `SUBSCRIPTION`. Alternatively it can be defined in a .env file as: `SUBSCRIPTION=AZURE-COGNITIVE_SERVICES-SPEECH-KEY`

- [Description](#description)
- [Install code](#install-code)
  - [Install source code](#install-source-code)
    - [Build your own package if you modify source code](#build-your-own-package-if-you-modify-source-code)
  - [Install built package](#install-built-package)
- [How to use the code](#how-to-use-the-code)
  - [Set env variable when running from command line](#set-env-variable-when-running-from-command-line)
  - [How to run code from source code](#how-to-run-code-from-source-code)
  - [How to use class after package install](#how-to-use-class-after-package-install)
    - [Run from commandline after package install](#run-from-commandline-after-package-install)
- [Folder structure](#folder-structure)


# Description
This code is a wrapper which can be used to interface easily with the azure cognitive services.
When run, the class outputs to a log and a file.
It has a class with two main methods.
1. `SpeechToText.from_file(filepath)` - Transcribes an audio file and writes the output to a file.
2. `SpeechToText.from_mic()` - Live transcription from your microphone.

It can be installed with the [prebuilt package](#install-built-package) or as [source code](#install-source-code)


# Install code
This guide assumes you are using windows, the instructions should be similar for other operating systems.
Its assumed that you are using [vscode and have python installed](https://code.visualstudio.com/docs/python/python-tutorial).

## Install source code
1. Download/clone the code (where this readme is located)
2. Open vscode and from within vscode open the main folder with the code
3. Open a new terminal
   1. Press: Ctrl+Shift+P and type "terminal"
   2. Select: Python: create terminal
4. In the new terminal create a new environment and activate it
   1. 'python -m venv .venv'
   2. If prompted, click yes to use the new virtual environment
   3. If not prompted, click the python/environment button i the bottom left of the blue ribbon and select the new environment
   4. Ensure that the correct environment is activated, you should see the following in the terminal
      1. `([env_name]) folderpath]>`
      2. `(.venv) C:\Users\testuser>`
5.  Install the requirements file.
   * **Ensure that you are in the correct directory and using the "[env_name]" environment**
   * Run: `pip install -r requirements.txt`
6.  Done! you can now move on to the next section on [how to use the code](#how-to-use-the-code)
* Optionally: -Install code as a dynamic package, for dev purposes, imported code updates when code updates
    - pip install -e .
### Build your own package if you modify source code
In your activated venv, in terminal run
    - `python -m build`

## Install built package
1. Download the `dist/speech_to_text_az_interface-[version]-py3-none-any.whl` file.
2. Make sure your in your virtual env (in terminal) (see instructions for [creating venv](#install-source-code))
3. In terminal run `pip install path_to_whl/speech_to_text_az_interface-[version]-py3-none-any.whl`
4. Done! you can now move on to the next section on [how to use the code](#how-to-use-the-code)

Uninstall with: `pip uninstall speech-to-text-az-interface`

# How to use the code
* Pre-requisites
  1. Ensure that you have followed all the steps to [Install code](#install-code)
  2. Ensure that you have activated the correct virtual environment.
  3. Ensure that the dependencies in requirements.txt are installed (if you are installing source code).
  4. Ensure that you have navigated to the directory containing this code (if you are installing source code).
  5. You have a valid and working `AZURE-COGNITIVE_SERVICES-SPEECH-KEY`
  6. If your running from CMD, the `AZURE-COGNITIVE_SERVICES-SPEECH-KEY` is set as an [environment variable](#set-env-variable-when-running-from-command-line)

## Set env variable when running from command line
1. Define in a .env file.
   * Create a .env file in the main directory
   * Put the `AZURE-COGNITIVE_SERVICES-SPEECH-KEY` in the .env file as follows
     * `SUBSCRIPTION=AZURE-COGNITIVE_SERVICES-SPEECH-KEY`
2. Temporarily set the variable in the virtual environment using the terminal
   * `set SUBSCRIPTION=AZURE-COGNITIVE_SERVICES-SPEECH-KEY` - (Windows)
   * `export SUBSCRIPTION=AZURE-COGNITIVE_SERVICES-SPEECH-KEY` - (Mac)

## How to run code from source code
Use the command line
`python speechtotext -h` - Help
`python speechtotext version` - Print version info
`python speechtotext run -h` - Help for run options
`python speechtotext run --option1 "value" --option2 "value"` - etc

## How to use class after package install
Assuming the code is installed from wheel, you can import the code and use it as follows:
```
required kwargs:
:param subscription: The subscription key to use for the service, str

optional kwargs
:param region: The region of the service i.e. westeurope (default), str
:param out: The output file and location to save results i.e. "./default_out.txt" (default), Path
:param max_duration: The maximum time the recognizer will run, seconds i.e. 3600 (default), Int
:param language: The language the recognizer will use, i.e. "en-US" (default), str
:param verbose: logging level to output, default = INFO
```
```
# Import
from speechtotext import SpeechToText

speech2txt = SpeechToText(subscription=AZURE-COGNITIVE_SERVICES-SPEECH-KEY)
# To run speech to text from mic
speech2txt.from_mic()

# To run speech to text from file
speech2txt.from_file(audio_file_path)

```

### Run from commandline after package install
`python -m speechtotext -h` - Help
`python -m speechtotext version` - Print version info
`python -m speechtotext run -h` - Help for run options
`python -m speechtotext run --option1 "value" --option2 "value"` - etc

# Folder structure

+ <details>
    <summary> Speech to text - The main directory of the code </summary>

    + <details>
        <summary> speechtotext - The source code </summary>

        * [__ init __.py](/speechtotext/__init__.py) - init file
        * [__ main __.py](/speechtotext/__main__.py) - The commandline interface code
        * [entry.py](/speechtotext/entry.py) - The entry wrapper used by __ main __

        + <details>
            <summary> samples - Contains audio fragments </summary>

            * [__ init __.py](/speechtotext/samples/__init__.py) - init file
            * audio_files - any audio fragment samples used for testing purposes

            </details>

        + <details>
            <summary> speech_to_text - Contains source code for the SpeechToText wrapper class </summary>

            * [__ init __.py](/speechtotext/speech_to_text/__init__.py) - init file
            * [speech_to_text.py](/speechtotext/speech_to_text/speech_to_text.py) - The wrapper class source code

            </details>

        + <details>
            <summary> tests - Code for tests </summary>

            + <details>
                <summary> integration - Code for integration tests </summary>

                + <details>
                    <summary> speechtotext - Integration tests for the code in speechtotext </summary>

                    * [__ init __.py](/speechtotext/tests/integration/speechtotext/__init__.py) - Empty init file
                    </details>

                * [__ init __.py](/speechtotext/tests//integration/__init__.py) - Empty init file
                </details>

            + <details>
                <summary> unit - Code for unit tests </summary>

                + <details>
                    <summary> speechtotext - Unit tests for the code in speechtotext </summary>

                    * [__ init __.py](/speechtotext/tests/unit/__init__.py) - Empty init file
                    * [test_speechtotext.py](/speechtotext/tests/unit/speechtotext/test_speechtotext.py) - unit tests
                    </details>

                * [__ init __.py](/speechtotext/tests/unit/__init__.py) - Empty init file
                </details>

            * [__ init __.py](/speechtotext/tests/__init__.py) - Empty init file
            * [conftest.py](/speechtotext/tests/conftest.py) - File containing pytest fixtures and configurations
            </details>
        </details>

    + <details>
        <summary> dist - The prebuilt wheel packages </summary>

        * speech_to_text_az_interface-[version]-py3-none-any.whl - Built wheel package

        </details>


    * [.gitignore](/.gitignore) - The git ignore file
    * [LICENSE](/LICENSE) - The license file
    * [README.md](/README.md) - The project documentation
    * [requirements.txt](/requirements.txt) - The code dependencies/requirements
    * [setup.cfg](/setup.cfg) - The static project setup file
    * [setup.py](/setup.py) - The dynamic project setup file

    </details>
