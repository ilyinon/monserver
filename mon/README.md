curl -X POST  -H "Content-Type: application/json" --data '{"status":"True","version":"111"}' http://127.0.0.1:8000/status/server1/apife/

curl -X POST  -H "Content-Type: application/json" --data '{"server":"server1.scl","service":"apife","status":"True","version":"111"}' \
 http://127.0.0.1:80/status/


curl -X POST  -H "Content-Type: application/json" --data '{"server":"qacore811.scl.five9lab.com","service":"VCC","status":"True","version":"1.10.1"}' \
 http://127.0.0.1:80/status/

curl -X POST  -H "Content-Type: application/json" --data '{"server":"qacore812.scl.five9lab.com","service":"UNKNOWN","status":"False","version":"UNKNOWN"}' \
 http://127.0.0.1:80/status/

