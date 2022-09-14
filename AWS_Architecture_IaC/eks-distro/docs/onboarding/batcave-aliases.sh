## CMS Aliases
export BATCAVE_CMS_USERNAME=abcd #your cms-id

function batcave_aliases(){
  # For each account, create a set of aliases:
  #  $ batcave-aliases <account_id> <ct-role-prefix> bat-dev
  #  creates...
  #  bat-dev-admin
  #  bat-dev (same as above)
  #  bat-dev-admin-login
  #  bat-dev-login (same as above)
  #  bat-dev-ro
  #  bat-dev-ro-login
  account_id=$1
  ct_role_prefix=$2 #eg "batcave", "sssa"
  alias_nickname=${3:-$ct_role_prefix}
  batcave_alias ${account_id} ${ct_role_prefix} ${alias_nickname} "ro" "readonly"
  batcave_alias ${account_id} ${ct_role_prefix} ${alias_nickname} "admin" "application-admin"
  # Default <nick> and <nick>-login to admin role
  alias ${alias_nickname}=${alias_nickname}-admin
  alias ${alias_nickname}-login=${alias_nickname}-admin-login
}
function batcave_alias(){
  account_id=$1
  ct_role_prefix=$2 #eg "batcave", "sssa"
  alias_nickname=$3
  alias_suffix=$4
  ct_role_suffix=$5
  alias ${alias_nickname}-${alias_suffix}="export AWS_PROFILE=${account_id}_${ct_role_prefix}-${ct_role_suffix}"
  alias ${alias_nickname}-${alias_suffix}-login="ctkey --account=${account_id} --cloud-access-role=${ct_role_prefix}-${ct_role_suffix}"
  export jq_map="{\"${account_id}_${ct_role_prefix}-${ct_role_suffix}\": \"${alias_nickname}-${alias_suffix}\"}"
  export BATCAVE_ENV_MAP=$(echo $BATCAVE_ENV_MAP | jq '. as $bem | $ENV.jq_map | fromjson as $jqm | $bem * $jqm')
  unset jq_map
}
export BATCAVE_ENV_MAP="{}"
batcave_aliases 373346310182 batcave bat-dev
batcave_aliases 831579051573 batcave bat-test
batcave_aliases 111594127594 batcave bat-impl
batcave_aliases 863306670509 batcave bat-prod
batcave_aliases 368332260651 sssa signal-dev
batcave_aliases 724350100575 sssa signal-test
batcave_aliases 546924760321 sssa signal-prod

function __batcave_aws_profile_prompt {
  echo $BATCAVE_ENV_MAP | jq -r '.[env.AWS_PROFILE] // ""'
}

### CloudTamer Login Function
ctkey () {
  mkdir -p ~/.ctkey
  if [ ! -f ~/.ctkey/ctkey.zip ]; then
    # Download the ctkey.zip arhive
    curl -o ~/.ctkey/ctkey.zip https://ctkey.s3.amazonaws.com/ctkey.zip
    # Ensure the archive will be re-extracted by removing the extracted directory
    rm -rf ~/.ctkey/ctkey
  fi
  if [ ! -d ~/.ctkey/ctkey ]; then
    # Extract the archive
    unzip ~/.ctkey/ctkey.zip -d ~/.ctkey/ctkey
  fi
  # Run the ctkey binary
  case $(uname -s) in
    Darwin)
      CT_BINARY=osx
      ;;
    *)
      CT_BINARY=linux
  esac
  CTKEY_URL=https://cloudtamer.cms.gov
  CT_USER_OPT="--username=${BATCAVE_CMS_USERNAME}"
  CT_PASS_OPT="--password=$(pass cms/eua-pass)"
  ~/.ctkey/ctkey/ctkey-${CT_BINARY} savecreds --url=$CTKEY_URL --idms=2 $CT_USER_OPT $CT_PASS_OPT $@
}
