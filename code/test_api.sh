# POST
# curl localhost:5000/order/2 -X POST -H "Content-Type:application/json" -d '{"state":2}' -w %{http_code}"\n"

# GET
curl localhost:5000/order/ -w %{http_code}"\n"

# PUT
# curl localhost:5000/dish/2 -X PUT -H "Content-Type:application/json" -d '{"price":"2.0"}' -w %{http_code}"\n"

# DELETE
# curl localhost:5000/dish/recommendation/2 -X DELETE -w %{http_code}"\n"

