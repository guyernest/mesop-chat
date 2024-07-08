
# Alternative chat interface for Bedrock Agent

This repository is part of the [Bedrock Agent](https://github.com/guyernest/bedrock-agent) project. It contains the code for the alternative chat interface for the Bedrock Agent, using the [mesop](https://google.github.io/mesop/) library. The chat interface in the main project is built using the [FastAPI](https://fastapi.tiangolo.com/) Python library, [Jinja](https://jinja.palletsprojects.com/), and [HTMX](https://htmx.org/) JavaScript library.

# CDK Python project

To manually create a virtualenv on MacOS and Linux:

```shell
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```shell
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```shell
.venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```shell
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```shell
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
