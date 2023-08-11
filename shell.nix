with import <nixpkgs> {};

let
  pythonPackages = python39Packages;

in pkgs.mkShell rec {
  name = "ngd-proxy-tester-dev-venv";
  venvDir = "./.venv";
  buildInputs = [
    # install python interpreter
    pythonPackages.python

    # python venv shell hook
    pythonPackages.venvShellHook
  ];
  postVenvCreation = ''
    echo "installing requirements.txt"
    pip install -r requirements.txt
  '';
  postShellHook = ''
    echo "installing boto3-stubs for lsp"
    pip install 'boto3-stubs[essential]'
  '';
}
