### Prerequisites/Assumptions
### * This script is run within the batcave-landing-zone/helpers directory
### * The `signal/` repository path is either parallel with `batcave-landing-zone/` or provided as the first parameter

blz_base=../infra/base
ado_base=${1:-../../signal/infra/base}

echo "Comparing ${blz_base} with ${ado_base}"
diff -ur ${blz_base} ${ado_base}
echo "To synchronize these differences:  cp -r ${blz_base} ${ado_base}"