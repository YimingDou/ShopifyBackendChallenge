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
curl -X DELETE \
  -H "Authorization: Bearer ${TOKEN}" \
  http://127.0.0.1:5000/uploads/$filename