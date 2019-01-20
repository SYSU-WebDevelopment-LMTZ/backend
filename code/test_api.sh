# POST
# curl localhost:5000/order/ -X POST -H "Content-Type:application/json" -d '{"restaurant_id":1, "tableid":1, "dishes":[{"dishid":1, "count":2}, {"dishid":5, "count":2}, {"dishid":9, "count":1}], "note":"this is an order"}' -w %{http_code}"\n"
# curl localhost:5000/restaurant/ -X POST -H "Content-Type:application/json" -d '{"phone":"12345678910", "password":"abc123", "name":"sysu-lmtz", "description":"canteen-lmtz", "logo":"logourl"}' -w %{http_code}"\n"

# GET
curl localhost:5000/dish/ -w %{http_code}"\n"

# PUT
# curl localhost:5000/dish/2 -X PUT -H "Content-Type:application/json" -d '{"price":"2.0"}' -w %{http_code}"\n"

# DELETE
# curl localhost:5000/dish/recommendation/2 -X DELETE -w %{http_code}"\n"

