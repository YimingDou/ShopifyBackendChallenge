filename=$1
username=$2
password=$3

# Login first
JSON_STRING=$( jq -n \
                  --arg un "$username" \
                  --arg pw "$password" \
                  '{username: $un, password: $pw}' )

TOKEN=$(curl --silent \
  --header "Content-Type: application/json" \
  --request POST \
  --data "$JSON_STRING" \
  http://127.0.0.1:5000/auth/login | jq -r ".access_token")

if [ "$TOKEN" = "null" ]
then
    echo "\$TOKEN is NULL, authorization failed"
    exit 1
fi

(curl -v -L \
  -H "Authorization: Bearer ${TOKEN}" \
  -F file=@$filename \
  -F 'is_public=False' \
  -F press=OK \
  http://127.0.0.1:5000/upload 2>&1 1>&3 | grep "Location") 3>&1
