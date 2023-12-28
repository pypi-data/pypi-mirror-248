# directoryshard
Shard filenames into subdirectories.

A large number of files in a single directory can make operations such as listing or browsing cumbersome. 
Splitting files into subdirectories alleviates this. 

## API
Two methods are provided:
 
    def shardprefix(filename: str) -> str:
    """Return a 2 character alphanumeric string by deterministically hashing filename"""

    def sharded(filepath: Path) -> Path:
     """Return path sharded into subdirectory"""

## Class

**ShardedDirectory** provides getting file paths from a directory:


    sharded_tmp = ShardedDirectory('/tmp)
    print(sharded_tmp.filepath('python'))

return */tmp/ep.python*.