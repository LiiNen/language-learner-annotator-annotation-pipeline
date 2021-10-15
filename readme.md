# Dialog Annotator Web

This is a project to let MTurkers evaluate the dialogs. 

## How to setup

Make sure to have Python 3 installed, and run commands below to set up.

```bash
$ python -m venv ./env
$ source ./env/bin/activate
(env)$ pip install -r requirements.txt
```

## How to develop

To run development server, run the command below.

```bash
(env)$ FLASK_ENV=development python main.py
```

## How to run in production mode

To run this web app in production mode, run the command below.
```bash
(env)$ sh run.sh
```

Try http://localhost:5000 on a web browser.

## Prepare the source data

### Contexts

Dialog *contexts* must be prepared in `./data/contexts`. 
Each file represents one context, and should have a filename in a form `{context_id}.json`. Context ID can be any string that does not include `__` as a substring. 
A JSON object in a context file includes one dialog and multiple candidates to put at the end of the dialog. The dialog and all candidates should be in markdown format. Here is an example of a context JSON object.

```json
{
    "dialog": "**A**: \"When will Daddy come home?\"\n**B**: \"Soon, baby.\"\n**A**: \"But, he said he would be home for dinner,\"",
    "candidates": {
        "tfidf": "**B**: \"That is correct.\"",
        "hred": "**B**: \"You think so, too?\"",
        "vhcr": "**B**: \"You have to understand, dear.\"",
        "human": "**B**: \"Daddy will be here in an hour. You wanna wait?\""
    }
}
```

### Questions

Questions for each *context* should be prepared in `./data/questions.json`. 
The JSON object should be an array that has many quetion objects. 
A question object should have `id`, `text`, `mintext`, and `maxtext`.
Here is an example of a questions JSON array.

```json
[
    {
        "id": "overall",
        "text": "How appropriate is the response overall?",
        "mintext": "Not appropriate at all",
        "maxtext": "Very appropriate"
    },
    {
        "id": "topic",
        "text": "How on-topic is the response?",
        "mintext": "Not on-topic at all",
        "maxtext": "Very on-topic"
    }
]
```

## Results

Participants who submitted the answer will get a code that looks like: 

`under_slack_talk_{user_id_with_16_digits_and_letters}`

The results are saved in `./output/response/{context_id}__res__{user_id}.json`. 

**NOTE**

There may be participants who got the code `pass_no_132v82389a823l3133id112`. 
These participants have not passed the validity check and answered wrong to one or more validity check questions.

## Configs

Modify the value of a global variable `context_count_per_user` in `./main.py` if you need to.



