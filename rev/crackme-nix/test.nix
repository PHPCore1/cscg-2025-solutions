let
    pwr =
      base: exponent:
      builtins.foldl' (x: y: x * y) 1 (
        builtins.genList (index: base) exponent
      );
in 
with builtins;
{
  test = pwr 2 12;
}