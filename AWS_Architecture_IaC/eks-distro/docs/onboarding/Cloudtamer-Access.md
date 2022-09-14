# Getting Cloudtamer AWS Access
CMS uses [Cloudtamer](https://cloudtamer.cms.gov/portal) (must be on VPN) to manage access to AWS accounts. In order to log into CMS AWS accounts via the CLI, you will first need to set up a few things

## AWS CLI
Install with `brew install awscli`

## Pass
[Pass](https://www.passwordstore.org/) is a CLI password manager for Unix systems. Batcave developers use this as a secure password store, specifically when logging into Cloudtamer AWS accounts via the CLI. To setup `pass`:
1. Install with `brew install pass` 
2. Generate a GPG Key using your own information 
    - `gpg2 --full-generate-key`  
        - Kind of key: `RSA and RSA`
        - Keysize: `4096`
        - Key should not expire 
        - Fill out the rest of the prompts with your own information (ie. name, email (non-CMS), etc)    

The output the command should look like:  
```
    Please select what kind of key you want:
    (1) RSA and RSA (default)
    (2) DSA and Elgamal
    (3) DSA (sign only)
    (4) RSA (sign only)
    (14) Existing key from card
    Your selection? 1
    RSA keys may be between 1024 and 4096 bits long.
    What keysize do you want? (3072) 4096
    Requested keysize is 4096 bits
    Please specify how long the key should be valid.
            0 = key does not expire
        <n>  = key expires in n days
        <n>w = key expires in n weeks
        <n>m = key expires in n months
        <n>y = key expires in n years
    Key is valid for? (0) 0
    Key does not expire at all
    Is this correct? (y/N) y

    GnuPG needs to construct a user ID to identify your key.

    Real name: rusty
    Email address: rusty@bestcontractor.com
    Comment:
    You selected this USER-ID:
        "rusty <rusty@bestcontractor.com>"

    Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
    We need to generate a lot of random bytes. It is a good idea to perform
    some other action (type on the keyboard, move the mouse, utilize the
    disks) during the prime generation; this gives the random number
    generator a better chance to gain enough entropy.
    We need to generate a lot of random bytes. It is a good idea to perform
    some other action (type on the keyboard, move the mouse, utilize the
    disks) during the prime generation; this gives the random number
    generator a better chance to gain enough entropy.
    gpg: revocation certificate stored as '/Users/gedd/.gnupg/openpgp-revocs.d/1FFF4CE52D6249B8D6ACEEB840FD38BCFEFA8852.rev'
    public and secret key created and signed.

    pub   rsa4096 2022-08-23 [SC]
        1FFF4CE52D6249B8D6ACEEB840FD38BCFEFA8852
    uid                      rusty <rusty@bestcontractor.com>
    sub   rsa4096 2022-08-23 [E]
```
Now that the GPG key has been created, you will need to initialize `pass` using the secret key.  

3. Run: `gpg2 --list-secret-keys --keyid-format LONG`
    - You should see output that looks something like:
       ```
       sec   rsa4096/40FD38BCFEFA8852 2022-08-23 [SC]
             1FFF4CE52D6249B8D6ACEEB840FD38BCFEFA8852
       uid                 [ultimate] rusty <rusty@bestcontractor.com>
       ssb   rsa4096/719F7DD856A8C9AB 2022-08-23 [E]
       ```
      The secret key in this case is `40FD38BCFEFA8852`.  
4. `pass init <secret key>`  
5. Create the `pass` datastore: `pass insert cms/eua-pass` and enter your EUA password 

Your `pass` password store should now be initialized and encrypted. 

(Good reference material: https://www.redhat.com/sysadmin/management-password-store)

## Cloudtamer
To login to Cloudtamer and access AWS accounts via the CLI, you'll need to add some aliases to your shell. If you use `bash` open the `.bashrc` file, or if you use `zsh` open the `.zshrc` file, both are located in your home directory. If you prefer to put these aliases somewhere else, you can do that as well but that topic will not be covered in this guide. Add the following aliases and functions to your `.*rc` file: [batcave-aliases.sh](./batcave-aliases.sh)

A few more things:
- Be sure to change the first line containing `BATCAVE_CMS_USERNAME` to your EUA username.  
- Re-source your `.*rc` file using something like: `source ~/.zshrc` (if using `zsh`)
- Test that everything is working correctly by invoking the alias `bat-dev-login`

If all goes well (you may be prompted for your GPG key's password), you should be logged into the Batcave dev AWS account. Test this by running `aws sts get-caller-identity --region us-east-1`, the output's `Arn` field should look like:
```
"Arn": "arn:aws:sts::373346310182:assumed-role/ct-ado-batcave-application-admin/<your CMS EUA ID>"
```

Verify that the account number is `373346310182`. If this is correct, congratuations! You have now set up your machine's access to CMS/Batcave AWS.

## Using the Aliases
Use these aliases to easily switch between AWS accounts. Note that commands ending in `-login` will call the `ctkey` function which will log you into the desired AWS account. To set your shell to actually point to that environment, you'll need to run the corresponding command without the `-login` suffix. For example, to log into the dev environment you can simply run:
```
bat-dev-login && bat-dev
```
- `bat-dev-login` logs you into dev AWS account using Cloudtamer
- `bat-dev` points your shell at the dev AWS account
