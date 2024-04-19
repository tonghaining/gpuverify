chmod -R 777 .
docker run --mount type=bind,source="$(pwd)",target=/app -ti --rm --entrypoint=/bin/bash delcypher/gpuverify-docker:cvc4