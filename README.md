# JSON POLICY SIZE

## Purpose

This will work to allow the checking of a JSON object's non-whitespace character
size. This will work from either the root level of a JSON document or from within
a subkey structure (it does not support drilling down through arrays, only object
keys.)

## Usage

Basic run..

> check-json-size document.json

Specify maximum document size *(defaults to 6144, this is the max size of an AWS
IAM Policy)*...

> check-json-size --max-size 600 document.json

Specify start key in JQ notation (does not support integer references for arrays,
only works for object keys)...

> check-json-size --start-key .key1.key2.key3 document.json
