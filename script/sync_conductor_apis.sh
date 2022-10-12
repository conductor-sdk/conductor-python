brew install swagger-codegen

swagger-codegen generate -l python -i https://pg-staging.orkesconductor.com/api-docs -o swagger-code

cp ./swagger-code/swagger_client/api/* ../src/conductor/client/http/api/
cp ./swagger-code/swagger_client/models/*