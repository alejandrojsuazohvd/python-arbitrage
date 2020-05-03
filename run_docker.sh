#/bin/sh
docker stop arbitrage_container
docker rm -v arbitrage_container
docker build -t arbitragesuazo .
docker run --name arbitrage_container -d -p 8081:8081 arbitragesuazo
exit 0
