SWAGGER_API_DOCS_URL="https://pg-staging.orkesconductor.com/api-docs"
LANGUAGE_TO_GENERATE_CODE="python"
TEMPORARY_FILE="temp.txt"
POSSIBLE_LINE_ENDINGS=('\n' '\r')
REPLACEMENT_FOR_LINE_ENDING='\f'
PACKAGE_PATH="../src/conductor/client/http"
SWAGGER_GENERATED_CODE_FOLDER="./swagger-code"

function install_dependencies {
    brew install swagger-codegen
}

function generate_code {
    swagger-codegen generate -l "${LANGUAGE_TO_GENERATE_CODE}" -i "${SWAGGER_API_DOCS_URL}" -o "$SWAGGER_GENERATED_CODE_FOLDER"
}

function do_line_ending_replacement {
    tr '\n' $REPLACEMENT_FOR_LINE_ENDING <"$1" >"$TEMPORARY_FILE" && mv "$TEMPORARY_FILE" "$1"
}

function undo_line_ending_replacement {
    tr $REPLACEMENT_FOR_LINE_ENDING '\n' <"$1" >"$TEMPORARY_FILE" && mv "$TEMPORARY_FILE" "$1"
}

function copy_from_generated_files {
    source_path="${SWAGGER_GENERATED_CODE_FOLDER}/swagger_client/${1}"
    destination_path="${PACKAGE_PATH}/${1}/"
    for filename in $(ls "${source_path}"); do
        cp "${source_path}/${filename}" "${destination_path}"
    done
    echo "copied code from ${source_path} to ${destination_path}"
}

function replace_with_sed {
    sed -i '' -E s/"$1"/"$2"/g "$3"
}

function remove_file_header {
    pattern="${2}"
    replace="${3}"
    replace_with_sed "$pattern" "$replace" "$1"
}

function replace_import_header {
    pattern="from swagger_client.api_client import ApiClient"
    replace="from conductor.client.http.api_client import ApiClient"
    replace_with_sed "$pattern" "$replace" "$1"
}

function replace_authentication {
    pattern="'api_key'"
    replace=""
    replace_with_sed "$pattern" "$replace" "$1"
}

function replace_url_api_prefix {
    pattern="\'\/api"
    replace="\'"
    replace_with_sed "$pattern" "$replace" "$1"
}

function remove_init_file {
    init_path_to_remove="${PACKAGE_PATH}/${1}/__init__.py"
    echo "" >"${init_path_to_remove}"
    echo "removed content from ${init_path_to_remove}"
}

function append_method_for_model_task_result {
    code="\n    def add_output_data(self, key, value):\n        if self.output_data == None:\n            self.output_data = {}\n        self.output_data[key] = value"
    echo "${code}" >>"${1}"
}

function update_api_file {
    remove_file_header "${1}" "# coding: utf-8.*from __future__" "from __future__"
    replace_import_header "${1}"
    replace_authentication "${1}"
    replace_url_api_prefix "${1}"
}

function update_models_file {
    remove_file_header "$1" "# coding: utf-8.*import pprint" "import pprint"
    echo "updating models file: ${1}"
    if [[ "$1" == *"task_result.py" ]]; then
        append_method_for_model_task_result "${1}"
    fi
}

function update_files {
    echo "starting to update ${1} files..."
    copy_from_generated_files "${1}"
    remove_init_file "${1}"
    for filename in $(ls "${PACKAGE_PATH}/${1}"); do
        filepath="${PACKAGE_PATH}/${1}/$filename"
        do_line_ending_replacement "${filepath}"
        ${2} "${filepath}"
        undo_line_ending_replacement "${filepath}"
        echo "done updating: ${filepath}"
    done
    echo "done updating ${1} files"
}

update_files "api" update_api_file
update_files "models" update_models_file
