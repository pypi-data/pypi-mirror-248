{
  makesLib,
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit nixpkgs python_version;
    inherit (makesLib) pythonOverrideUtils;
  };
  pkgDeps = {
    runtime_deps = with deps.python_pkgs; [
      deprecated
      more-itertools
      simplejson
      types-deprecated
      types-simplejson
      typing-extensions
    ];
    build_deps = with deps.python_pkgs; [flit-core];
    test_deps = with deps.python_pkgs; [
      arch-lint
      mypy
      pytest
      pylint
    ];
  };
  publish = nixpkgs.mkShell {
    packages = [
      nixpkgs.git
      deps.python_pkgs.flit
    ];
  };
  packages = makesLib.makePythonPyprojectPackage {
    inherit (deps.lib) buildEnv buildPythonPackage;
    inherit pkgDeps src;
  };
  dev_shell = import ./dev_env {
    inherit nixpkgs;
    dev_env = packages.env.dev;
  };
in
  packages // {inherit dev_shell publish;}
