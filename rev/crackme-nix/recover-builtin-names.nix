let
    get_builtin_by_hash =
    with builtins;
    builtin_hash_name:
    head (filter (attribute_name: hashString "sha256" attribute_name == builtin_hash_name) (attrNames builtins));

    custom_builtins = {
        ADu9AD5I = get_builtin_by_hash "eafe895eb8119e6e5d06463590b2ef81b3651c157d5c8e18f1889186c7fd0ac0";
        ahse8ueB = get_builtin_by_hash "32e15d12dc4ac09d025c6a6a8210c7abaa220e462e99fdc694ae6cb1ea3bf40f";
        aiCoo0ph = get_builtin_by_hash "9f2e6d33a3717ee826353a404ba4618d1aeeb6879ad7936bce8ed5f46814924d";
        au9ooKaa = get_builtin_by_hash "0c62f876ef1dea830de9f32c2f4b46dd6d74d50d15896e09ef5a2fcd4ac7e1d7";
        die0Aemi = get_builtin_by_hash "2b9c5d5d52d96c349d07d6c78ae2716b27c21619598545086f3d8aaab1c122c6";
        eag0eiJu = get_builtin_by_hash "1b8ff7f5693dc807c609c83b6d8213715fd14938916acd784dfccbc586fd4528";
        ee9Deike = get_builtin_by_hash "1a1cd8136092f08584f8be479f7453e2d51da635ce3d34408f289f73c11d31db";
        EiThohw9 = get_builtin_by_hash "2b6badd843c60121c895d257e0b31f51b62466043460748350f16d384eac9d1a";
        Et0odohz = get_builtin_by_hash "9e0689626a1e02ffa425a4ac0ff23328fd2fb7deae2f76c82ad0d9de792d58ba";
        Fotea9ah = get_builtin_by_hash "29df0906e1730ea20667b4788939c47a20cf1cde6fa8ca173307efde7088f458";
        geeJ0fez = get_builtin_by_hash "ddc6e2b224d0fd821669202258386936fc9ce2899e215eec6322b95f8dd96d6a";
        iiV8Em3u = get_builtin_by_hash "60be9861750facbfad8758254a2f76c0cfe78d54459a3bc187d49b1401fcd8e8";
        Mei2kohw = get_builtin_by_hash "7e9e5ac30f2216fd0fd6f5faed316f2d5983361a4203c3330cfa46ef65bb4767";
        ohR3phie = get_builtin_by_hash "bbb522f7e532f10d2d79413a98bdec613444b049a3c98639fb17831d712a2ca2";
        phee1Aid = get_builtin_by_hash "7344ac65393d5d558603a40ad0a7aff85dc418df6f0b7a559802bc6bd016e8d1";
        seecohJ8 = get_builtin_by_hash "fe64b11c32bf5a63de33a2892307c08e4a9db5d483de86a6d8d465cba6b27ca4";
        sha1Kaa8 = get_builtin_by_hash "2265d647e8fb3545b296b1a6f823c87fcec6c5e0292f2347e0ded18d5fe23b3d";
        Tohy5uez = get_builtin_by_hash "cd35a2426062b7d58fd4a63f813cc506ef87e449087d28d256b8c393f20fa364";
        Uwae2iet = get_builtin_by_hash "0f82aca66af91493b1ff401de5f1f7e3e24e14560df3f6f7e465dbc915b9947d";
        Wa0phoo2 = get_builtin_by_hash "1605510b959ee96596cd14f92a5735c8977cbf47cc7765b434b20d0b1d7fac13";
        Xu4coh1L = get_builtin_by_hash "da49315e924b8bebc1bad9f9ad7e6963cbb1f5a42a29413c389cfe7f696218e6";
    };
in 
with builtins;
{
    custom_builtins = custom_builtins;
}