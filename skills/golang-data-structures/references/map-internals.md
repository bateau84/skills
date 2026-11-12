# Map Internals Deep Dive

## Hash table layout depends on Go version

**Go 1.24+ (default runtime):** the built-in map uses Swiss Table-inspired groups of eight slots with control bytes, one or more tables, and table splitting/growth. Its exact fill thresholds and internal shapes are implementation details, not API contracts. Do not diagnose current memory behavior using the older `B`, `oldbuckets`, overflow-chain or `6.5 entries/bucket` model. See [Go's Swiss Table implementation](https://go.dev/blog/swisstable).

**Before Go 1.24:** the older runtime used eight-entry buckets, overflow buckets, a bucket-count exponent `B`, and incremental evacuation. Only apply those details after verifying the target toolchain/runtime configuration.

## Memory growth and capacity

- There is no map `cap()`; `make(map[K]V, hint)` offers an approximate size hint and reduces some growth costs but does not promise a specific number of groups/buckets.
- Deleting keys does not guarantee the backing allocation immediately shrinks. If retained memory matters, measure it under the deployed Go version, then consider rebuilding a map at a bounded lifecycle boundary.
- Keys must be comparable; map iteration order is unspecified. Benchmark actual access patterns before asserting a specific collision or growth cost.

## Preallocation

```go
m := make(map[string]int, expectedSize) // capacity hint, not a fixed bucket count
```

## Pointers vs Values

For large value types, storing pointers reduces copy overhead:

```go
// Large struct — copied on every read/write
m := map[string]BigStruct{}  // copies large struct

// Pointer — only pointer is copied
m := map[string]*BigStruct{} // copies 8-byte pointer
```

Trade-off: pointer maps add GC pressure. For small structs (< 128 bytes), value maps are typically faster.

## `maps` Package (Go 1.21+)

| Function | Description |
| --- | --- |
| `Clone`, `Equal`, `EqualFunc` | Shallow copy and equality comparison |
| `Keys`, `Values`, `All` (1.23+) | Iterators over keys, values, or pairs |
| `Collect`, `Insert` (1.23+) | Build maps from iterators or insert entries |

See `golang-safety` skill for `Clone`, `Equal`, and sorted iteration patterns.

## Map Key Requirements

Map keys must be comparable (`==` must work). This includes:

- All numeric types, `string`, `bool`
- Pointers, channels, interfaces (compared by identity)
- Arrays of comparable types
- Structs where all fields are comparable

Slices, maps, and functions **cannot** be map keys.
