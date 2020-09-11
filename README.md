# Winter 2021 Shopify Developer Intern Challenge

## Image repository backend

Built with Python + Flask

## Running the backend

Create a virtualenv
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

To start, execute
```
FLASK_APP=app/main.py flask run
```

## Example testing with shell scripts

Install jq using apt-get (or other package tools)
```
sudo apt-get install jq
```

Create dummy image
```
echo test > test.jpg
```

Register user
```
./scripts/register.sh username password
```

Upload private image  
Remeber the location of the redirect  
And note the body of the image should be same as what was echoed.  

```
./scripts/upload.sh test.jpg username password
```

View the image again (replace image name with the name in previous output)
```
./scripts/upload.sh bV8aCl7V9b1YFEPxsVwmqx.jpg username password
```

Verify the image is private. The command should return "access not permitted"
```
./scripts/upload.sh bV8aCl7V9b1YFEPxsVwmqx.jpg
```

Delete the image
```
./scripts/delete.sh bV8aCl7V9b1YFEPxsVwmqx.jpg username password
```

Verify the image is deleted. The command should return "image does not exist"
```
./scripts/upload.sh bV8aCl7V9b1YFEPxsVwmqx.jpg username password
```