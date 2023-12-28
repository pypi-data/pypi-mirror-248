import speedy_antlr_lua_parser

assert speedy_antlr_lua_parser.sa_lua.USE_CPP_IMPLEMENTATION
speedy_antlr_lua_parser.parse_chunk("a = 1")
