JSON_STRING=$( jq -n \
                  --arg un "$1" \
                  --arg pw "$2" \
                  '{username: $un, password: $pw}' )

curl --silent \
  --header "Content-Type: application/json" \
  --request POST \
  --data "$JSON_STRING" \
  http://127.0.0.1:5000/auth/register