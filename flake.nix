{
  description = "Flake for when2meet-cli";

  inputs = {
   nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05"; 
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in
  {
    devShells.${system}.default =
    pkgs.mkShell
    {
      buildInputs = [
        pkgs.python311
        pkgs.python311Packages.pyvirtualdisplay
        pkgs.python311Packages.selenium
        pkgs.geckodriver
      ];   

      shellHook = ''
      echo "You are now in the flake environment"
      '';
    };
  }; 
}
