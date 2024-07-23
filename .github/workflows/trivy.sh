#!/bin/bash

trivy image --exit-code 1 --severity HIGH,CRITICAL fastpython_web

EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
    echo "trivy encontrou vulnerabilidades altas na aplicação"
    exit 1
else
    echo "Trivy não encontrou nenhuma vulnerabilidade alta"
    exit 0
fi

