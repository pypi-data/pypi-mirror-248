import whiledb_rs

whiledb_rs.exec(
"""
print(1) = "OK";
print(print(2));
"""
)