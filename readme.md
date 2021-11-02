# Language Learner Annotator Web

This is a project to let MTurkers evaluate the dialogs. 

## How to setup

Make sure to have Python 3 installed, and run commands below to set up.

```bash
$ python -m venv ./env
$ source ./env/bin/activate
(env)$ pip install -r requirements.txt
```

for windows
```bash
$ python -m venv ./env
$ env\Scripts\activate.bat
(env)$ pip install -r requirements.txt
```

## How to develop

To run development server, run the command below.

```bash
(env)$ FLASK_ENV=development python main.py
```

for windows
```bash
(env)$ set FLASK_ENV=development
(env)$ $env:FLASK_APP = "main"
(env)$ flask run
```

Try http://localhost:5000 on a web browser.

## How to run in production mode

To run this web app in production mode, run the command below.
```bash
(env)$ sh run.sh
```

Try http://localhost:5000 or https://rum.uilab.kr:5000 on a web browser.

## Prepare the source data

### Sentence

Provide dataset at [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1DPQnBmAQtJ0pCYGgD7dSmoN8EUKWU10eGUjPJ76B5TE/edit?usp=sharing) with a `json` format.

```json
{
    "premise": "Kucing itu mengejar burung.", 
    "sentence1": "Burung itu terbang.", 
    "sentence2": "Burung itu menangkap seekor cacing.", 
    "question": "effect"
}
```

### Questions

Questions for each *task* should be prepared in `./data/questions.json`. 
The JSON object should be an array that has many quetion objects. 
A question object should have `id`, `text`, `mintext`, and `maxtext`.
Here is an example of a questions JSON array.

```json
[
    {
        "task": "natural language inference",
        "text": "Based on the premise, determine the hypothesis",
        "option": {
            "ent": "entailment",
            "neu": "neutral",
            "con": "contradict"
        }
    },
    {
        "task": "binary sentence similarity",
        "text": "Determine whether two sentences deliver same meaning",
        "option": {
            "0": "different",
            "1": "similar"
        }
    }
]
```

## Results

Participants who submitted the answer will get a code that looks like: 

`done_{user_id_with_16_digits_and_letters}`

The results are saved in `./output/response/{context_id}__res__{user_id}__{worker_id}.json`. 

<!-- **NOTE**

There may be participants who got the code `pass_no_132v82389a823l3133id112`. 
These participants have not passed the validity check and answered wrong to one or more validity check questions. -->

## Configs

Modify the value of a global variable `context_count_per_user` and `user_count_per_context` in `./main.py` if you need to.



