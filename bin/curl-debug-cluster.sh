#!/bin/sh

kubectl run "curl-debug" --image=curlimages/curl -it --rm -- sh
