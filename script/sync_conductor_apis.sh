TEMPORARY_FILE="temp.txt"
POSSIBLE_LINE_ENDINGS=('\n' '\r')
REPLACEMENT_FOR_LINE_ENDING='\f'
PACKAGE_APIS_PATH="../src/conductor/client/http/api/"
SWAGGER_GENERATED_CODE_FOLDER="./swagger-code"

function install_dependencies {
    brew install swagger-codegen
}

function generate_code {
    swagger-codegen generate -l python -i https://pg-staging.orkesconductor.com/api-docs -o "$SWAGGER_GENERATED_CODE_FOLDER"
}

function do_line_ending_replacement {
    tr '\n' $REPLACEMENT_FOR_LINE_ENDING <"$1" >"$TEMPORARY_FILE" && mv "$TEMPORARY_FILE" "$1"
}

function undo_line_ending_replacement {
    tr $REPLACEMENT_FOR_LINE_ENDING '\n' <"$1" >"$TEMPORARY_FILE" && mv "$TEMPORARY_FILE" "$1"
}

function copy_generated_api_files {
    cp $SWAGGER_GENERATED_CODE_FOLDER/swagger_client/api/* "$PACKAGE_APIS_PATH"
    echo "copied the generated code into the package api"
}

function replace_with_sed {
    sed -i '' -E s/"$1"/"$2"/ "$3"
}

function remove_file_header {
    pattern="# coding: utf-8.*from __future__"
    replace="from __future__"
    replace_with_sed "$pattern" "$replace" "$1"
}

function replace_import_header {
    pattern="from swagger_client.api_client import ApiClient"
    replace="from conductor.client.http.api_client import ApiClient"
    replace_with_sed "$pattern" "$replace" "$1"
}

function update_api_file {
    do_line_ending_replacement "$1"
    remove_file_header "$1"
    replace_import_header "$1"
    undo_line_ending_replacement "$1"
}

function update_api_files {
    echo "start updating api files..."
    copy_generated_api_files
    for filename in $(ls "$PACKAGE_APIS_PATH"); do
        filepath="$PACKAGE_APIS_PATH$filename"
        update_api_file "$filepath"
        echo "done updating api: $filepath"
    done
    echo "done updating api files"
}

generate_code
update_api_files
